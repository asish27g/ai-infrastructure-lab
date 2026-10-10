#!/usr/bin/env python3

import torch

parser = argparse.ArgumentParser()
parser.add_argument("--seconds", type=int, default=120)
parser.add_argument("--size", type=int, default=8192)
parser.add_argument("--memory-gb", type=float, default=2.0)
args = parser.parse_args()

if not torch.cuda.is_available():
    raise SystemExit("CUDA is unavailable. Check nvidia-smi and PyTorch.")

device = "cuda:0"
props = torch.cuda.get_device_properties(0)

print(f"GPU: {props.name}", flush=True)
print(f"VRAM: {props.total_memory / 1024**3:.1f} GiB", flush=True)
print(f"Matrix size: {args.size} x {args.size}", flush=True)

# Matrix multiplication workload
n = args.size
a = torch.randn((n, n), device=device, dtype=torch.float32)
b = torch.randn((n, n), device=device, dtype=torch.float32)
c = torch.empty_like(a)

# Memory bandwidth workload, allocated in manageable chunks
chunk_elements = 16 * 1024 * 1024  # 64 MiB per chunk
num_chunks = max(1, int(args.memory_gb * 1024**3 / (chunk_elements * 4)))
chunks = [
    torch.ones(chunk_elements, device=device, dtype=torch.float32)
    for _ in range(num_chunks)
]
torch.cuda.synchronize()

print(f"Allocated tensor memory: approximately "
      f"{num_chunks * 64} MiB, plus matrices", flush=True)
print(f"Running for {args.seconds} seconds. Press Ctrl+C to stop.",
      flush=True)

start = time.monotonic()
iterations = 0

try:
    while time.monotonic() - start < args.seconds:
        # Compute-intensive phase
        torch.mm(a, b, out=c)

        # Memory-intensive phase
        for t in chunks:
            t.mul_(1.000001).add_(0.000001)

        iterations += 1

        if iterations % 5 == 0:
            torch.cuda.synchronize()
            elapsed = time.monotonic() - start
            allocated = torch.cuda.memory_allocated() / 1024**3
            print(
                f"Elapsed={elapsed:.1f}s | "
                f"Iterations={iterations} | "
                f"PyTorch GPU memory={allocated:.2f} GiB",
                flush=True,
            )

except KeyboardInterrupt:
    print("Stopping workload...", flush=True)

torch.cuda.synchronize()
print(f"Finished. Total iterations: {iterations}", flush=True)
print(torch.cuda.memory_summary(device=device, abbreviated=True), flush=True)
