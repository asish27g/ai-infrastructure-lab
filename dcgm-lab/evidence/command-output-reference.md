# DCGM Lab — Command Reference and Observations

## E. GPU Discovery

### Command

```bash
dcgmi discovery --list
```

**Purpose:** Show GPUs and supported hardware discovered by DCGM.

**Observed:** One active NVIDIA Tesla T4 GPU.

## F. Health

### Commands

```bash
dcgmi health -s a
dcgmi health -c
```

**Purpose:** Enable health-watch groups and check current GPU health.

**Observed:** Health monitoring configured successfully; overall health reported as `Healthy`.

## G. Process Watches

### Command

```bash
dcgmi stats -e
```

**Purpose:** Enable DCGM process statistics watches.

**Observed:** Process watches started successfully.

## H. Persistence Mode

### Incorrect Command

```bash
nvidia-smi -o 0 -pm 1
```

**Result:** Failed because the command used an invalid option for this operation.

### Correct Command

```bash
nvidia-smi -i 0 -pm 1
```

**Purpose:** Enable persistence mode on GPU 0.

**Observed:** Legacy persistence mode enabled successfully.

## I. Diagnostics

### Command

```bash
dcgmi diag -r 1
```

**Purpose:** Run a Level 1 DCGM diagnostic.

**Observed — First Run:** Failed because persistence mode was disabled.

**Observed — After Enabling Persistence Mode:**

```text
software Pass
GPU0: Pass
```

## J. Live DCGM Monitoring

### Command

```bash
dcgmi dmon -e 100,150,155,203,204
```

**Purpose:** Observe selected DCGM telemetry fields.

**Observed While Idle:**

- SM clock: approximately 300 MHz.
- Temperature: approximately 37 °C.
- Power consumption: approximately 13.6–13.8 W.
- GPU utilization: 0%.
- Memory utilization: 0%.

These values are historical observations from the idle monitoring session.

## K. NVIDIA-SMI Monitoring

### Command

```bash
nvidia-smi dmon -s pucm -d 1
```

**Purpose:** Display NVIDIA GPU power, utilization, clock, and memory telemetry at one-second intervals.

**Observation:** A complete, simultaneous comparison between DCGM and NVIDIA-SMI during an active workload was not captured in the historical evidence.

## L. GPU Workload

**Workload:** PyTorch matrix multiplication.

**Observed Configuration and Results:**

- Matrix dimensions: 8192 × 8192.
- PyTorch GPU memory allocation: approximately 2.76 GiB.
- Completed iterations: 200.
- Elapsed time: approximately 73 seconds.
- Out-of-memory (OOM) error: None observed.
- Execution: Manually stopped with `Ctrl+C` before the configured 120-second duration.

These results describe the recorded workload run, not a standardized performance benchmark.

## M. Useful Commands for Future Sessions

### GPU and Driver Information

```bash
nvidia-smi

nvidia-smi --query-gpu=index,name,driver_version,memory.total,persistence_mode \
  --format=csv
```

### DCGM Version and Discovery

```bash
dcgmi version
dcgmi discovery --list
```

### Health and Process Monitoring

```bash
dcgmi health -s a
dcgmi health -c
dcgmi stats -e
```

### Diagnostics

```bash
dcgmi diag -r 1
```

### DCGM Telemetry

```bash
dcgmi dmon -e 100,150,155,203,204
```

### NVIDIA-SMI Telemetry

```bash
nvidia-smi dmon -s pucm -d 1
```

## Notes and Limitations

- Historical observations document results from a previous experiment; they do not guarantee current system behavior.
- Capture fresh command output when repeating an experiment.
- To validate GPU behavior under load, run telemetry monitoring concurrently with the workload and retain both outputs.
- Compare DCGM and NVIDIA-SMI results only when the measurements correspond to comparable time periods and supported metrics.
