# K8s Cluster on AWS EC2

在 [chapter1-ec2-setup](/02_environment_setup/chapter1-ec2-setup.md) 中起好 EC2 後，就可以開始進行 K8s 的集群設定。

## Command line tool

以下會先介紹三個常見的 command line 工具，每個工具的使用層級不同。

後續在建置集群的時候，會常使用到此三個指令，因此只要看是使用哪個指令，就可以知道對應要操作的層級。

### kubeadm

kubeadm 為**集群整體**的管理工具，用來快速搭建 K8s 集群，它簡化了集群安裝和配置過程中的許多手動操作。基本上建起來後就會比較少使用 kubeadm。

但因為是集群整體的工具，所以未來整個集群要重新啟用，或是有新的 Node 要加入集群，或集群升級，都還是會需要 kubeadm。

同時也藉由 kubeadm 生成相關配置檔案和開啟集群所需的一些元件。

### kubectl

kubectl 為**集群內部**的管理工具。和[上一章](/01_kubernetes_introduction/chapter2-component-details.md)介紹的一致，使用者用此指令會直接打到 kube-apiserver。

而 kube-apiserver 就是作為整個集群的資訊中心，大部分元件都會監聽此元件，並且也是對 etcd 的唯一窗口，因此可以做**集群內部**的管控。

比如創建、查看、更新、刪除 Pods、Services、Deployments 等資源。

若不熟悉集群內部操作，可以看[上一章](/01_kubernetes_introduction/chapter2-component-details.md)的介紹。

### kubelet

kubelet 為 **Worker Node 的管理工具**。一樣在[上一章](/01_kubernetes_introduction/chapter2-component-details.md)有介紹。

kubelet 是每個 Worker Node 都有的元件，主要會監聽 kube-apiserver，並且對自己的 Node 進行管控。

因此未來如果要進入特定的 Node 重啟或是查看 Node 內的 Pod 運行狀況等等，都可以用此指令來看。

## Cluster Setup

### Rename host (Optional)

目前我們有三台 EC2 機器，但預設情況下，比較難區分哪台機器的任務是什麼，後續在建置可能會困惑。

首先輪流進去三台機器，把原本裸露在外的 Private IP，改成所屬的類別，使用以下指令：

```sh
sudo hostnamectl set-hostname control-plane
```

之後重新連進去即可（記得把`control-plane`替換成你想要的對應名稱），改完後顯示這樣就代表成功。

![alt text](image-5.png)

### Preparation Work

#### 1. Turn off swap

正常的系統，可能會使用 Swap memory 的內存管理技術，也就是系統將不常用的 RAM 轉到硬碟的技術，這樣可以解決 RAM 不夠的問題，只是常這樣做會讓效率變慢（硬碟讀寫慢很多）。

而 Kubernetes 的 kubelet 預設情況下**不支援在節點啟用 Swap 的情況下運行**。因為 Kubernetes **希望能夠準確判斷和管理節點上的資源分配和利用**。如果允許 Swap，被調度到該節點的容器可能會因 Swap 而遭受性能問題，從而影響應用程式的運行。

所以當系統啟用了 Swap 時，**kubelet 將不會啟動**，這是一種防範措施。這樣可以確保所有正在運行的 Pod 都是基於可靠的記憶體配置，而不是依賴 Swap。

因此要先到每個節點跑以下指令：

```sh
sudo swapoff -a
```

`swapoff` 就是禁用特定的儲存區塊，`-a` 的 a 就是 all，也就是所有交換區都禁用。


### Container Runtime Installation




### Kubernetes Command Line Tool Installation






