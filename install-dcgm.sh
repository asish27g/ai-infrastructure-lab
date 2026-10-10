#!/usr/bin/env bash

set -euo pipefail

echo "========================================"
echo " NVIDIA DCGM Installation"
echo "========================================"

# --------------------------------------------------
# Configuration
# --------------------------------------------------

CUDA_REPO="https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64"
CUDA_KEYRING="cuda-keyring_1.1-1_all.deb"
DCGM_PACKAGE="datacenter-gpu-manager-4-cuda13"

# --------------------------------------------------
# Check prerequisites
# --------------------------------------------------

if [[ "${EUID}" -eq 0 ]]; then
    SUDO=""
else
    SUDO="sudo"
fi

if ! command -v nvidia-smi >/dev/null 2>&1; then
    echo "ERROR: nvidia-smi not found."
    echo "Install/configure the NVIDIA driver first."
    exit 1
fi

echo
echo "[1/7] Checking NVIDIA GPU..."
nvidia-smi

# --------------------------------------------------
# Install CUDA repository keyring
# --------------------------------------------------

echo
echo "[2/7] Installing NVIDIA CUDA repository keyring..."

if ! dpkg -s cuda-keyring >/dev/null 2>&1; then
    wget -q "${CUDA_REPO}/${CUDA_KEYRING}"
    ${SUDO} dpkg -i "${CUDA_KEYRING}"
    rm -f "${CUDA_KEYRING}"
else
    echo "CUDA keyring already installed."
fi

# --------------------------------------------------
# Update package repository
# --------------------------------------------------

echo
echo "[3/7] Updating package repository..."

${SUDO} apt-get update

# --------------------------------------------------
# Install DCGM
# --------------------------------------------------

echo
echo "[4/7] Installing DCGM..."

${SUDO} apt-get install -y "${DCGM_PACKAGE}"

# --------------------------------------------------
# Verify installation
# --------------------------------------------------

echo
echo "[5/7] Verifying DCGM installation..."

command -v dcgmi
command -v nv-hostengine

dcgmi --version

# --------------------------------------------------
# Enable GPU persistence mode
# --------------------------------------------------

echo
echo "[6/7] Enabling NVIDIA persistence mode..."

GPU_COUNT=$(nvidia-smi --query-gpu=count --format=csv,noheader | head -n1)

for ((GPU=0; GPU<GPU_COUNT; GPU++)); do
    ${SUDO} nvidia-smi -i "${GPU}" -pm 1
done

# --------------------------------------------------
# Start DCGM Host Engine
# --------------------------------------------------

echo
echo "[7/7] Starting DCGM Host Engine..."

if pgrep -x nv-hostengine >/dev/null 2>&1; then
    echo "nv-hostengine is already running."
else
    ${SUDO} nv-hostengine
fi

echo
echo "========================================"
echo " DCGM installation complete"
echo "========================================"

echo
echo "DCGM version:"
dcgmi --version

echo
echo "GPU:"
nvidia-smi --query-gpu=index,name,driver_version,memory.total \
    --format=csv

echo
echo "DCGM discovery:"
dcgmi discovery --list
