import os

files_to_header = {
    "apps/backend/main.py": "# File: apps/backend/main.py\n# Description: FastAPI Backend with Prometheus Instrumentation for SRE Golden Signals.\n# Project: Kubernetes Monitoring Stack\n",
    "kubernetes/base/deployments.yaml": "# File: kubernetes/base/deployments.yaml\n# Description: Core deployments for Backend, PostgreSQL, and Redis with monitoring sidecars.\n# Project: Kubernetes Monitoring Stack\n",
    "helm/prometheus-stack/values.yaml": "# File: helm/prometheus-stack/values.yaml\n# Description: Production-grade Helm values for the Kube-Prometheus-Stack.\n# Project: Kubernetes Monitoring Stack\n",
    "terraform/environments/prod/main.tf": "# File: terraform/environments/prod/main.tf\n# Description: AWS EKS Cluster and VPC provisioning using Terraform modules.\n# Project: Kubernetes Monitoring Stack\n",
    "prometheus/rules/sre_alerts.yaml": "# File: prometheus/rules/sre_alerts.yaml\n# Description: Prometheus Alerting Rules for Application and Infrastructure outages.\n# Project: Kubernetes Monitoring Stack\n",
    "scripts/install-monitoring.sh": "# File: scripts/install-monitoring.sh\n# Description: Automated installation script for the entire monitoring stack.\n# Project: Kubernetes Monitoring Stack\n",
    "kubernetes/security/rbac-network-policy.yaml": "# File: kubernetes/security/rbac-network-policy.yaml\n# Description: Security policies and RBAC for monitoring infrastructure.\n# Project: Kubernetes Monitoring Stack\n"
}

# Determine if we are in the project root or one level above
if os.path.exists("apps/backend/main.py"):
    prefix = ""
elif os.path.exists("k8s-monitoring-stack/apps/backend/main.py"):
    prefix = "k8s-monitoring-stack"
else:
    print("Could not find project files.")
    exit(1)

for file_rel_path, header in files_to_header.items():
    full_path = os.path.join(prefix, file_rel_path)
    if os.path.exists(full_path):
        with open(full_path, "r") as f:
            content = f.read()
        
        # Only prepend if not already there
        if not content.startswith("# File:"):
            with open(full_path, "w") as f:
                # For shell scripts, keep the shebang at the top
                if content.startswith("#!"):
                    lines = content.splitlines()
                    shebang = lines[0]
                    rest = "\n".join(lines[1:])
                    f.write(f"{shebang}\n{header}\n{rest}")
                else:
                    f.write(f"{header}\n{content}")
            print(f"Header added to: {file_rel_path}")
