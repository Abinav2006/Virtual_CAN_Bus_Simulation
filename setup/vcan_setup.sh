#!/usr/bin/env bash

set -euo pipefail

INTERFACE="${1:-vcan0}"

echo "[INFO] Loading vcan kernel module..."

if ! lsmod | grep -q '^vcan'; then
    sudo modprobe vcan
fi

echo "[INFO] Creating ${INTERFACE}..."

if ip link show "${INTERFACE}" >/dev/null 2>&1; then
    echo "[INFO] ${INTERFACE} already exists."
else
    sudo ip link add dev "${INTERFACE}" type vcan
fi

echo "[INFO] Bringing ${INTERFACE} up..."

sudo ip link set up "${INTERFACE}"

echo
echo "[INFO] CAN interface status:"
ip -details link show "${INTERFACE}"
