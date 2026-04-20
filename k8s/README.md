# Kubernetes Manifests

Raw Kubernetes manifests for deploying the AI Agent Blueprint stack.

## Components

- **PostgreSQL 16** — StatefulSet with persistent storage
- **Redis 7** — In-memory cache and task queue backend
- **Migrations Job** — Runs `alembic upgrade head` before app deployment
- **API Server** — FastAPI application (2 replicas)
- **SAQ Worker** — Background task processor (1 replica)

## Prerequisites

- A running Kubernetes cluster (k3s, kind, EKS, GKE, etc.)
- `kubectl` configured to talk to your cluster
- Container image built and pushed to your registry

## Quick Start

### 1. Create the namespace

```bash
kubectl apply -f k8s/namespace.yml
```

### 2. Configure secrets

Edit `k8s/secrets.yml` with your base64-encoded values:

```bash
# Encode a value
echo -n "my-secret-value" | base64

# Apply secrets
kubectl apply -f k8s/secrets.yml
```

**Never commit real secrets to version control.**

### 3. Configure the ConfigMap

Edit `k8s/configmap.yml` with your environment-specific values, then apply:

```bash
kubectl apply -f k8s/configmap.yml
```

### 4. Deploy infrastructure

```bash
kubectl apply -f k8s/postgres.yml
kubectl apply -f k8s/redis.yml
```

Wait for pods to be ready:

```bash
kubectl get pods -n app-dev -w
```

### 5. Run migrations

```bash
kubectl apply -f k8s/migrations.yml
```

Check migration status:

```bash
kubectl get jobs -n app-dev
kubectl logs -n app-dev job/run-migrations
```

### 6. Deploy the application

```bash
kubectl apply -f k8s/api.yml
kubectl apply -f k8s/worker.yml
```

### 7. (Optional) Enable ingress

Uncomment and configure `k8s/ingress.yml`, then apply:

```bash
kubectl apply -f k8s/ingress.yml
```

## Common Operations

```bash
# Check all pods
kubectl get pods -n app-dev

# View API logs
kubectl logs -n app-dev -l component=api --tail=100 -f

# View worker logs
kubectl logs -n app-dev -l component=worker --tail=100 -f

# Restart the API deployment
kubectl rollout restart deployment/api -n app-dev

# Re-run migrations (delete old job first)
kubectl delete job run-migrations -n app-dev
kubectl apply -f k8s/migrations.yml

# Exec into the API pod
kubectl exec -it -n app-dev $(kubectl get pod -n app-dev -l component=api -o jsonpath='{.items[0].metadata.name}') -- bash

# Scale the API
kubectl scale deployment/api -n app-dev --replicas=3
```

## Switching to Production

1. Change `namespace: app-dev` to `namespace: app-prod` in all manifests
2. Update image tag from `dev-latest` to a versioned tag
3. Change `imagePullPolicy` from `Always` to `IfNotPresent`
4. Increase resource limits as needed
5. Enable ingress with TLS
