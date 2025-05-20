# 🚀 FastAPI + MongoDB Auth App (Kubernetes + Tailwind UI)

A modern authentication-ready CRUD web app built with **FastAPI**, **MongoDB**, and deployed via **Kubernetes**. Includes:

- 🔐 Login / Logout / Register flow
- 🌐 Google OAuth2 placeholder (ready for integration)
- 🧾 MongoDB CRUD operations
- 📦 Dockerized with local Minikube support
- 🎨 TailwindCSS UI aligned with DevOps portfolio theme

---

## 🖼️ Live Preview

![Auth UI Screenshot](./assets/screenshot.png)

---

## ⚙️ Features

- [x] FastAPI backend with Jinja templates
- [x] MongoDB Atlas or local DB support
- [x] Login + Logout with session cookies
- [x] Register new users
- [x] Export users to CSV
- [x] Google Login button UI
- [x] Beautiful responsive dark-mode UI
- [x] Kubernetes deployment with Minikube
- [x] Docker image build pipeline

---

## 🧠 Tech Stack

- **Backend:** FastAPI (Python 3.10)
- **Frontend:** TailwindCSS via CDN + Jinja templates
- **Database:** MongoDB
- **Containerization:** Docker + Minikube
- **Orchestration:** Kubernetes

---

## 🚀 Quickstart (Minikube)

> ⚠️ Make sure Docker is configured to work with Minikube:

```bash
minikube start
minikube image build -t fastapi-mongo:local .
kubectl apply -f k8s/
minikube service webapp-service
