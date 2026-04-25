# ☸️ Kubernetes Monitoring & SRE Observability Stack

[![Kubernetes](https://img.shields.io/badge/Kubernetes-1.23+-326CE5?style=flat-square&logo=kubernetes&logoColor=white)](https://kubernetes.io)
[![Prometheus](https://img.shields.io/badge/Prometheus-v2.38-E6522C?style=flat-square&logo=prometheus&logoColor=white)](https://prometheus.io)
[![Grafana](https://img.shields.io/badge/Grafana-v9.1-F46800?style=flat-square&logo=grafana&logoColor=white)](https://grafana.com)
[![Terraform](https://img.shields.io/badge/Terraform-v1.2-7B42BC?style=flat-square&logo=terraform&logoColor=white)](https://terraform.io)

An enterprise-grade, production-ready Kubernetes monitoring stack designed for Senior SRE and DevOps Engineer portfolios.

---

## 🛠️ Required Tools & Installation

Before you begin, ensure you have the following CLI tools installed:

| Tool | Purpose | Installation (MacOS/Linux) | Installation (Windows) |
| :--- | :--- | :--- | :--- |
| **kubectl** | K8s CLI | `brew install kubectl` | `choco install kubernetes-cli` |
| **helm** | Package Manager | `brew install helm` | `choco install kubernetes-helm` |
| **minikube** | Local K8s | `brew install minikube` | `choco install minikube` |
| **terraform** | Infra as Code | `brew install terraform` | `choco install terraform` |

---

## 🏗️ Step-by-Step Deployment Guide

### Phase 1: Cluster Initialization
```bash
# Start a local cluster with sufficient resources
minikube start --memory=4096 --cpus=4 --driver=docker

# Verify connection
kubectl cluster-info
```

### Phase 2: Core Monitoring Stack (Helm)
Deploy the Prometheus-Grafana-Alertmanager stack using the custom production values provided in this repo.
```bash
# Add and Update Repos
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install kube-prometheus-stack
helm upgrade --install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace \
  -f helm/prometheus-stack/values.yaml

# Install Loki (Logging)
helm repo add grafana https://grafana.github.io/helm-charts
helm upgrade --install loki grafana/loki-stack \
  --namespace monitoring \
  --set loki.persistence.enabled=true
```

### Phase 3: Application Deployment
Deploy the instrumented microservices and security policies.
```bash
# Create Namespace
kubectl create namespace app-prod

# Deploy Backend, DB, Redis, and Exporters
kubectl apply -f kubernetes/base/deployments.yaml

# Apply SRE Security Rules (RBAC & Network Policies)
kubectl apply -f kubernetes/security/rbac-network-policy.yaml
```

### Phase 4: Verification & Access
```bash
# Check all pods are Running
kubectl get pods -A

# Port-forward Grafana to localhost:3000
kubectl port-forward svc/prometheus-grafana -n monitoring 3000:80
```
> **Login Credentials:**  
> **Username:** `admin`  
> **Password:** `admin`

---

## 📈 SRE Observability Commands

### Check Prometheus Targets
Verify that Prometheus is successfully scraping your applications:
```bash
kubectl port-forward svc/prometheus-kube-prometheus-prometheus -n monitoring 9090:9090
# Open http://localhost:9090/targets
```

### Simulate High Traffic (Generate Alerts)
Run this loop to simulate a surge in traffic and watch the Grafana dashboards react:
```bash
# Port-forward the app first
kubectl port-forward svc/backend-service -n app-prod 8000:80

# Run traffic generator
while true; do curl -s http://localhost:8000/api/v1/data; sleep 0.1; done
```

### Inspect Logs via Loki (LogQL)
In Grafana "Explore" tab, use the following query to see backend logs:
```logql
{namespace="app-prod", container="backend"} |= "error"
```

---

## ☁️ Production Deployment (AWS EKS)

For a real-world cloud deployment, use the Terraform manifests:
```bash
cd terraform/environments/prod
terraform init
terraform apply -auto-approve

# Connect to the new cluster
aws eks update-kubeconfig --name monitoring-cluster --region us-east-1
```

---

## 🧹 Cleanup
To remove all resources and stop costs:
```bash
kubectl delete ns app-prod monitoring
minikube delete
# or
terraform destroy -auto-approve
```

---
**Senior SRE Architect Project** | [Detailed Setup Guide](docs/setup_guide.md)