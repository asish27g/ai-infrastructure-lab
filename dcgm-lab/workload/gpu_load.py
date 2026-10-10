#!/usr/bin/env python3

# ============================================================
# GPU Compute and Memory Workload
# Purpose: Generate GPU activity for NVIDIA DCGM telemetry
# ============================================================

import argparse
import time

import torch


# ------------------------------------------------------------
# 1. Parse command-line arguments
# ------------------------------------------------------------
parser = argparse.ArgumentParser(
    description="GPU compute and memory workload for DCGM monitoring"
)

# Duration of the workload in seconds
parser.add_argument("--seconds", type=int, default=120)

# Matrix dimension: 8192 means an 8192 x 8192 matrix
parser.add_argument("--size", type=int, default=8192)

# Additional GPU tensor memory to allocate, in GiB
parser.add_argument("--memory-gb", type=float, default=2.0)

args = parser.parse_args()


# ------------------------------------------------------------
# 2. Validate input arguments
# ------------------------------------------------------------
if args.seconds <= 0:
    parser.error("--seconds must be greater than zero")

if args.size <= 0:
    parser.error("--size must be greater than zero")

if args.memory_gb < 0:
    parser.error("--memory-gb cannot be negative")


# ------------------------------------------------------------
# 3. Verify CUDA availability
# ------------------------------------------------------------
if not torch.cuda.is_available():
    raise SystemExit(
        "CUDA is unavailable. Check nvidia-smi and your PyTorch installation."
    )

# Select the first CUDA GPU
device = "cuda:0"

# Read GPU properties
props = torch.cuda.get_device_properties(0)

print("=" * 60, flush=True)
print("GPU WORKLOAD STARTING", flush=True)
print("=" * 60, flush=True)

print(f"GPU: {props.name}", flush=True)
print(f"VRAM: {props.total_memory / 1024**3:.1f} GiB", flush=True)
print(f"Matrix size: {args.size} x {args.size}", flush=True)
print(f"Target duration: {args.seconds} seconds", flush=True)


# ------------------------------------------------------------
# 4. Allocate matrices for compute-intensive operations
# ------------------------------------------------------------
# Float32 matrices use approximately 4 bytes per element.
# Three N x N matrices require approximately 12 * N * N bytes.
n = args.size

print("Allocating GPU matrices...", flush=True)

a = torch.randn(
    (n, n), device=device, dtype=torch.float32
)

b = torch.randn(
    (n, n), device=device, dtype=torch.float32
)

c = torch.empty_like(a)


# ------------------------------------------------------------
# 5. Allocate additional GPU memory in 64 MiB chunks
# ------------------------------------------------------------
# Each float32 element uses 4 bytes.
# 16,777,216 elements x 4 bytes = 64 MiB per chunk.
chunk_elements = 16 * 1024 * 1024
chunk_bytes = chunk_elements * 4

# Round down to whole chunks, preserving the original workload logic.
# At least one chunk is allocated, even if --memory-gb is zero.
num_chunks = max(
    1,
    int(args.memory_gb * 1024**3 / chunk_bytes)
)

print(
    f"Allocating {num_chunks} additional memory chunks...",
    flush=True,
)

chunks = [
    torch.ones(
        chunk_elements,
        device=device,
        dtype=torch.float32
    )
    for _ in range(num_chunks)
]

# Wait for queued GPU operations to finish before timing.
torch.cuda.synchronize()

print(
    f"Additional tensor allocation: approximately "
    f"{num_chunks * 64} MiB",
    flush=True,
)

print(
    f"PyTorch allocated GPU memory: "
    f"{torch.cuda.memory_allocated() / 1024**3:.2f} GiB",
    flush=True,
)


# ------------------------------------------------------------
# 6. Execute compute and memory operations
# ------------------------------------------------------------
# Matrix multiplication exercises GPU compute resources.
# Repeated tensor updates generate additional memory traffic.
#
# The duration is a target. An iteration already in progress
# may finish after the target time has elapsed.
start = time.monotonic()
iterations = 0

print(
    f"Running for up to {args.seconds} seconds. "
    "Press Ctrl+C to stop.",
    flush=True,
)

try:
    while time.monotonic() - start < args.seconds:

        # Compute-intensive phase: matrix multiplication
        torch.mm(a, b, out=c)

        # Memory-intensive phase: update every additional tensor
        for tensor in chunks:
            tensor.mul_(1.000001).add_(0.000001)

        iterations += 1

        # Report progress every five iterations
        if iterations % 5 == 0:

            # Synchronize so elapsed time and memory readings
            # reflect completed GPU work.
            torch.cuda.synchronize()

            elapsed = time.monotonic() - start

            # Memory allocated by PyTorch, not total device usage
            allocated = torch.cuda.memory_allocated() / 1024**3

            # Report progress for correlation with DCGM telemetry
            print(
                f"Elapsed={elapsed:.1f}s | "
                f"Iterations={iterations} | "
                f"PyTorch GPU memory={allocated:.2f} GiB",
                flush=True,
            )

except KeyboardInterrupt:
    # Allow the user to stop the workload with Ctrl+C
    print("Stopping workload...", flush=True)


# ------------------------------------------------------------
# 7. Synchronize and report final results
# ------------------------------------------------------------
# Wait for outstanding GPU operations to finish.
torch.cuda.synchronize()

elapsed = time.monotonic() - start

print("=" * 60, flush=True)
print("GPU WORKLOAD FINISHED", flush=True)
print("=" * 60, flush=True)

print(f"Elapsed time: {elapsed:.1f} seconds", flush=True)
print(f"Total iterations: {iterations}", flush=True)

print(
    f"Final PyTorch GPU memory allocated: "
    f"{torch.cuda.memory_allocated() / 1024**3:.2f} GiB",
    flush=True,
)

# Display PyTorch CUDA allocator statistics.
# These statistics do not represent all GPU memory consumers.
print("\nPyTorch GPU memory summary:", flush=True)

print(
    torch.cuda.memory_summary(
        device=device,
        abbreviated=True
    ),
    flush=True,
)
