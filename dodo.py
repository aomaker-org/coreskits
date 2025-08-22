import os
import sys
import subprocess

def task_about():
    """Prints a help message"""
    return {
        'actions': ['echo "Please use doit list to see available tasks."'],
        'doc': 'Prints a help message',
    }

def build_docker_action(ssh_key):
    """A Python action to build the Docker image."""
    try:
        with open(ssh_key, 'r') as f:
            ssh_key_content = f.read()
    except FileNotFoundError:
        print(f"Error: SSH key file not found at {ssh_key}", file=sys.stderr)
        return False
    
    cmd = [
        "docker", "build",
        "--build-arg", f"SSH_PUBLIC_KEY={ssh_key_content}",
        "-t", "micropython-dev",
        "."
    ]
    
    # Using Popen for real-time streaming of output
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
            
    return process.poll() == 0


def task_build_docker():
    """Builds the Docker image. Requires --ssh-key parameter pointing to a public SSH key."""
    return {
        'actions': [build_docker_action],
        'params': [
            {
                'name': 'ssh_key',
                'long': 'ssh-key',
                'type': str,
                'default': os.path.expanduser('~/.ssh/id_rsa.pub')
            }
        ],
        'file_dep': ['Dockerfile'],
        'doc': 'Builds the Docker image. Use --ssh-key to specify the path to your public SSH key.',
        'verbosity': 2, # Keep verbosity to see doit's output and any action prints
    }

def task_run_container():
    """Runs the Docker container in detached mode"""
    return {
        'actions': ['docker run -d -p 2222:22 --name micropython-dev-container micropython-dev'],
        'doc': 'Runs the Docker container',
    }

def task_stop_container():
    """Stops the Docker container"""
    return {
        'actions': ['docker stop micropython-dev-container && docker rm micropython-dev-container'],
        'doc': 'Stops and removes the Docker container',
    }

def task_build_firmware():
    """Builds the firmware for a given board"""
    return {
        'actions': ['docker exec micropython-dev-container /bin/bash -c "cd /micropython/ports/rp2 && make BOARD=%(board)s"'],
        'params': [
            {
                'name': 'board',
                'long': 'board',
                'type': str,
                'default': 'RPI_PICO'
            }
        ],
        'doc': 'Builds the firmware for a given board. Use --board to specify the board.',
    }

def task_test():
    """Runs the test suite for the RPI_PICO board"""
    return {
        'actions': ['docker exec micropython-dev-container /bin/bash -c "cd /micropython/tests && ./run-tests.py -t execpty:\\"qemu-system-arm -machine pico -nographic -kernel ../ports/rp2/build-RPI_PICO/firmware.elf\\""'],
        'doc': 'Runs the test suite for the RPI_PICO board',
    }


DOIT_CONFIG = {'default_tasks': ['about']}

