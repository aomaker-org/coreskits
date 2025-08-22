Of course. Here is a comprehensive `README.md` file for the `run.py` script, designed to be clear, informative, and easy for any user to follow.

-----

# `run.py`: A Command-Line Wrapper for Robust Logging

`run.py` is a versatile Python script that acts as a wrapper for any command-line program. Its primary purpose is to execute a command, capture all of its output (`stdout` and `stderr`), and meticulously log it in real-time to both the console and a uniquely timestamped log file.

This tool is invaluable for development, automation, and CI/CD pipelines where you need a persistent, detailed, and timestamped record of a command's execution without losing the immediate feedback of seeing the output on your screen.

## Key Features

  - **Real-time Streaming:** Output from the command is captured and displayed line-by-line as it's generated. You don't have to wait for the command to finish to see its output.
  - **"Tee" Functionality:** Just like the Unix `tee` command, it shows the command's output on the console while simultaneously writing it to a file.
  - **Automatic Timestamped Logs:** Each time you run a command, a new log file is created in a `logs/` directory with a unique name based on the command and the current timestamp (e.g., `logs/ping_2025-08-20_15-30-44.log`).
  - **Detailed Log Records:** Inside the log file, every single line from `stdout` and `stderr` is prefixed with a high-precision timestamp and a log level, making it easy to analyze timings and trace events.
  - **Differentiated `stdout` vs. `stderr`:** By default, lines from `stdout` are logged as `INFO` and lines from `stderr` are logged as `ERROR`, making it easy to spot issues in the log file.
  - **Exit Code Propagation:** The script exits with the *exact same exit code* as the command it wrapped. This ensures it can be seamlessly integrated into shell scripts and build systems that rely on exit codes to determine success or failure.
  - **Simple and Dependency-Light:** Requires only Python and the excellent `loguru` library.

## Requirements

  - Python 3.7+
  - `loguru` library

## Installation & Setup

1.  **Save the Script:** Place the `run.py` script in your project directory or in a location that is part of your system's `PATH` for easy access.

2.  **Install Dependencies:** Install the `loguru` library using pip.

    ```bash
    pip install loguru
    ```

## Usage

The syntax is straightforward: simply prefix the command you want to run with `python run.py`.

**General Syntax:**

```bash
python run.py <your_command> [arg1] [arg2] ...
```

### Examples

**1. Basic network command:**

```bash
python run.py ping -c 4 google.com
```

**2. Command with both `stdout` and `stderr`:**

```bash
python run.py ls -la / /non_existent_directory
```

**3. Long-running process to demonstrate streaming:**

```bash
python run.py bash -c "for i in {1..5}; do echo \"Processing item \$i...\"; sleep 1; done"
```

**4. Wrapping another Python script:**

```bash
python run.py python your_other_script.py --input data.csv
```

-----

## Example Walkthrough

Let's run a command that we know will produce both standard output and an error.

#### 1\. The Command

We'll execute `ls -l` on the root directory (`/`) which will succeed, and on a directory that doesn't exist, which will fail.

```bash
python run.py ls -l / /non_existent_dir
```

#### 2\. Console Output

You will see the script's status messages, followed by the real-time, interleaved output from the `ls` command, and a final status message with the exit code.

```text
2025-08-20 15:30:44 | INFO     | RUNNER | Executing command: ls -l / /non_existent_dir
2025-08-20 15:30:44 | INFO     | RUNNER | Full log file at: /home/user/project/logs/ls_2025-08-20_15-30-44.log
--------------------------------------------------------------------------------
ls: cannot access '/non_existent_dir': No such file or directory
/:
total 64
dr-xr-xr-x.   1 root root  4096 Aug 19 09:00 bin
dr-xr-xr-x.   1 root root  4096 Aug 19 09:00 boot
drwxr-xr-x.  20 root root  3220 Aug 20 15:00 dev
... (rest of stdout from ls) ...
--------------------------------------------------------------------------------
2025-08-20 15:30:45 | ERROR    | RUNNER | Command failed with exit code: 2
```

#### 3\. Generated Log File

The script will create a file inside the `logs/` directory. Based on the timestamp above, the file would be named: `logs/ls_2025-08-20_15-30-44.log`.

#### 4\. Log File Content

This file contains the complete, timestamped record of the execution. Note how the error line is clearly marked with the `ERROR` level.

```log
2025-08-20 15:30:44.810 | ERROR    | ls: cannot access '/non_existent_dir': No such file or directory
2025-08-20 15:30:44.812 | INFO     | /:
2025-08-20 15:30:44.812 | INFO     | total 64
2025-08-20 15:30:44.812 | INFO     | dr-xr-xr-x.   1 root root  4096 Aug 19 09:00 bin
2025-08-20 15:30:44.812 | INFO     | dr-xr-xr-x.   1 root root  4096 Aug 19 09:00 boot
2025-08-20 15:30:44.812 | INFO     | drwxr-xr-x.  20 root root  3220 Aug 20 15:00 dev
...
```

## How It Works

  - The script uses Python's `subprocess.Popen` to execute the given command in a non-blocking manner, redirecting its `stdout` and `stderr` streams to pipes.
  - To prevent deadlocks (where the script might wait for `stdout` while the `stderr` buffer fills up, or vice versa), it launches two separate threads: one dedicated to reading the `stdout` pipe and another for the `stderr` pipe.
  - Each thread reads its assigned pipe line-by-line. For each line it reads, it performs two actions:
    1.  It `print()`s the line directly to the console for immediate viewing.
    2.  It passes the line to a `loguru` logging function (`logger.info` for stdout, `logger.error` for stderr), which handles timestamping and writing to the log file.
  - The main process waits for the command to complete and for both streaming threads to finish before exiting.

## License

This script is released under the MIT License.
