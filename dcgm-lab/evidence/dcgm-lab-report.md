# NVIDIA DCGM GPU Observability Lab — Execution Report

**Lab date:** October 10, 2026  
**Environment:** Google Colab  
**GPU:** NVIDIA Tesla T4  
**DCGM version:** 4.7.0

> Evidence note: This report consolidates the outputs and results

### Command
```bash
dcgmi diag -r 1
```

### Observed result
- Software test: Fail.
- GPU0: Fail.
- The diagnostic warned that persistence mode was disabled.

This was the initial result before persistence mode was enabled.

## 10. Incorrect persistence-mode command

### Command attempted
```bash
nvidia-smi -o 0 -pm 1
```

### Result
The command failed because `-o` was not a valid option for the
intended persistence-mode operation.

## 11. Persistence-mode correction

### Correct command
```bash
nvidia-smi -i 0 -pm 1
```

### Observed output
```text
Enabled Legacy persistence mode for GPU 00000000:00:04.0.
```

Result: Persistence mode was enabled for the Tesla T4 in that session.

## 12. Diagnostic success after the fix

### Command
```bash
dcgmi diag -r 1
```

### Observed result
```text
software Pass
GPU0: Pass
```

Result: The Level 1 diagnostic passed after persistence mode was
enabled.

## 13. Idle GPU telemetry

### Command
```bash
dcgmi dmon -e 100,150,155,203,204
```

### Observed sample values
| Metric | Sample |
|---|---:|
| SM clock | 300 MHz |
| GPU temperature | 37 C |
| GPU power | Approximately 13.622–

The conversation established that idle telemetry was observed and
that the compute workload ran. It did not establish a complete
captured side-by-side DCGM and nvidia-smi output during the workload.

## 16. Completed work

- Installed DCGM 4.7.0.
- Verified DCGM command-line tools.
- Started the DCGM Host Engine.
- Discovered one active Tesla T4.
- Enabled health monitoring.
- Enabled process statistics watches.
- Enabled GPU persistence mode.
- Passed Level 1 diagnostics after the persistence-mode correction.
- Observed idle GPU clock, temperature, power, and utilization.
- Ran a PyTorch matrix-multiplication workload.
- Observed approximately 2.76 GiB of PyTorch GPU memory usage.

## 17. Remaining work

- Capture DCGM telemetry during active GPU compute.
- Compare DCGM metrics with nvidia-smi under load.
- Explore additional DCGM fields and process statistics.
- Install DCGM Exporter.
- Integrate GPU metrics with Prometheus and Grafana.
- Continue Kubernetes GPU observability exercises.

## 18. Evidence provenance

This report records historical observations shared during the lab.
It is not a verbatim transcript of every command or every output.

Use the timestamped `current-session-*.log` file for fresh results
from the environment in which the capture script is executed.
