# 📖 Full Implementation & Setup Guide

This guide provides a exhaustive step-by-step walkthrough to set up the **Kubernetes Monitoring Stack** from scratch.

---

## 🏗️ Phase 1: Local Environment Preparation

Before starting, ensure you have the following tools installed:
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) or [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [Kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Helm v3](https://helm.sh/docs/intro/install/)

### 1. Start your Local Cluster
```bash
minikube start --memory=4096 --cpus=4
```

---

## 🛠️ Phase 2: Monitoring Stack Deployment

### 1. Create the Monitoring Namespace
```bash
kubectl create namespace monitoring
```

### 2. Deploy Prometheus Stack via Helm
The `kube-prometheus-stack` bundles Prometheus, Grafana, and Alertmanager.
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Deploy with our custom production-grade values
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  -f helm/prometheus-stack/values.yaml
```

### 3. Deploy Loki for Log Aggregation
```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm install loki grafana/loki-stack \
  --namespace monitoring \
  --set loki.persistence.enabled=true \
  --set loki.persistence.size=5Gi
```

---

## 🚀 Phase 3: Deploying Instrumented Applications

Now we deploy the apps that we want to monitor. These apps have special annotations that Prometheus will use to find them.

### 1. Create the Application Namespace
```bash
kubectl create namespace app-prod
```

### 2. Apply Application Manifests
```bash
# This includes Backend API, PostgreSQL, and Redis
kubectl apply -f kubernetes/base/deployments.yaml

# Apply security policies
kubectl apply -f kubernetes/security/rbac-network-policy.yaml
```

---

## 📊 Phase 4: Verification & Dashboarding

### 1. Verify Pod Status
Ensure all pods in both `monitoring` and `app-prod` namespaces are `Running`.
```bash
kubectl get pods -A
```

### 2. Access Grafana Dashboards
```bash
kubectl port-forward svc/prometheus-grafana -n monitoring 3000:80
```
- Open `http://localhost:3000`
- User: `admin` / Password: `admin`
- Navigate to **Dashboards** -> **SRE Application Golden Signals**.

### 3. Access Prometheus (Optional)
```bash
kubectl port-forward svc/prometheus-kube-prometheus-prometheus -n monitoring 9090:9090
```

---

## 🧪 Phase 5: Simulating a Production Incident

To prove the stack works, we need to generate some "bad" traffic.

### 1. Generate Traffic (High RPS)
```bash
# In a new terminal
while true; do curl -s http://localhost:8000/api/v1/data; sleep 0.1; done
```

### 2. Monitor Alertmanager
Check if the `HighLatencyP95` or `HighErrorRate` alerts trigger in the Grafana "Alerting" tab.

---

## ☁️ Phase 6: Production Setup (AWS EKS)

For a real SRE portfolio, you should deploy to EKS:

1. **Configure AWS CLI**: `aws configure`
2. **Provision Infra**:
   ```bash
   cd terraform/environments/prod
   terraform init
   terraform apply
   ```
3. **Connect to EKS**:
   ```bash
   aws eks update-kubeconfig --name monitoring-cluster --region us-east-1
   ```
4. **Repeat Phases 2 & 3** on the EKS cluster.

---

## 📝 SRE Interview Talking Points

- **Metric Scrapping**: Explain how `kubernetes_sd_configs` (Service Discovery) in Prometheus automatically finds new pods using annotations.
- **Sidecar Exporters**: Explain why we use `postgres-exporter` as a sidecar to expose metrics from the DB without modifying the DB source code.
- **Log Correlation**: Show how Loki labels like `container_name` and `namespace` allow you to filter logs identically to how you filter metrics in Prometheus.
