Containerized Network Health Checker

Automated network state validation and health-checking service designed to pull real-time telemetry from Cisco IOS infrastructure, containerized with Docker, and orchestrated on Kubernetes (Minikube).

Overview:

This project leverages Python and network automation librarie (Netmiko) to continuously poll network devices interface up/down status. It then packages the Python script into a lightweight Docker container and runs it as a Kubernetes pod in a local Minikube environment. 

Architecture:

The automation pipeline flows from physical/virtual infrastructure up through container orchestration:

+------------------------------------+      +-------------------------------------------+
|   Cisco IOS Router                 |      |   Minikube (Kubernetes Cluster)           |
|   (VirtualBox Host-Only Network)   |      |                                           |
|                                    |      |   +-----------------------------------+   |
|   - SSH Server Enabled             | <------- |   Network Health Checker Pod      |   |
|   - Management IP: 192.168.8.x     |  SSH |   |   (Python + Netmiko / NAPALM)     |   |
|   				     |      |   +-----------------------------------+   |
+------------------------------------+      +-------------------------------------------+


1. Infrastructure Layer: A Cisco IOS instance hosted locally in VirtualBox, reachable via a host-only network interface.
2. Automation Layer: Python script utilizing Netmiko for SSH execution.
3. Containerization Layer: Multi-stage Docker image optimizing runtime dependencies and security.
4. Orchestration Layer: Kubernetes Pod deployed via Minikube on Windows WSL2, managing deployment lifecycle and environment variables.

Tech Stack:

* Language: Python 3.11+
* Network Automation: Netmiko
* Containerization: Docker Desktop / WSL2
* Orchestration: Kubernetes (Minikube)
* Target Infrastructure: Cisco IOS (VirtualBox)
* Configuration: Environment variables (.env / Kubernetes ConfigMaps & Secrets)

Features & Health Checks:

The health checker collects and validates structural operational state:

* Interface Status & Statistics: Identifies down interfaces.
* Structured Output: Exports status checks into standardized JSON logs suitable for downstream ingestion (e.g., Elasticsearch, Prometheus, or stdout).

Getting Started:

Prerequisites:

* Windows 10/11 with WSL2 enabled
* Docker Desktop configured with the WSL2 backend
* Minikube and kubectl installed
* VirtualBox running a Cisco IOS router configured with SSH access (e.g., IP: 192.168.56.101, User: admin)

Local Setup & Execution:

1. Clone the repository:

git clone https://github.com/Maab-Abuelbasher/Network.git
cd Network

2. Build the Docker image locally:

docker build -t interface-status:v1.0 .


3. Deploy to Minikube:
Point your terminal to Minikube’s internal Docker daemon:

eval $(minikube docker-env)
docker build -t interface-status:v1.0 .
kubectl apply -f pod.yaml


4. View pod output & logs:

kubectl get pods
kubectl logs -f interface-status


Why This Project?

As a Network and Security Engineer transitioning into DevNetOps, I built this project to move beyond manual CLI show commands and traditional static network management. Traditional network operations often rely on human intervention to diagnose link degradation or routing failures.

This repository demonstrates:

* Infrastructure-as-Code & Automation: Treating network state verification as modern software microservices.
* Cloud-Native Networking: Applying containerization (Docker) and cloud orchestration (Kubernetes) to legacy routing and switching topologies.
* Root-Cause Systems Thinking: Automating repetitive diagnostic workflows to focus on system resilience and high-level architecture.
