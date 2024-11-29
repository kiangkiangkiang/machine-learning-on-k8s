# Distributed LLM Training on Kubernetes

Welcome to the Distributed LLM (Large Language Model) Training on Kubernetes project! 

This repository provides guides and examples for setting up Kubernetes and deploying distributed LLM training workflows (**mostly in chinese**). 

It is structured to facilitate easy understanding and implementation even for those new to specific technologies.


### Introduction

In this project, you will find detailed instructions and deploying distributed training of Large Language Models using Kubernetes. 

The project is divided into three main sections, each with its own documentation, covering **Kubernetes basics**, **manual setup**, and **practical implementation of distributed LLM training**.


### Prerequisites

Before you begin, ensure you have the following:

- **Basic Docker Knowledge**: Understanding Docker images, containers, and network.
- **AWS Basics**: Some familiarity with AWS services is beneficial, although not required.
- **Machine Learning Knowledge**: Transformers. Training Step. Fowrward/Backward Concepts.

## Folder Structure

```plaintext
├── 01_kubernetes_introduction/
│   └── chapter1-1-basic-concept.md        - Why we use Kubernetes.
│   └── chapter1-2-component-details.md    - Concepts and components of Kubernetes.
│
├── 02_environment_setup/
│   └── chapter2-1-ec2-setup.md            - Step-by-step guide to manually set up AWS EC2 environment.
│   └── chapter2-2-kubernetes-setup.md     - Step-by-step guide to manually set up a Kubernetes environment.
│   └── chapter2-3-developer-setup.md      - Step-by-step guide to manually set up a developer environment.
│
└── 03_LLM_full_finetune_on_k8s/
    └── chapter3-1-simple-test.md          - Toy API for cluster network testing.
    └── chapter3-2-training-llm-on-k8s.md  - Implementation guide and scripts for distributed LLM training on Kubernetes.
```

## Reference
- https://www.omniwaresoft.com.tw/product-news/k8s-introduction/
- https://kubernetes.io/
- https://gist.github.com/kkbruce/c632e946c59f04ea8d7ce20f6f80b26d
- https://github.com/bobcchen/finetuning-exploration/tree/master
- https://mrmaheshrajput.medium.com/deploy-kubernetes-cluster-on-aws-ec2-instances-f3eeca9e95f1
- https://aws.amazon.com/tw/blogs/machine-learning/scale-llms-with-pytorch-2-0-fsdp-on-amazon-eks-part-2/
- https://pytorch.org/blog/efficient-large-scale-training-with-pytorch/
- https://github.com/aws-samples/aws-do-eks/tree/main/Container-Root/eks/deployment/distributed-training/pytorch/pytorchjob/fsdpex