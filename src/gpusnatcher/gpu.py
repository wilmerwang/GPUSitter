import os
import subprocess


def query_gpu() -> list[dict[str, int]] | None:
    """Query GPU information.

    Returns:
        list[dict[str, int]] | None: A list of dictionaries containing GPU information, or None if querying fails.
        Each dictionary contains:
            - index (int): GPU index
            - memory.free (int): Free memory in MiB
            - memory.total (int): Total memory in MiB
    """
    qargs = ["index", "memory.free", "memory.total"]
    cmd = ["nvidia-smi", f"--query-gpu={','.join(qargs)}", "--format=csv,noheader,nounits"]
    try:
        output = subprocess.check_output(cmd, encoding="utf-8")  # noqa: S603
    except Exception as e:
        raise RuntimeError("Failed to query GPU:") from e

    results = [line.strip().split(", ") for line in output.strip().split("\n")]

    return [dict(zip(qargs, map(int, r), strict=False)) for r in results]


def get_gpu_count() -> int:
    """Get the number of GPUs."""
    try:
        result = subprocess.run(
            ["nvidia-smi", "--list-gpus"],  # noqa: S607
            capture_output=True,
            text=True,
            check=True,
        )
        gpus = result.stdout.strip().split("\n")
        return len(gpus)
    except FileNotFoundError:
        return 0
    except subprocess.CalledProcessError:
        return 0


class GPUManager:
    """A class to manage GPU selection based on memory availability."""

    def __init__(self, num_gpus: int, gpu_free_memory_ratio_threshold: float = 0.85) -> None:
        """Initialize the GPU manager.

        Args:
            num_gpus (int): The number of GPUs to manage.
            gpu_free_memory_ratio_threshold (float): The threshold for the free memory ratio to consider a GPU as free.
        """
        self.num_gpus = self.get_num_gpus(num_gpus)
        self.gpu_free_memory_ratio_threshold = gpu_free_memory_ratio_threshold

        self.snatched_gpus: list = []

        self._gpu_maps: dict[int, int] | None = None

    def get_free_gpus(self) -> list[dict[str, int] | None]:
        """Get a list of free GPUs.

        Returns:
            list[dict[str, int] | None]: A list of dictionaries containing information about free GPUs.
        """
        gpus = query_gpu()
        if gpus is None:
            return []

        gpus = self.get_visible_gpus(gpus)

        return [gpu for gpu in gpus if gpu["memory.free"] / gpu["memory.total"] > self.gpu_free_memory_ratio_threshold]

    def get_num_gpus(self, num_gpus: int) -> int:
        """Get the number of GPUs to use."""
        gpu_counts = get_gpu_count()

        if num_gpus == -1 or num_gpus > gpu_counts:
            return gpu_counts
        if num_gpus < 0:
            raise ValueError("num_gpus must be -1 or a non-negative integer.")
        return num_gpus

    @property
    def num_snatched_gpus(self) -> int:
        """Get the number of snatched GPUs."""
        return len(self.snatched_gpus)

    @property
    def gpu_maps(self) -> dict[int, int] | None:
        """Get the GPU mapping."""
        return self._gpu_maps

    @gpu_maps.setter
    def gpu_maps(self, value: dict[int, int] | None) -> None:
        """Set the GPU mapping."""
        self._gpu_maps = value

    def get_num_gpus_needed(self) -> int:
        """Get the number of GPUs still needed to snatch.

        Returns:
            int: Number of GPUs still needed.
        """
        return max(self.num_gpus - self.num_snatched_gpus, 0)

    def get_visible_gpus(self, gpus: list[dict[str, int]] | None) -> list[dict[str, int]] | None:
        """Filter GPUs based on the CUDA_VISIBLE_DEVICES environment variable."""
        cuda_visible = os.environ.get("CUDA_VISIBLE_DEVICES")
        if cuda_visible is None:
            return gpus

        visible_gpus = [gpu for gpu in gpus if gpu["index"] in map(int, cuda_visible.split(","))]
        self.gpu_maps = {gpu["index"]: i for i, gpu in enumerate(visible_gpus)}

        return visible_gpus
