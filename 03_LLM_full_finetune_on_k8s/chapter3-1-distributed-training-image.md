# Build distributed traininge image

最後，我們將實作一個 [Pytorch FSDP](https://pytorch.org/tutorials/intermediate/FSDP_adavnced_tutorial.html) 的分散式訓練方法在已經建立好的 Cluster 內。

先到 AWS EC2，將機器 Worker Node 都改成有 GPU 的 Instance，我是使用 NVIDIA A10G 24GB GPU Memory，如果有更多錢可以開更大更快的 GPU Instance。但這裡只是為了串通好訓練流程，當訓練流程串通好後，未來無論模型多大，甚至到 175B 以上，都可以透過增加 Worker Node 或是加大 Worker Node 的機器大小來處理。

## Pytorch FSDP

FSDP 的核心概念就是將一個龐大模型內的參數切片分給多個 GPU，這樣就不需要在乎單個 GPU 大小，無論模型參數多大，只需要透過 GPU 擴增的方式都能進行訓練。想像一個模型內的參數都被均勻分組，每一組丟給一個 GPU 去跑訓練，大幅降低 GPU Memory 的消耗。

#### Forward 

在模型跑 Forward Function 時，

#### Backward

- rank
- policy


## Distributed Training


### Data Preparation


### Model Parallel Training Pipeline


## Build Image



