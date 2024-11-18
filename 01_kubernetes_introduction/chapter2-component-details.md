# K8s Component

有別於[上一章](chapter1-basic-concept.md)從 K8s 應用情境切入介紹，本章將更著重在實際內部元件的概述。包含介紹上一章提到的 Control Plane、Node 等結構中，內部有什麼組成？彼此間資訊如何傳遞？而在了解這些細節後，未來在實作上會更清楚如何建立一個 Control Plane 以及 Node。

以下為基礎 K8s 架構範例（可能會因為不同服務建置需求而有不同），後續將透過此架構圖進一步說明內部細節。

![alt text](image-1.png)

## 1. Control Plane

Control Plane 內部包含多個元件，每個元間之間透過 kube-apiserver 當作中心點相互溝通，透過以下「新建服務」的例子，來快速瞭解彼此間所扮演的角色以及溝通模式：

通常，在 K8s 內，管理集群資源的指令會使用`kubectl`，而當開發人員使用此指令時，實際上會直接打到 kube-apiserver 內，由 kube-apiserver 處理所有後續的操作。

舉例來說，假設我們已經把 K8s 集群架好，接著要開始把一些微服務配置到 K8s Node 內，因此我們會透過 `kubectl apply -f my_service.yaml` 來把我的服務 (my_service) 推進集群內（注意：使用此指令需要確保發送的機器打得到 kube-apiserver），此時，實際上接收到`kubectl`訊息的是 Control Plane 內部的 kube-apiserver，而會依序進行以下幾件事情：
1. 確認當前使用者是否有足夠權限執行此操作：例如我想起一個 Nginx 服務，kube-apiserver 會檢視我是否有足夠權限起。
2. 假設權限足夠，kube-apiserver 接著會把我寫好的配置 `my_service.yaml` 存到 [etcd](#etcd) 內部，將此配置作為集群的一部分。
3. 同時，因為 [controller-manager](#controller-manager) 持續監聽 kube-apiserver，因此當新的服務要被建置時，controller-manager 會知道「有服務更新了」，此時 controller-manager 會主動打到 kube-apiserver 取得此服務的 Spec，並且建立相對應的資源（Pod or other），甚至建立所需要的硬體規格 (CPU 數量) 等等 。
4. controller-manager 建立好這些規格後，會把這樣的資訊回傳給 kube-apiserver，由 kube-apiserver 寫入 etcd 更新集群狀態。並且此時 kube-apiserver 會得到 controller-manager 來的一個資訊：有新的服務未被部署。
5. 此時，Scheduler 因為持續監聽著 kube-apiserver 的某些事件，因此發現「有新的服務未被部署」時，觸發了 Scheduler 的程式，Scheduler 會主動打到 kube-apiserver 要這些未被部署的服務的資訊（由於 controller-manager 已經將服務都標記上要求的硬體，因此 Scheduler 只需要計算集群內每個 Node 擁有的資源，根據特定策略做分配即可）。
6. 最終 Scheduler 分配完成後，會告訴 kube-apiserver，將這些服務所分配到的 Node 等資訊，寫入 etcd。

### kube-apiserver

由上述範例可知，kube-apiserver 實際上就是在做以下工作：

1. 處理所有打進 Control Plane 的 API 請求。
2. K8s 內部資源管控中心（對 etcd 的唯一入口）：對所有 K8s 資源實現 CRUD 等操作。
3. 身份認證中心：檢視所有打進來的流量（用戶）是否有對應請求資源的權限。

可以想像成整個 K8s 的資訊中心，有任何資訊都可以透過 kube-apiserver 得知，在集群內的所有元件則是會跟 kube-apiserver 用類似「訂閱」的方式，取得特定類型資源的更新狀況，此監聽機制稱作「watch」，只要其他元件有主動 watch apiserver，apiserver 便會將其所關注的資源更新狀況傳遞給該元件。以達到監聽的功用。

舉例來說，kube-apiserver 類似學校的教務處，教務處會把學校的一些資訊放到佈告欄上，每個班級要告訴教務處說「我需要知道哪些資訊」，後續只要那些資訊跟某些班級有相關，教務處就會派人將這些資訊去該班級宣達。後續要如何處理該訊息，就是該班級內部自己決定的事情。

### etcd

分散式系統內最主要的狀態儲存庫，主要儲存以下資訊整個集群的資訊，以及服務相對應的配置資訊，或是每個 Pod 的狀態等資訊。

由先前範例可知，在集群內做操作時，統一透過 kube-apiserver 來像各個元件溝通，因此 kube-apiserver 會知道每個元件間的配置狀況，且將這些資訊統一存到 etcd，未來有需要使用到集群資源分配等問題時，就會由 kube-apiserver 訪問到 etcd。

為何要有 etcd ?

k8s 是一個分散式系統，而當在分散式系統發現有個機器故障了，勢必得修復它，但這台機器是做什麼用，處理哪些任務的，正常情況下沒人知道，所以要有個地方存這些資訊，並且要整個集群內都統一，這樣才不會有的人說要修復成 A 狀態，有的說要修復成 B 狀態，因此 etcd 就是集群內部資訊的統一儲存庫，無論是要更新、修復等，都可以藉由 etcd 來取得最新資訊。

### scheduler

scheduler 主要就是用於調度與排程，最基本的就是當有新建立的 Pod 且未指定 Node 運行時，scheduler 就會根據硬體條件、資料位置、工作負載等各種資訊，將 Pod 調到最適當的 Node。

因此 scheduler 會持續監聽 kube-apiserver (watch)，可以想像成 scheduler 向 apiserver 訂閱了某個特定事件（例如狀態更新的通知），因此當 kube-apiserver 有此狀態更新時，kube-apiserver 會主動向 scheduler 通知，接著 scheduler 再向 apiserver 索要特定狀態資訊，例如當發現此特定狀態資訊是有新建立的 Pod 且未指定 Node 運行時，scheduler 就會向 apiserver 要求此 Pod 資訊。最終根據 scheduler 內部演算法進行 Node 調配。

### controller-manager

管理整個集群的主要邏輯層。

基本上集群內大大小小的管理操作，可能都有一個或多個 controller 在管控。以上述例子來說，使用者有新的資源配置的需求發送到 apiserver，此時 controller-manager 會根據此資源類型，**交給特定的 controller 處理**，並且透過 controller loop 持續監控該類型的資源，監聽到事件發生時，再交由該 controller 做特定處理。而通常 controller loop 內部邏輯會和該資源類型相關，但可以概括成以下幾步驟：

1. 監聽該類型的資源變化。和 scheduler 一樣，通過 watch 機制，controller 主動打開一個持久連接的管道讓 apiserver 能夠藉由這個管道發送更新資訊到 controller 內以達到監聽效果。
2. 取得當前集群狀況。收到更新事件後，controller 會主動打到 apiserver 詢問當前集群內部資源配置狀況。
3. 有了集群資源分配狀況後，就可以跟 1. 所監聽到的使用者所想更新的配置進行比較，看使用者更新的配置是否可以匹配到當前集群的實際資源內。
4. 規劃調整：假設無法匹配，則根據特定的策略調整資源（例如創建或刪除某些其他特定的 Pod 來達到資源匹配）。
5. 執行調整：規劃完後，會開始向 apiserver 要求資源的調整，此時 apiserver 可能就會開始向各個 Node 發送資源調整的請求。
6. 調整完後回到 1.，繼續監聽。

而 controller 並不只處理資源更新的邏輯。也處理各種集群內部的一些特定邏輯。例如資源重啟，自動擴展，安全配置等。

所以可以想像一個 Control Plane 中，有很多個 controller，各自監聽各自想要的資源或任務，並且規劃一系列執行**意圖**，把這些執行意圖交給 kube-apiserver，讓 kube-apiserver 統一發送到各個 Node 的 kubelet 執行（注意：controller 只是告知 apiserver 想要新增或修改的 Pod 訊息，並不是真正的新增修改的指令）。

### cloud-controller-manager (Optional)

和雲平台溝通的節點，主要是 K8s 服務如果有用到雲端資源時，會透過 Cloud Controller Manager 來管控使用雲端的服務（沒用到就不用這個節點）。例如，假設我們建立一個 K8s 服務，其中會使用 AWS LoadBalancer，則就會在此節點管控兩者之間的交互。

## Node

### kubelet

負責管理每個 Node。

例如 kubelet 監聽 kube-apiserver，當有新的資源要分配到該節點時，就是透過 kubelet 將此服務建置起來。

將這些 Pod 建置起來後，kubelet 也會持續監控 Pod 的運行狀況，並且主動回報給 kube-apiserver。而當有 Pod 死掉時，kubelet 也會進行自動重啟（因為他是負責管理 Node 的，所以每個 Pod 的配置都在 kubelet 身上，所以才能根據該配置重啟服務，而通常配置上也可以敘述一些重啟策略等）。並且提供該 Node 上所有 Log 資訊。

通常如果是自動建置集群的話（kubeadm），正常情況下不需要到每個 Node 上跑 kubelet 指令，只有在手動建置時，或是在除錯時，需要真的進入該 Node 進行錯誤盤查。


### container runtime

Kubernetes 是為了編排和管理容器化服務而設計的，因此在 Kubernetes 上運行的每個服務都需要事先被打包成 container，反之，如果你的服務已經是一個 container，那麼可以直接將此 image 配置到 K8s 環境中。

因此 K8s 為了要能運行這些 container，因此要有個底層能夠運行及管理這些 container 的軟體，例如 Docker Engine 就是一個 container runtime。所以在建置 K8s 集群時，要確保每個 Node 都有裝好適當的 container runtime。

而 K8s 內幾個常見的 container runtime 如下：

- containerd
- CRI-O
- Docker Engine
- Mirantis Container Runtime

還有其他就不贅述了，不同 container runtime 還是有些微差異，但只在管理或是效率等方面，若服務不夠龐大，實際上彼此之間的差異並不顯著。

而這些 container runtime 都是 K8s 原生支援的，也就是這些都有開放 container runtime interface (CRI)，kubelet 便是透過此管道向 內部的 container 進行管控，因此安裝完後，只需要配置好其中的設定檔（確保 CRI 有正確啟用），就可以無痛整進 K8s 環境內。

### kube-proxy

分配在每個 Node 上的 Component，主要就是處理流量問題。

例如，某個服務在 Node 1 上的 Pod 3 和 Pod 4（兩個副本），而外部使用者要怎麼打到這兩個服務？

實際上我們會從 K8s 上新建一個 `Services`，用此來宣告哪一個 Node Port 會導向哪一個我們起的 App Port，以上述的例子來說，我們有一個服務開放 30000 port，且複製了兩份，而 `Services` 則需要宣告 Node Port 30000 導向上述服務的 30000 Port（注意：實際上並不會指定 Node，因為正常來說，此服務會到哪個 Node 是自動分配的，所以我們只需要指定 Node Port 如何導向 App Port 就好），這樣無論未來服務被分配到哪個 Node，流量都能正常打入。

而集群內部運行則是，kube-proxy 會持續監聽 kube-apiserver 的 Services，當有新的 Services 時，kube-proxy 會向 kube-apiserver 所要 Services 相關資訊，自動根據我們定義好的配置，自動更新到 kube-proxy 內的 iptables 中。

因此我們只要打某一個 Node IP + Port，實際上就是去訪問那個 Node 的 kube-proxy，接著 kube-proxy 會藉由 iptables，將此流量導向正確的 App（在 Services 設定好的），無論此 App 有沒有在該 Node 上，kube-proxy 都能正確傳導。
