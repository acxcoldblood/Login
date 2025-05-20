
# FastAPI + MongoDB on Kubernetes (Minikube)

## Build Docker Image (inside Minikube)
```bash
minikube image build -t fastapi-mongo:local .
```

## Apply K8s Resources
```bash
kubectl apply -f k8s/mongo-config.yaml
kubectl apply -f k8s/mongo-secret.yaml
kubectl apply -f k8s/mongo.yaml
kubectl apply -f k8s/webapp.yaml
```

## Access the App
```bash
minikube service webapp-service
```

## Endpoints
- `/` → app check
- `/users` → list users (from MongoDB)
