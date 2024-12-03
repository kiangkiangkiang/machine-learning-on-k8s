# Copyright (c) Meta Platforms, Inc. and affiliates.
# This software may be used and distributed according to the terms of the Llama 2 Community License Agreement.

from dataclasses import dataclass


@dataclass
class train_config:
    seed: int = 42

    # model related
    model_name: str="model-7b"
    quantization: bool = False # load_in_4bit or load_in_8bit; tentatively 4bit
    use_fp16: bool=False
    # full finetuning related use if not using PEFT
    freeze_layers: bool = False
    num_freeze_layers: int = 1

    # PEFT related
    use_peft: bool=False
    peft_method: str = "lora" # None , llama_adapter, prefix

    # dataset related
    dataset: str="samsum_dataset"
    dataset_path: str= "dataset"
    split_slice: str=None # use to limit dataset size to prevent oom; 10 for 10 samples in split or 10% for 10% of samples in split
    batching_strategy: str="padding" #alternative: packing
    context_length: int=4096 #specific to packing
    num_workers_dataloader: int = 1

    # training related
    batch_size_training: int=1
    gradient_accumulation_steps: int=4
    num_epochs: int=3
    lr: float=1e-4 # for SGD and AdamW
    momentum: float=0.9 # for SGD
    weight_decay: float=0.0  # for AdamW
    gamma: float= 0.85  # for StepLR
    run_validation: bool=True
    val_batch_size: int=1
    save_model: bool = False
    output_dir: str = "outputs"

    # FDSP related
    enable_fsdp: bool=False
    low_cpu_fsdp: bool=False
    mixed_precision: bool = True
    dist_checkpoint_root_folder: str="outputs" # will be used if using FSDP
    dist_checkpoint_folder: str="checkpoint" # will be used if using FSDP
    save_optimizer: bool=False # will be used if using FSDP
    use_fast_kernels: bool = False # Enable using SDPA from PyTroch Accelerated Transformers, make use Flash Attention and Xformer memory-efficient kernels
