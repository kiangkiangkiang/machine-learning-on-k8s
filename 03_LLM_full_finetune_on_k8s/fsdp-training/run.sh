echo "Start training worker 1"
kubectl apply -f training_worker1.yaml

echo "Wait 50s for RDZV Server setup"
sleep 50

echo "Start training worker 2"
kubectl apply -f training_worker2.yaml