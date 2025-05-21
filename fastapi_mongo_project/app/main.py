from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from pymongo import MongoClient
from passlib.context import CryptContext
from datetime import datetime
from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
import pandas as pd
import os

# Load .env variables
load_dotenv()

# Initialize app
app = FastAPI(
    title="User Profile API",
    description="🚀 FastAPI + MongoDB CRUD App with Mongo Login & Google OAuth",
    version="3.0.0"
)

# Middleware
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "supersecret"))
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth config
oauth = OAuth()
oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={"scope": "openid email profile"}
)

# MongoDB setup
client = MongoClient(
    f"mongodb://{os.environ.get('USER_NAME')}:{os.environ.get('USER_PWD')}@{os.environ.get('DB_URL')}"
)
db = client["demo"]
users_collection = db["users"]

# Templates
templates = Jinja2Templates(directory="app/templates")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str):
    return pwd_context.hash(password)
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Pydantic model
class User(BaseModel):
    name: str
    email: EmailStr
    age: int

# 🏠 Homepage
@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    user = request.session.get("user")
    return templates.TemplateResponse("index.html", {"request": request, "user": user})

# 🔐 Register
@app.post("/register")
def register_user(request: Request, username: str = Form(...), password: str = Form(...)):
    if users_collection.find_one({"email": username}):
        return HTMLResponse("⚠️ User already exists", status_code=400)
    users_collection.insert_one({
        "email": username,
        "password": hash_password(password),
        "created_at": datetime.utcnow()
    })
    request.session["user"] = username
    return RedirectResponse(url="/", status_code=303)

# 🔐 Login
@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = users_collection.find_one({"email": username})
    if not user or not verify_password(password, user["password"]):
        return HTMLResponse(content="❌ Invalid credentials", status_code=401)
    request.session["user"] = username
    return RedirectResponse(url="/", status_code=303)

# 🔓 Logout
@app.post("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)

# 📄 Get all users
@app.get("/users", summary="Get All Users")
def get_users():
    users = list(users_collection.find({}, {"_id": 0, "password": 0}))
    return {
        "status": "success",
        "count": len(users),
        "users": users
    }

# ➕ Add a new user
@app.post("/users", summary="Add New User")
def add_user(user: User):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="❌ User with this email already exists.")
    user_data = user.dict()
    user_data["created_at"] = datetime.utcnow()
    users_collection.insert_one(user_data)
    return {
        "status": "success",
        "message": "✅ User added successfully",
        "user": user_data
    }

# 📤 Export users to CSV
@app.get("/export", summary="Export Users to CSV")
def export_users():
    data = list(users_collection.find({}, {"_id": 0, "password": 0}))
    if not data:
        raise HTTPException(status_code=404, detail="❌ No users to export.")
    df = pd.DataFrame(data)
    export_path = "/app/exports/users.csv"
    os.makedirs("/app/exports", exist_ok=True)
    df.to_csv(export_path, index=False)
    return FileResponse(
        export_path,
        media_type="text/csv",
        filename="users.csv"
    )

# 🔑 Google Sign-In
@app.get("/auth/google")
async def login_google(request: Request):
    redirect_uri = str(request.url_for('auth'))
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth")
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)

        # Correct way to get user info
        resp = await oauth.google.get("userinfo", token=token)
        user = resp.json()

        # Validate
        email = user.get("email")
        if not email:
            return HTMLResponse("❌ Google login failed: email not found.", status_code=400)

        request.session["user"] = email

        # Auto-create user if not exists
        if not users_collection.find_one({"email": email}):
            users_collection.insert_one({
                "email": email,
                "password": None,
                "created_at": datetime.utcnow(),
                "google": True
            })

        return RedirectResponse(url="/", status_code=303)

    except Exception as e:
        print("Google login error:", str(e))
        return HTMLResponse("❌ Login failed", status_code=500)
