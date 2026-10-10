# ai-infrastructure-lab
# NVIDIA DCGM GPU Observability Lab

Hands-on GPU observability using NVIDIA Data Center GPU Manager (DCGM).

## Environment

- NVIDIA GPU
- NVIDIA Driver
- CUDA
- Ubuntu/Debian-based Linux
- DCGM 4.x

## Repository structure

```text
dcgm-lab/
├── README.md
├── install-dcgm.sh
├── verify-dcgm.sh
├── workload/
└── monitoring/
    └── dcgm-monitor.sh

## Install

Repository

```
https://github.com/asish27g/ai-infrastructure-lab.git
```

Clone the repository:

```bash
git clone git@github.com:asish27g/ai-infrastructure-lab.git
cd dcgm-lab

#How to install DCGM
chmod +x install-dcgm.sh
./install-dcgm.sh

#How to verify DCGM Install status
chmod +x verify-dcgm.sh
./verify-dcgm.sh

#How to monitor GPU with DCGM
chmod +x monitoring/dcgm-monitor.sh
./monitoring/dcgm-monitor.sh


# Show GPU and driver information
nvidia-smi

# Discover GPUs known to DCGM
dcgmi discovery --list

# Enable all DCGM health-watch groups
dcgmi health -s a

# Check current health
dcgmi health -c

# Enable process statistics watches
dcgmi stats -e

# Run Level 1 diagnostics
dcgmi diag -r 1

# View selected telemetry fields
dcgmi dmon -e 100,150,155,203,204

#Workiad run
python3 workload/gpu-workload.py
#Custom run
#python3 workload/gpu-workload.py --seconds 60 --size 4096 --memory-gb 1

# Check persistence mode
nvidia-smi --query-gpu=index,name,persistence_mode \
  --format=csv
