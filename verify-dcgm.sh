#!/usr/bin/env bash

set -euo pipefail

echo "========================================"
echo " DCGM Verification"
echo "========================================"

echo
echo "=== DCGM Version ==="
dcgmi --version

echo
echo "=== NVIDIA GPU ==="
nvidia-smi

echo
echo "=== DCGM Discovery ==="
dcgmi discovery --list

echo
echo "=== DCGM Health ==="
dcgmi health -s a
dcgmi health -c

echo
echo "=== DCGM Process Statistics ==="
dcgmi stats -e

echo
echo "=== DCGM Diagnostic Level 1 ==="
dcgmi diag -r 1

echo
echo "========================================"
echo " Verification complete"
echo "========================================"
