# GPUSitter

Watch for idle GPUs and run your jobs: launches jobs in tmux, keeps logs/status and sends start/finish emails..

## Features

- Real-time GPU usage monitoring
- Command-line interface, easy to integrate into workflows
- Email notifications
- Scheduled automatic job running

## Dependencies

- tmux

## Installation

```
pip install gpusitter
```

## Usage

> [!IMPORTANT]
> Make sure the job environment (especially the Python environment) is correctly set up before running `gpust`. There are two common ways to do this:
>
> 1. Activate your environment before running `gpust`. e.g. `conda activate xxx`, `source .venv/bin/activate`. (If you are using uv
>    to manage environments, you can also run: `uv run gpust`)
> 2. Specify the Python path directly in the job command, e.g. `gpust --job="~/myproject/.venv/bin/python train.py"`

```bash
# One job with 1 gpu
gpust --job="python train.py"

# One job with 4 gpus
gpust --job="python train.py:4"

# Two jobs with 1 gpu and 4 gpus respectively
gpust --job="python train.py" --job="python train.py --epoch=12 --lr=-.001:4"

# With CUDA_VISIBLE_DEVICES env
CUDA_VISIBLE_DEVICES=2 gpust --job="python train.py"

# With different python envs
gpust --job="~/job1/.venv/bin/python train1.py" --job="~/job2/.venv/bin/python train2.py"
```

After starting your job, you can monitor its progress using `tmux`.

```bash
# List all running tmux sessions
tmux ls

# Attach to your job session (replace GPUSitter_xxx_xx with your session name)
tmux a -t GPUSitter_xxx_xx
```

Parameter description:

```
class ConfigData:
    """Configuration data for GPU Snatcher."""

    gpu_free_memory_ratio_threshold: float
    friendly_min: float
    email_host: str
    email_user: str
    email_pwd: str
    email_sender: str
    email_receivers: list[str]
```

- gpu_free_memory_ratio_threshold: The minimum free GPU memory ratio required to consider a GPU available. Only GPUs with free memory above this threshold will be used.
- friendly_min: Waiting time (in seconds) before allocating GPUs. Helps prevent OOM from previous jobs.
- email_host: Email server, e.g., smtp.qq.com
- email_user: Email address
- email_pwd: SMTP authorization code
- email_sender: Sender
- email_receivers: Recipients

# Contribution

Issues and pull requests are welcome. Please follow the project's code style guidelines.

# License

This project is licensed under the MIT License.
