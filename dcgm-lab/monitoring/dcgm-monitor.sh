#!/usr/bin/env bash

set -euo pipefail

echo "Starting DCGM live GPU monitoring..."
echo
echo "Press Ctrl+C to stop."
echo

dcgmi dmon -e 100,150,155,203,204
