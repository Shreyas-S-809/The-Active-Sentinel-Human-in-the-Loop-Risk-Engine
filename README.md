<div align="center">

# The Active Sentinel — Human-in-the-Loop Loan Risk Engine

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Live Demo](https://img.shields.io/badge/LIVE-DEMO-white.svg)](https://the-active-sentinel.streamlit.app/)

</div>

> **Goal:**  
> Build a production-oriented loan risk prediction system that not only makes decisions, but learns from human corrections and monitors its own performance in real time.

---

## 🎯 Motivation

Most ML projects end at `model.predict()`. Real-world systems continue long after deployment.
**The Active Sentinel bridges this gap** by simulating how deployed ML systems handle uncertainty, collect corrections, and evolve post-deployment.

---

## 💡 Why This Project Exists

Financial institutions don't just need accurate models—they need **accountable, auditable systems** that:
- Operate under regulatory scrutiny
- Handle edge cases through human oversight
- Adapt to data drift and changing risk patterns
---

## 🏗️ Core Architecture

```
┌─────────────────────────┐
│  Streamlit Frontend     │  User interaction & feedback collection
└───────────┬─────────────┘
            │ HTTPS
            ↓
┌─────────────────────────┐
│  FastAPI Backend        │  Inference API + feedback logging
│  (Render)               │
└───────────┬─────────────┘
            │
    ┌───────┴────────┐
    ↓                ↓
┌─────────┐    ┌──────────┐
│ RF Model│    │ SQLite DB│
│ (.pkl)  │    │ Feedback │
└─────────┘    └──────────┘
```

**Stack:**
- **Backend:** FastAPI (stateless inference service)
- **Frontend:** Streamlit (user interface)
- **Model:** Random Forest (scikit-learn)
- **Storage:** SQLite (feedback persistence)
- **Deployment:** Render (HTTPS endpoints)

---

## ✨ Key Features

###  Inference
- REST API with `/predict`, `/feedback`, and `/stats` endpoints
- Confidence-scored predictions with interpretability
- Stateless service design for horizontal scaling

### 🔄 Human-in-the-Loop Validation
- Real-time feedback mechanism (Correct/Incorrect labels)
- Persistent storage for post-deployment analysis
- Simulates domain expert review workflows

###  Live Performance Monitoring
- Dynamic accuracy computation from user corrections
- Transparent model reliability metrics
- Feedback-driven evaluation dashboards

### 🚀 Deployment-Aware Design
- Independent backend/frontend services
- Production-grade API contracts & Scalable

---

##  Use Cases

| **Scenario** | **Application** |
|-------------|----------------|
| **Loan Origination** | Risk officers review and override model decisions |
| **Insurance Underwriting** | Human adjustors provide ground truth labels |
| **Fraud Detection** | Security analysts validate alert accuracy |

---

## 🌐 Deployment Guide

Check out the live demo at: **[https://the-active-sentinel.streamlit.app/](https://the-active-sentinel.streamlit.app/)**

### Backend (FastAPI)
```bash
# Deployed on Render
# Exposes inference API at: https://active-sentinel.onrender.com
```

### Frontend (Streamlit)
```bash
# Configure backend URL in app
# Run locally or deploy to Streamlit Cloud
streamlit run app.py
```

### ⚠️ Cold Start Behavior
Render's free tier auto-sleeps inactive services. **First request after inactivity may take 30-60 seconds**—this is expected.

---

## 🎓 What This Demonstrates

**End-to-end ML system design**  
**API-based inference** (production patterns vs. notebook code)  
**Feedback integration** (human-in-the-loop workflows)  
**Live monitoring** (post-deployment performance tracking)  
**Deployment trade-offs** (cold starts, stateless services, persistence) 

---

## 🛠️ Technical Decisions

| **Choice** | **Rationale** |
|-----------|--------------|
| **FastAPI** | Async support, auto-generated docs, type safety |
| **SQLite** | Zero-config persistence for MVP; easy migration to PostgreSQL |
| **Random Forest** | Interpretable, handles mixed data types, production-proven |
| **Render Free Tier** | Demonstrates real deployment constraints (cold starts) |
| **Separate Backend/Frontend** | Mirrors microservices architecture, independent scaling |

---

## 🔮 Future Enhancements

- [ ] **PostgreSQL migration** for multi-user persistence
- [ ] **Scheduled retraining pipeline** using collected feedback
- [ ] **Drift detection alerts** (PSI, KS tests, data quality monitoring)
- [ ] **Role-based access control** for feedback validation workflows
- [ ] **A/B testing framework** for model version comparison

---

## 💭 Project Philosophy

> **"This project is intentionally simple in modeling and strong in system design."**

The goal isn't chasing 99% accuracy—it's about demonstrating how ML systems operate **after deployment**:
- How feedback gets collected
- How performance is monitored
- How humans stay in the loop

---

## 🚀 Getting Started

```bash
# Clone repository
git clone https://github.com/Shreyas-S-809/The-Active-Sentinel-Human-in-the-Loop-Risk-Engine
cd The-Active-Sentinel-Human-in-the-Loop-Risk-Engine

# Install dependencies
pip install -r requirements.txt

# Run backend locally
uvicorn api:app --reload

# Run frontend (separate terminal)
streamlit run app.py
```

---

## 🖥️ Running the Project Locally (Important)

This project is deployed using a separated frontend–backend architecture. When running the system locally, a few configuration changes are required to avoid environment-specific issues.

### 1️⃣ Update API Endpoint for Local Development

The Streamlit frontend communicates with the FastAPI backend via an API URL.

**When deployed**, the frontend points to the Render-hosted backend:
```python
API_URL = "https://active-sentinel.onrender.com"
```

**For local development**, update this in `frontend/app.py`:
```python
API_URL = "http://127.0.0.1:8000"
```

This ensures the frontend correctly connects to the locally running FastAPI server.

⚠️ **If this change is not made**, the frontend will attempt to call the deployed API, resulting in connection errors.

### 2️⃣ Install Local-Only Dependencies

During deployment, the backend and frontend were separated to meet platform constraints. When running the project locally, the frontend requires additional packages.

Ensure the following dependencies are present in `requirements.txt`:
```
streamlit
requests
```

Then install all dependencies using:
```bash
pip install -r requirements.txt
```

These packages are required only for local execution of the Streamlit UI and are intentionally excluded from the backend-only deployment environment.

### 3️⃣ Start Both Services

**Terminal 1 – Start FastAPI Backend**
```bash
uvicorn api.main:app --reload
```

**Terminal 2 – Start Streamlit Frontend**
```bash
streamlit run frontend/app.py
```

**Access Points:**
- Backend: `http://127.0.0.1:8000`
- Frontend: `http://localhost:8501`

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

## 📬 Contact

**Shreyas S**  
[GitHub](https://github.com/Shreyas-S-809) | [LinkedIn](https://www.linkedin.com/in/shreyas-s-97081b290/)

---

<div align="center">

**⭐ Star this repo if you found it helpful!**

</div>