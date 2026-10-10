
cat > scripts/setup-python-env.sh <<'BASH'
#!/usr/bin/env bash

# Create an isolated Python environment for the GPU workload.
set -euo pipefail

LAB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${LAB_DIR}"

echo "=== Python environment setup ==="

# Check for Python 3.
if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: python3 is not installed."
    exit 1
fi

python3 --version

# Create a virtual environment if one does not exist.
if [[ ! -x .venv/bin/python ]]; then
    python3 -m venv .venv
fi

# Activate the isolated environment.
source .venv/bin/activate

# Update pip and install the project dependencies.
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo
echo "=== Verify PyTorch and CUDA ==="

python - <<'PY'
import torch

print("PyTorch version:", torch.__version__)
print("PyTorch CUDA build:", torch.version.cuda)
print("CUDA available:", torch.cuda.is_available())

if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
    print(
        "GPU memory:",
        f"{torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GiB",
    )
else:
    print("WARNING: PyTorch cannot access a CUDA GPU in this environment.")
PY

echo
echo "Environment setup finished."
echo "Activate it with: source .venv/bin/activate"
BASH

chmod +x scripts/setup-python-env.sh

