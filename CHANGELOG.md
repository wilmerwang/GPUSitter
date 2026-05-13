## v2.1.1 (2026-05-13)

## v2.1.0 (2025-09-17)

### Feat

- add server information in the email notification

### Fix

- prevent gpust from hanging when job requests more GPUs than available

## v2.0.4 (2025-09-15)

### Fix

- prevent CUDA_VISIBLE_DEVICES env in tmux

## v2.0.3 (2025-09-15)

### Fix

- prevent NoneType error when updating status in debug mode

### Refactor

- **gpu**: using pynvml instead of "nvidia-smi" to query gpus
- update the spinner when friendly sleep is end

## v2.0.2 (2025-09-13)

### Refactor

- update the spinner

## v2.0.1 (2025-09-13)

### Fix

- there has not extra group in uv sync in ci

## v2.0.0 (2025-09-13)

### Feat

- version 2.0.0 for real job running
- add tmux support
- remove stdout and stderr from jobs
- **config**: allow friendly_min to accept float values
- add max_retry support
- using jobs instead of fake tasks
- remove the property related to gpu number
- remove gpu_nums and gpu_tims_min from config

### Fix

- change sender name to GPUSitter
- ensure job is start or not
- using cmd_list instead of cmd_str

## v1.8.1 (2025-09-12)

### Fix

- uncomment previously commented code

## v1.8.0 (2025-09-11)

### Feat

- **config**: add prompt when config file do not contains some necessary keys
- **debug**: add debug support

### Fix

- cuda index error when using CUDA_VISIBLE_DEVICES env

## v1.7.0 (2025-09-11)

### Refactor

- move None check outside function

## v1.6.0 (2025-09-10)

### Feat

- **gpu**: add CUDA_VISIBLE_DEVICES support

### Fix

- the config test cannot works

## v1.5.0 (2025-09-07)

### Feat

- add args of friendly_min to avoid OOM from previous job's final test/cleanup

## v1.4.0 (2025-09-03)

### Feat

- add spinner in the processing of snatching gpus

## v1.3.2 (2025-09-03)

### Fix

- The snatched gpu index is error in Notifications
- counts error of snatchered gpu if worker not works

### Refactor

- simulation task for gpu

## v1.3.0 (2025-09-02)

### Feat

- to simulate fluctuating GPU utilization

## v1.2.2 (2025-09-02)

### Fix

- change the threshold ratio of free/total memory (0.10 -> 0.85)

## v1.2.1 (2025-09-02)

## v1.2.0 (2025-09-02)

## v1.1.1 (2025-09-02)

### Fix

- only run ci in main branch & remove CHANGE LOG in publish

## v1.1.0 (2025-09-02)

### Feat

- add spinner for waiting time
- toy version
- process email_pwd
- add config module

### Fix

- can not use nvidia-smi in github actions
- the index name of torch
- response error from email
