# 🚀 FastAPI + MongoDB Auth App (Kubernetes + Tailwind UI)

A modern authentication-ready CRUD app built with **FastAPI**, **MongoDB**, and deployed using **Kubernetes (Minikube)**. Includes:

- 🔐 Login / Logout / Register
- 🌐 Google Sign-In UI (OAuth-ready)
- 🎨 Responsive TailwindCSS UI
- 🧾 MongoDB-based storage
- 📦 Docker & Kubernetes deployment

---

## 🧱 Tech Stack

- **Backend**: FastAPI (Python 3.10)
- **Frontend**: TailwindCSS (via Jinja templates)
- **Database**: MongoDB (local or cloud)
- **Containerization**: Docker
- **Orchestration**: Kubernetes (Minikube)

---

## 🐳 Build Docker Image in Minikube

> First, ensure you’re using Minikube’s Docker daemon:

```bash
minikube image build -t fastapi-mongo:local .
Deploy Kubernetes Resources
bash
Copy
Edit
kubectl apply -f k8s/mongo-config.yaml
kubectl apply -f k8s/mongo-secret.yaml
kubectl apply -f k8s/mongo.yaml
kubectl apply -f k8s/webapp.yaml
🌐 Access the App
bash
Copy
Edit
minikube service webapp-service
This opens the app in your browser at a NodePort like http://127.0.0.1:30100

🔁 Common Rebuild Commands
After updating index.html, main.py, or static files:

bash
Copy
Edit
minikube image build -t fastapi-mongo:local .
kubectl rollout restart deployment webapp-deployment
📡 API Endpoints
Method	Path	Description
GET	/	Homepage (Login/Register UI)
POST	/login	Email/password login
POST	/logout	Clear session
POST	/register	Register new user
GET	/users	List all MongoDB users
GET	/export	Download users as CSV

📂 Project Structure
arduino
Copy
Edit
.
├── app/
│   ├── main.py
│   └── templates/
│       └── index.html
├── k8s/
│   ├── mongo.yaml
│   ├── mongo-config.yaml
│   ├── mongo-secret.yaml
│   └── webapp.yaml
├── Dockerfile
├── requirements.txt
└── README.md
🧪 Development (Run Locally)
Install dependencies:
bash
Copy
Edit
pip install -r requirements.txt
Start the app:
bash
Copy
Edit
uvicorn app.main:app --reload
Visit: http://localhost:8000

📦 Environment Variables (used in K8s)
Name	Source	Purpose
USER_NAME	Secret (mongo-user)	MongoDB username
USER_PWD	Secret (mongo-password)	MongoDB password
DB_URL	ConfigMap (mongo-url)	MongoDB host/service

👨‍💻 Author
Kushagra Agarwal
🔗 GitHub
🌐 DevOps Portfolio

📝 License
This project is licensed under the MIT License — free for personal and commercial use.

yaml
Copy
Edit

---

### ✅ To Use:
1. Create a file named `README.md` in your repo root.
2. Paste the above content.
3. (Optional) Add a screenshot named `screenshot.png` and include:
   ```markdown
   ![UI Screenshot](./screenshot.png)