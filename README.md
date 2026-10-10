# AI Infrastructure Lab

Hands-on experiments in AI infrastructure, GPU computing, Linux systems engineering, Kubernetes, observability, and inference serving.

The goal is to understand how AI infrastructure works in practice through reproducible experiments, system measurements, troubleshooting, and technical documentation.

## Objectives

- Understand GPU architecture, compute, memory, and telemetry.
- Explore GPU health monitoring, diagnostics, and observability.
- Build practical experience with Kubernetes scheduling and GPU workloads.
- Investigate AI inference serving, performance, and resource utilization.
- Automate infrastructure tasks and document reproducible procedures.
- Connect infrastructure components into an observable, production-oriented AI platform.

## Technical Areas

| Area | Focus |
|---|---|
| GPU Infrastructure | NVIDIA GPUs, drivers, CUDA, DCGM, GPU memory, compute utilization |
| GPU Observability | Health monitoring, diagnostics, telemetry, DCGM Exporter |
| Monitoring | Prometheus, Grafana, metrics collection, dashboards, alerting |
| Kubernetes | Cluster architecture, scheduling, resource requests, affinity, priority, multi-tenancy |
| AI Workloads | PyTorch, GPU compute, memory allocation, inference workloads |
| Inference Serving | vLLM, serving architecture, throughput, latency, resource utilization |
| Linux Engineering | System administration, performance analysis, networking, storage, automation |
| Multi-GPU Systems | GPU interconnects, NVLink, NVSwitch, InfiniBand, fabric observability |
| Automation | Python, shell scripting, YAML, Git, repeatable lab procedures |

## Experiments

### 1. NVIDIA DCGM GPU Observability

**Status:** Initial experiments completed; workload telemetry validation remains in progress.

Explore GPU discovery, health monitoring, diagnostics, persistence mode, and telemetry using NVIDIA Data Center GPU Manager.

Work completed:

- Installed and verified DCGM 4.7.0.
- Discovered an active NVIDIA Tesla T4 GPU.
- Enabled DCGM health monitoring and process statistics watches.
- Passed Level 1 diagnostics after enabling persistence mode.
- Observed idle GPU clock, temperature, power, and utilization.
- Executed a PyTorch matrix multiplication workload.
- Recorded approximately 200 iterations over 73 seconds, with approximately 2.76 GiB of PyTorch GPU memory allocated.

Next steps:

- Capture DCGM telemetry during active GPU computation.
- Compare DCGM and NVIDIA-SMI observations under load.
- Explore DCGM Exporter.
- Integrate GPU metrics with Prometheus and Grafana.

**Lab documentation:** [DCGM GPU Observability Lab](dcgm-lab/README.md)

### 2. GPU Performance and Workload Analysis

**Status:** Planned and partially explored.

Investigate how GPU compute, memory allocation, utilization, and workload characteristics affect observed behavior.

Planned experiments:

- Matrix multiplication workload analysis.
- GPU memory allocation and utilization.
- Telemetry comparison under idle and active conditions.
- Workload duration and iteration measurements.
- Performance observations across different workload parameters.

### 3. GPU Observability Stack

**Status:** Planned.

Build a monitoring stack that exposes GPU metrics and makes infrastructure behavior easier to understand.

Planned components:

- NVIDIA DCGM Exporter.
- Prometheus metrics collection.
- Grafana dashboards.
- GPU utilization, temperature, power, and memory panels.
- Alerting and monitoring validation.

### 4. Kubernetes GPU Scheduling

**Status:** In progress.

Explore Kubernetes scheduling concepts and how GPU resources can be represented, requested, and allocated to workloads.

Planned and ongoing topics:

- Kubernetes device plugin architecture.
- GPU resource requests and limits.
- GPU node labels, taints, and tolerations.
- Node affinity and workload placement.
- Priority classes and preemption.
- Resource quotas and multi-tenant GPU allocation.
- NVIDIA GPU Operator architecture.
- Multi-Instance GPU (MIG) and GPU time-slicing concepts.

### 5. AI Inference Serving

**Status:** Planned.

Explore how AI models are deployed and served on GPU infrastructure.

Planned experiments:

- vLLM installation and configuration.
- Model serving architecture.
- GPU memory requirements.
- Request throughput and latency.
- Concurrency and workload behavior.
- Monitoring inference-serving resources.

### 6. Multi-GPU Infrastructure

**Status:** Planned.

Investigate the hardware and networking technologies that support distributed GPU workloads.

Planned topics:

- NVLink and NVSwitch.
- InfiniBand and high-performance networking.
- GPU-to-GPU communication.
- NVIDIA Collective Communications Library (NCCL).
- Multi-GPU telemetry and observability.
- Fabric performance and troubleshooting.

## Repository Structure

```text
ai-infrastructure-lab/
├── README.md
└── dcgm-lab/
    ├── README.md
    ├── install-dcgm.sh
    ├── verify-dcgm.sh
    ├── workload/
    │   └── gpu-workload.py
    └── monitoring/
        └── dcgm-monitor.sh
```

Additional experiments will be organized into their own directories as the lab grows.

## Current Test Environment

| Component | Observed configuration |
|---|---|
| GPU | NVIDIA Tesla T4 (16 GB) |
| NVIDIA Driver | 580.82.07 |
| CUDA version reported by `nvidia-smi` | 13.0 |
| DCGM | 4.7.0 |
| Operating system | Ubuntu-based Linux |

These details describe the environment used for the initial DCGM experiments. Other experiments may use different hardware, operating systems, or software versions.

## Roadmap

The roadmap is organized around progressing from individual GPU experiments to an observable AI infrastructure platform.

- [x] Install and verify NVIDIA DCGM.
- [x] Discover GPU resources and check GPU health.
- [x] Run DCGM Level 1 diagnostics.
- [x] Execute a PyTorch GPU workload.
- [x] Document initial GPU telemetry observations.
- [ ] Capture telemetry during active GPU computation.
- [ ] Compare DCGM and NVIDIA-SMI under load.
- [ ] Deploy DCGM Exporter.
- [ ] Integrate Prometheus and Grafana.
- [ ] Build GPU monitoring dashboards and alerts.
- [ ] Continue Kubernetes GPU scheduling exercises.
- [ ] Explore NVIDIA GPU Operator architecture.
- [ ] Investigate MIG and GPU time-slicing.
- [ ] Deploy an inference-serving workload with vLLM.
- [ ] Measure inference throughput, latency, and GPU memory use.
- [ ] Explore multi-GPU communication and fabric observability.

## Engineering Principles

- **Reproducibility:** Document the commands and configuration needed to repeat an experiment.
- **Measurement:** Back quantitative claims with actual command output or captured experiment logs.
- **Validation:** Verify expected behavior instead of assuming that installation means the system works.
- **Observability:** Connect workload behavior with measurable system metrics.
- **Troubleshooting:** Record errors, root causes, corrective actions, and limitations.
- **Incremental development:** Build from individual components toward integrated infrastructure.

## Scope and Disclaimer

This is a personal, hands-on engineering lab for learning and experimentation. Scripts and configurations are provided for educational use and should be reviewed before production deployment.

Results depend on hardware, drivers, software versions, workload configuration, and environment-specific restrictions. Planned experiments are distinguished from completed and verified work.
