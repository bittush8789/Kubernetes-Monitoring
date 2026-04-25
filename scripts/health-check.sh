#!/bin/bash

echo "🔍 Checking Monitoring Stack Health..."

# Check Prometheus
if kubectl get pods -n monitoring | grep -q "prometheus-server.*Running"; then
    echo "✅ Prometheus is Running"
else
    echo "❌ Prometheus is NOT Running"
fi

# Check Grafana
if kubectl get pods -n monitoring | grep -q "grafana.*Running"; then
    echo "✅ Grafana is Running"
else
    echo "❌ Grafana is NOT Running"
fi

# Check Apps
echo "🔍 Checking Application Status..."
kubectl get pods -n app-prod
