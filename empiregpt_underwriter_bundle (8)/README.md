# EmpireGPT Underwriting Engine
This is a production-ready, modular Python project scaffold for real estate underwriting with Streamlit frontend.
# EmpireGPT Underwriter

## 🚀 Quick Start (Local)

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
Copy `.env.example` to `.env` and update values:
```bash
cp .env.example .env
```

### 3. Run Streamlit
```bash
streamlit run app/main.py
```

---

## 🐳 Quick Start (Docker)

### 1. Set `.env`
```bash
cp .env.example .env
```

### 2. Launch Docker Compose
```bash
docker-compose up
```

Streamlit → http://localhost:8501  
FastAPI   → http://localhost:8000
