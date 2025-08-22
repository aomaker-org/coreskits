# MicroPython Development Environment for RP2040/RP235x (523)

This repository contains a comprehensive, Docker-based development environment for building and testing MicroPython for the Raspberry Pi RP2040 and RP235x microcontrollers.

This project was created to provide a complete, self-contained, and secure development environment, with a focus on robust logging and automation.

## Features

- **Dockerized:** The entire development environment is containerized with Docker, ensuring consistency and reproducibility.
- **Secure SSH:** SSH access is configured to use a user-provided public key for enhanced security.
- **Emulation:** Includes a QEMU-based emulator for the RP2040, allowing for automated testing without physical hardware. **Note:** Emulation for the RP235x is not currently available.
- **Debugging:** Comes with OpenOCD and Picoprobe firmware to support hardware debugging.
- **Automation:** A `dodo.py` script provides a simple command-line interface for common tasks like building, testing, and running the environment.
- **CI/CD Ready:** Includes a GitHub Actions workflow for automated building and testing.

## Getting Started

For instructions on how to set up and use this development environment, please see the [Getting Started guide](Jules/getting_started.md).

## Documentation

- [Getting Started](Jules/getting_started.md): A guide for new users.
- [doit Automation](Jules/doit.md): Detailed documentation for the `dodo.py` script.
- [Developer Log](Jules/devlog.md): A verbose, structured log of the development process for this environment.
