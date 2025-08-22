# Getting Started

This guide will walk you through setting up and using this MicroPython development environment.

## Prerequisites

- [Docker](https://www.docker.com/get-started) must be installed on your system.
- You should have a basic understanding of how to use the command line.
- You should have an SSH key pair. If you don't have one, you can generate one with `ssh-keygen -t rsa -b 4096`.

## 1. Build the Docker Image

The first step is to build the Docker image that contains the development environment. This image is configured to use your personal SSH public key for secure access.

From the `523` directory, run the `build_docker` task, passing the path to your public key:

```bash
doit build_docker --ssh-key /path/to/your/id_rsa.pub
```
By default, it will look for `~/.ssh/id_rsa.pub`.

This will execute the `build_docker` task defined in the `dodo.py` script, which in turn runs `docker build`. This may take some time as it downloads the base image and installs all the necessary dependencies.

## 2. Run the Container

Once the image is built, you can run a container from it:

```bash
doit run_container
```
This will start the container in detached mode and map port 2222 on your host to port 22 in the container for SSH access. The container will be named `micropython-dev-container`.

## 3. Connect via SSH

You can now connect to the running container using your private key.

To connect as the non-root `user`:
```bash
ssh -i /path/to/your/id_rsa -p 2222 user@localhost
```

To connect as `root`:
```bash
ssh -i /path/to/your/id_rsa -p 2222 root@localhost
```

You will now have a shell inside the container, with all the tools and source code needed to build and test MicroPython.

## 4. Building Firmware

Inside the container, you can build the firmware for different boards. For example, to build for the Raspberry Pi Pico:

```bash
cd /micropython/ports/rp2
make BOARD=RPI_PICO
```

The resulting `.uf2` file will be in the `build-RPI_PICO` directory.

You can also do this from your host machine using the `doit` script:
```bash
doit build_firmware --board=RPI_PICO
```

## 5. Running Tests

The test suite can be run against the emulated RP2040. From your host machine, run:

```bash
doit test
```
This will execute the test suite inside the Docker container.

## 6. Development Workflow with Bind Mounts

For a more convenient development workflow, you can stop the existing container and start a new one with a bind mount. This will share a directory from your host machine with the container.

First, stop the running container:
```bash
doit stop_container
```

Then, start a new container with a bind mount. For example, to mount a `workspace` directory from your current directory into the container at `/home/user/workspace`:

```bash
docker run -d -p 2222:22 -v $(pwd)/workspace:/home/user/workspace --name micropython-dev-container micropython-dev
```

You can now edit files in the `workspace` directory on your host, and the changes will be immediately available in the container.

## 7. Debugging with Picoprobe

This development environment includes tools for debugging the RP2040 using a Raspberry Pi Pico running the Picoprobe firmware.

### Picoprobe Firmware

The pre-built Picoprobe firmware (`picoprobe.uf2`) is included in the root directory of the container (`/picoprobe.uf2`). You can copy this file out of the container and flash it to a Raspberry Pi Pico to turn it into a debug probe.

To copy the firmware from the container to your host machine:
```bash
docker cp micropython-dev-container:/picoprobe.uf2 .
```

### OpenOCD

The environment includes OpenOCD, a tool for on-chip debugging. To use it with a Picoprobe, you will need to forward the Picoprobe's USB device from your host machine to the Docker container. This can be done with the `--device` flag when running `docker run`.

For example, if your Picoprobe is at `/dev/ttyACM0` on your host:
```bash
docker run -d -p 2222:22 --device=/dev/ttyACM0 --name micropython-dev-container micropython-dev
```
**Note:** The exact device path may vary. You may also need to grant the correct permissions to the device on your host.

Once the device is forwarded, you can run OpenOCD inside the container. You will need to create an OpenOCD configuration file or use one of the standard ones. For the Raspberry Pi Pico, the command would look something like this:

```bash
openocd -f interface/picoprobe.cfg -f target/rp2040.cfg
```

This will start an OpenOCD server, which you can then connect to with GDB for debugging.
