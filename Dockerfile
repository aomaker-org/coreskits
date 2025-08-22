# Dockerfile for MicroPython Development Environment

# Use a recent Ubuntu LTS release
FROM ubuntu:22.04

# Set non-interactive frontend for package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies for MicroPython, QEMU, and OpenOCD
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    wget \
    curl \
    ssh \
    sudo \
    libffi-dev \
    pkg-config \
    python3 \
    python3-pip \
    gcc-arm-none-eabi \
    libnewlib-arm-none-eabi \
    cmake \
    libglib2.0-dev \
    libgcrypt20-dev \
    zlib1g-dev \
    autoconf \
    automake \
    libtool \
    bison \
    flex \
    libpixman-1-dev \
    meson \
    ninja-build \
    diffutils \
    libusb-1.0-0-dev \
    openocd \
    && rm -rf /var/lib/apt/lists/*

# Clone the MicroPython repository
RUN git clone --depth 1 --branch v1.26.0 https://github.com/micropython/micropython.git /micropython

# Clone, build, and install QEMU with RP2040 support
RUN git clone https://github.com/ME-IRL/qemu-rp2040.git /qemu-rp2040
WORKDIR /qemu-rp2040
RUN ./configure --target-list=arm-softmmu --enable-fdt --disable-kvm --disable-xen
RUN make -j$(nproc)
RUN make install
WORKDIR /

# Download Picoprobe firmware
RUN wget https://github.com/raspberrypi/debugprobe/releases/download/debugprobe-v2.2.3/debugprobe_on_pico.uf2 -O /picoprobe.uf2

# SSH public key build argument
ARG SSH_PUBLIC_KEY

# Create a non-root user and set up SSH
RUN useradd -m -s /bin/bash -G sudo user && \
    echo "user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    mkdir -p /home/user/.ssh && \
    echo "${SSH_PUBLIC_KEY}" > /home/user/.ssh/authorized_keys && \
    chown -R user:user /home/user/.ssh && \
    chmod 700 /home/user/.ssh && \
    chmod 600 /home/user/.ssh/authorized_keys

# Set up SSH for root user
RUN mkdir -p /root/.ssh && \
    cp /home/user/.ssh/authorized_keys /root/.ssh/authorized_keys && \
    chmod 700 /root/.ssh && \
    chmod 600 /root/.ssh/authorized_keys

# Configure and expose SSH
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config

EXPOSE 22

# Start SSH server
CMD ["/usr/sbin/sshd", "-D"]
