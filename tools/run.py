#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A wrapper script to execute command-line programs and capture their output.

This script uses the 'loguru' library to provide robust, real-time logging
of stdout and stderr to both the console and a timestamped log file.

Features:
- Executes any command passed as arguments.
- Creates a 'logs' directory for log files.
- Generates a unique, timestamped log file for each execution.
- Streams stdout and stderr line-by-line in real-time.
- Prints command output directly to the console (like 'tee').
- Logs command output to the file with detailed timestamps and levels.
- Exits with the same return code as the executed command.

Usage:
    python run.py <your_command> [arg1] [arg2] ...

Example:
    python run.py ping -c 5 google.com
    python run.py ls -la /non_existent_directory
    python run.py bash -c "for i in {1..5}; do echo 'Hello $i'; sleep 1; done"
"""

import sys
import subprocess
import threading
from datetime import datetime
from pathlib import Path

from loguru import logger

def setup_logging(command_str: str):
    """Configures loguru sinks for console and a timestamped file."""

    # Sanitize command string for use in filename
    sanitized_command = "".join(
        [c if c.isalnum() else "_" for c in command_str.split()[0]]
    )

    # Create a 'logs' directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # Generate a timestamped log file path
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file_path = logs_dir / f"{sanitized_command}_{timestamp}.log"

    # Remove default handler to avoid duplicate console output
    logger.remove()

    # Console sink for the wrapper's own status messages
    # This keeps the console clean for the subprocess output.
    logger.add(
        sys.stderr,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>RUNNER</cyan> | <level>{message}</level>",
        colorize=True
    )

    # File sink for detailed, timestamped logging of everything
    logger.add(
        log_file_path,
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {message}",
        encoding="utf-8"
    )

    return log_file_path

def stream_output(pipe, log_function):
    """
    Reads from a subprocess pipe line-by-line and handles both logging and printing.

    Args:
        pipe: The subprocess pipe to read from (e.g., proc.stdout).
        log_function: The loguru function to use for logging (e.g., logger.info).
    """
    try:
        # Use iter to read lines in a non-blocking way
        for line in iter(pipe.readline, b''):
            decoded_line = line.decode('utf-8').strip()

            # 1. Log to file (with loguru's timestamp)
            log_function(decoded_line)

            # 2. Print to console (the "tee" or "tail -F" part)
            print(decoded_line, flush=True)
    finally:
        pipe.close()

def main():
    """Main function to parse arguments, run command, and log output."""
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <command> [args...]", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1:]
    command_str = ' '.join(command)

    log_file_path = setup_logging(command_str)

    logger.info(f"Executing command: {command_str}")
    logger.info(f"Full log file at: {log_file_path.resolve()}")
    print("-" * 80) # Separator for clarity

    try:
        # Popen is used for non-blocking, real-time streaming
        # stdout and stderr are redirected to pipes for capture
        proc = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Use separate threads to read stdout and stderr concurrently
        # This prevents deadlocks if one buffer fills up while waiting on the other
        stdout_thread = threading.Thread(
            target=stream_output,
            args=(proc.stdout, logger.info)
        )
        stderr_thread = threading.Thread(
            target=stream_output,
            args=(proc.stderr, logger.error)
        )

        stdout_thread.start()
        stderr_thread.start()

        stdout_thread.join()
        stderr_thread.join()

        # Wait for the process to terminate and get the return code
        return_code = proc.wait()

        print("-" * 80)
        if return_code == 0:
            logger.success(f"Command finished successfully with exit code: {return_code}")
        else:
            logger.error(f"Command failed with exit code: {return_code}")

        sys.exit(return_code)

    except FileNotFoundError:
        logger.critical(f"Command not found: '{command[0]}'")
        sys.exit(127) # Standard exit code for "command not found"
    except Exception as e:
        logger.critical(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
