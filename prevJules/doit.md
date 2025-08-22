# `doit` Automation

This project uses the `doit` automation tool to provide a simple command-line interface for common tasks. The tasks are defined in the `dodo.py` file in the `523` directory.

## Available Tasks

You can get a list of all available tasks by running `doit list` from the `523` directory.

### `about`
Prints a short help message. This is the default task that runs if you just execute `doit`.

### `build_docker`
Builds the Docker image for the development environment. It is tagged as `micropython-dev`. This task depends on the `Dockerfile`.

It requires you to provide your SSH public key via the `--ssh-key` parameter.

Example:
```bash
doit build_docker --ssh-key ~/.ssh/id_rsa.pub
```
If no key is provided, it will default to `~/.ssh/id_rsa.pub`.

### `run_container`
Starts a container in detached mode from the `micropython-dev` image. The container is named `micropython-dev-container` and port 2222 on the host is mapped to port 22 in the container.

### `stop_container`
Stops and removes the `micropython-dev-container` container.

### `build_firmware`
Builds the MicroPython firmware for a specific board. This task is run inside the Docker container. It takes a `--board` parameter to specify the target board.
Example:
```bash
doit build_firmware --board=SEEED_XIAO_RP2350
```
If no board is specified, it defaults to `RPI_PICO`.

### `test`
Runs the MicroPython test suite for the `RPI_PICO` board using the QEMU emulator. This task is run inside the Docker container.
