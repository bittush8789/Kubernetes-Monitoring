#!/bin/bash
# File: scripts/install-monitoring.sh
# Description: Automated installation script for the entire monitoring stack.
# Project: Kubernetes Monitoring Stack


# Configuration
NAMESPACE="monitoring"
APP_NAMESPACE="app-prod"

echo "🚀 Starting Kubernetes Monitoring Stack Installation..."

# 1. Create Namespaces
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -
kubectl create namespace $APP_NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# 2. Add Helm Repos
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

# 3. Install Prometheus Stack
echo "📊 Installing Prometheus & Grafana..."
helm upgrade --install prometheus prometheus-community/kube-prometheus-stack \
  --namespace $NAMESPACE \
  -f helm/prometheus-stack/values.yaml

# 4. Install Loki Stack
echo "📝 Installing Loki & Promtail..."
helm upgrade --install loki grafana/loki-stack \
  --namespace $NAMESPACE \
  --set loki.persistence.enabled=true \
  --set loki.persistence.size=10Gi

# 5. Deploy Apps
echo "🚀 Deploying Demo Applications..."
kubectl apply -f kubernetes/base/deployments.yaml

echo "✅ Installation Complete!"
echo "Run 'kubectl get pods -n $NAMESPACE' to check status."