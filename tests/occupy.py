"""GPU occupy script.

Features
--------
1. Accept arbitrary CLI args (ignored internally).
2. Detect free GPU memory via pynvml.
3. Occupy ~90% of free VRAM.
4. Run continuous CUDA compute to simulate a real training workload.
5. Automatically stop after a specified duration.

Example:
-------
python occupy.py \
    --config xxx.yaml \
    trainer.devices=0 \
    model.hidden=256 \
    --duration 0.5

The script ignores all unknown args except:
    --duration
    --gpu
    --ratio
"""

from __future__ import annotations

import argparse
import signal
import sys
import time

import torch
from pynvml import (
    nvmlDeviceGetHandleByIndex,
    nvmlDeviceGetMemoryInfo,
    nvmlDeviceGetName,
    nvmlInit,
)


def parse_args() -> argparse.Namespace:
    """Parse known args and ignore all others."""
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument("--gpu", type=int, default=0)
    parser.add_argument("--duration", type=float, default=0.5)
    parser.add_argument("--ratio", type=float, default=0.9)

    # Ignore all unknown args
    args, _ = parser.parse_known_args()

    return args


def get_free_memory_bytes(gpu_id: int) -> int:
    """Get free GPU memory in bytes."""
    nvmlInit()

    handle = nvmlDeviceGetHandleByIndex(gpu_id)
    info = nvmlDeviceGetMemoryInfo(handle)

    gpu_name = nvmlDeviceGetName(handle)

    print(f"[INFO] GPU: {gpu_name}")
    print(f"[INFO] Free memory: {info.free / 1024**3:.2f} GB")

    return info.free


def allocate_memory(gpu_id: int, ratio: float) -> torch.Tensor:
    """Allocate target amount of GPU memory."""
    free_mem = get_free_memory_bytes(gpu_id)

    target_bytes = int(free_mem * ratio)

    # float32 => 4 bytes
    num_elements = target_bytes // 4

    print(f"[INFO] Allocating ~{target_bytes / 1024**3:.2f} GB")

    device = torch.device(f"cuda:{gpu_id}")

    tensor = torch.empty(
        num_elements,
        dtype=torch.float32,
        device=device,
    )

    print("[INFO] Allocation complete")

    return tensor


def run_fake_training_loop(
    occupied_tensor: torch.Tensor,
    duration: int,
) -> None:
    """Run continuous CUDA compute."""
    device = occupied_tensor.device

    # Small compute tensors
    a = torch.randn((4096, 4096), device=device)
    b = torch.randn((4096, 4096), device=device)

    end_time = time.time() + int(duration * 3600)

    step = 0

    print(f"[INFO] Running fake workload for {duration} seconds")

    while time.time() < end_time:
        # Heavy CUDA ops
        c = torch.matmul(a, b)

        # Prevent optimization
        c = torch.relu(c)

        # Sync to ensure actual compute
        torch.cuda.synchronize(device)

        step += 1

        if step % 500 == 0:
            remaining = int(end_time - time.time())

            allocated = torch.cuda.memory_allocated(device) / 1024**3

            print(f"[INFO] step={step} allocated={allocated:.2f}GB remaining={remaining}s")

    print("[INFO] Finished")


def main() -> None:
    """Main."""
    args = parse_args()

    torch.cuda.set_device(args.gpu)

    print(f"[INFO] Using cuda:{args.gpu}")

    occupied_tensor = allocate_memory(
        gpu_id=args.gpu,
        ratio=args.ratio,
    )

    def cleanup(*_) -> None:
        print("\n[INFO] Cleaning up")

        torch.cuda.empty_cache()

        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    run_fake_training_loop(
        occupied_tensor=occupied_tensor,
        duration=args.duration,
    )


if __name__ == "__main__":
    main()
