# DCGM Lab —
dcgmi discovery --list
```
Purpose: Show GPUs and supported hardware discovered by DCGM.

Observed: 1 active Tesla T4.

## F. Health

### Commands
```bash
dcgmi health -s a
dcgmi health -c
```
Purpose: Enable health-watch groups and check current health.

Observed: Health monitor configured; overall health Healthy.

## G. Process watches

### Command
```bash
dcgmi stats -e
```
Purpose: Enable DCGM process watches.

Observed: Successfully started process watches.

## H. Persistence mode

### Incorrect command
```bash
nvidia-smi -o 0 -pm 1
```
Result: Failed due to an invalid option for this operation.

### Correct command
```bash
nvidia-smi -i 0 -pm 1
```
Purpose: Enable persistence mode on GPU 0.

Observed: Legacy persistence mode enabled.

## I. Diagnostics

### Command
```bash
dcgmi diag -r 1
```
Purpose: Run a Level 1 diagnostic.

Observed first run: Failed because persistence mode was disabled.

Observed after enabling persistence mode:
```text
software Pass
GPU0: Pass
```

## J. Live DCGM monitoring

### Command
```bash
dcgmi dmon -e 100,150,155,203,204
```
Purpose: Observe selected DCGM telemetry fields.

Observed while idle:
- SM clock around 300 MHz.
- Temperature around 37 C.
- Power around 13.6–
### Command
```bash
nvidia-smi dmon -s pucm -d 1
```
Purpose: Display NVIDIA GPU utilization, power, clock, and memory
telemetry at one-second intervals. Exact output from an active
workload comparison was not captured in the historical evidence.

## L. GPU workload

Observed workload configuration:
- PyTorch matrix multiplication.
- Matrix dimensions 8192 x 8192.
- Approximately 2.76 GiB PyTorch GPU memory.
- 200 iterations in approximately 73 seconds.
- No OOM observed.
- Manually stopped using Ctrl+C.

## M. Useful checks for future sessions

```bash
nvidia-smi
nvidia-smi --query-gpu=index,name,driver_version,memory.total,persistence_mode --format=csv
dcgmi --version
dcgmi discovery --list
dcgmi health -s a
dcgmi health -c
dcgmi stats -e
dcgmi diag -r 1
dcgmi dmon -e 100,150,155,203,204
nvidia-smi dmon -s pucm -d 1
```

Note: The historical observations above are not a substitute for
capturing fresh output from a live GPU environment.
