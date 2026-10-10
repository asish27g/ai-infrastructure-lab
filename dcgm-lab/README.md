# NVIDIA DCGM GPU Observability Lab

Hands-on experiments with NVIDIA Data Center GPU Manager (DCGM) for GPU discovery, health monitoring, diagnostics, and telemetry.

## Environment

| Component | Tested configuration |
|---|---|
| GPU | NVIDIA Tesla T4 (16 GB) |
| NVIDIA Driver | 580.82.07 |
| CUDA Version Reported by `nvidia-smi` | 13.0 |
| DCGM | 4.7.0 |
| Operating System | Ubuntu-based Linux |

## Repository Structure

```text
ai-infrastructure-lab/
└── dcgm-lab/
    ├── README.md
    ├── install-dcgm.sh
    ├── verify-dcgm.sh
    ├── workload/
    │   └── gpu-workload.py
    └── monitoring/
        └── dcgm-monitor.sh
```

## Clone the Repository

```bash
git clone git@github.com:asish27g/ai-infrastructure-lab.git
cd ai-infrastructure-lab/dcgm-lab
```

## 1. Install DCGM

Review the installation script before running it. A compatible NVIDIA driver must already be installed.

```bash
chmod +x install-dcgm.sh
./install-dcgm.sh
```

## 2. Verify the Installation

```bash
chmod +x verify-dcgm.sh
./verify-dcgm.sh
```

Check the DCGM version, GPU status, and discovery results:

```bash
dcgmi version
nvidia-smi
dcgmi discovery --list
```

## 3. Check GPU Health and Diagnostics

Enable DCGM health monitoring:

```bash
dcgmi health -s a
```

Check current GPU health:

```bash
dcgmi health -c
```

Enable process statistics watches:

```bash
dcgmi stats -e
```

Run Level 1 diagnostics:

```bash
dcgmi diag -r 1
```

If diagnostics require persistence mode, enable it where permitted:

```bash
sudo nvidia-smi -i 0 -pm 1
dcgmi diag -r 1
```

## 4. Monitor GPU Telemetry

Run the monitoring script:

```bash
chmod +x monitoring/dcgm-monitor.sh
./monitoring/dcgm-monitor.sh
```

Alternatively, run DCGM monitoring directly:

```bash
dcgmi dmon -e 100,150,155,203,204
```

Stop monitoring with `Ctrl+C`.

## 5. Run a GPU Workload

Run the default PyTorch workload:

```bash
python3 workload/gpu-workload.py
```

Run with custom parameters:

```bash
python3 workload/gpu-workload.py \
  --seconds 60 \
  --size 4096 \
  --memory-gb 1
```

Ensure PyTorch and a compatible CUDA-enabled build are installed before running the workload.

For workload telemetry, run the monitoring script in one terminal and the GPU workload in another. Compare the captured outputs to observe GPU behavior under load.

## 6. Check Persistence Mode

```bash
nvidia-smi --query-gpu=index,name,persistence_mode \
  --format=csv
```

## Validation Checklist

- [ ] DCGM version verified
- [ ] GPU discovered and reported active
- [ ] DCGM health checks completed
- [ ] Level 1 diagnostic results recorded
- [ ] Idle GPU telemetry observed
- [ ] PyTorch GPU workload completed
- [ ] Telemetry captured during active workload
- [ ] Command output and experiment results documented

## Troubleshooting

### GPU Not Detected

```bash
nvidia-smi
dcgmi discovery --list
```

Verify the NVIDIA driver, GPU visibility, permissions, and DCGM Host Engine status.

### Diagnostics Fail

Review the diagnostic output and verify compatibility between the GPU, driver, and DCGM version. Some checks may require elevated privileges.

### Telemetry Not Available

Check DCGM monitoring options:

```bash
dcgmi dmon --help
```

Verify that the DCGM Host Engine is running and that the selected telemetry fields are supported.

## Scope

This lab covers DCGM installation, GPU discovery, health monitoring, diagnostics, and telemetry. Future experiments will explore DCGM Exporter, Prometheus, Grafana, Kubernetes GPU observability, and multi-GPU monitoring.

Document measured results only when supported by actual command output or captured experiment logs.
