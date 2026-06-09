# 🛡️ FAILSAFE — Early Warning System for At-Risk Students

**Predict student failure BEFORE it happens — with Explainable AI and Auto-Generated Intervention Plans.**

---

## 🎯 Problem Statement

In educational institutions, student failure often goes undetected until end-of-semester results, leaving no room for meaningful intervention. Faculty lack a proactive, data-driven tool to identify at-risk students early and understand the root causes behind their struggles.

---

## 💡 Solution

FAILSAFE is a web-based system where faculty upload student data and a trained ML model predicts failure risk — with **Explainable AI (SHAP)** making every prediction transparent — and **auto-generates personalised intervention plans** to help faculty act before it's too late.

---

## 🚀 Live Demo

| Component | URL |
|-----------|-----|
| **Frontend** | [failsafe-six.vercel.app](https://failsafe-six.vercel.app) |
| **Backend API** | [failsafe-api-wvs6.onrender.com](https://failsafe-api-wvs6.onrender.com) |

---

## 🧠 Machine Learning Model

### Dataset
- **UCI Student Performance Dataset** — 649 students, 33 features
- Combined Math (`student-mat.csv`) and Portuguese (`student-por.csv`) courses

### Features Used (32 total)
| Category | Features |
|----------|----------|
| **Academic** | G1, G2 (period grades), failures, studytime |
| **Attendance** | absences, traveltime |
| **Behavioral** | Dalc, Walc (alcohol), goout, freetime, romantic |
| **Family** | Pstatus, famsup, famrel, Medu, Fedu, Mjob, Fjob |
| **Demographics** | age, sex, address, famsize, school |

### Model Architecture
XGBoost Classifier + SMOTEENN (Handling Imbalance)
├── SMOTE: Synthetic Minority Oversampling
├── ENN: Edited Nearest Neighbors (noise removal)
└── Threshold Tuning: Optimal F2-score threshold

text

### Performance
| Metric | Score |
|--------|:-----:|
| **Accuracy** | 92% |
| **Fail Recall** | **95%** 🔥 |
| **ROC-AUC** | 0.956 |
| **False Alarms** | 16 (acceptable) |

### Handling Imbalance
- Original ratio: 5.5:1 (Pass:Fail)
- SMOTEENN applied → Balanced training data
- Threshold tuned to 0.55 for optimal fail detection

---

## 🔍 Explainable AI (SHAP)

Every prediction comes with **5 SHAP risk factors** explaining exactly WHY a student is flagged:

| Feature | Impact | Direction |
|---------|:------:|:---------:|
| G2 | -4.59 | 🔴 Risk |
| absences | -0.34 | 🔴 Risk |
| studytime | +0.28 | 🟢 Protective |

Faculty see human-readable explanations:
- 🔴 **G2=4** → Strong risk factor
- 🔴 **absences=15** → Moderate risk  
- 🟢 **studytime=4** → Protective factor

---

## 📋 Auto-Generated Intervention Plans

Based on SHAP risk factors, the system generates personalised action plans:

| Risk Factor | Intervention | Priority |
|-------------|-------------|:--------:|
| Low G1/G2 | Schedule remedial classes | **High** |
| High absences | Attendance monitoring program | **High** |
| Alcohol (Dalc/Walc) | Counselor referral | **High** |
| Past failures | Assign academic mentor | **High** |
| Family factors | Parent-teacher meeting | Medium |

Each plan includes: **Action → Detail → Priority → Timeline**

---

## 🏗️ Architecture

┌─────────────────────────────────────────────────────────┐
│ React Frontend (Vercel) │
│ ┌──────────┐ ┌──────────┐ ┌───────────────────────┐ │
│ │ Upload │ │Dashboard │ │ Intervention Tracker │ │
│ │ Module │ │ & Charts │ │ │ │
│ └──────────┘ └──────────┘ └───────────────────────┘ │
└─────────────────────┬───────────────────────────────────┘
│ REST API
┌─────────────────────┴───────────────────────────────────┐
│ FastAPI Backend (Render) │
│ ┌──────────┐ ┌──────────┐ ┌──────────────────────┐ │
│ │ Auth │ │ ML Model │ │ Intervention │ │
│ │ Service │ │ Service │ │ Generator │ │
│ └──────────┘ └──────────┘ └──────────────────────┘ │
└─────────────────────┬───────────────────────────────────┘
│
┌─────────────────────┴───────────────────────────────────┐
│ PostgreSQL (Supabase Cloud) │
│ ┌──────────┐ ┌──────────┐ ┌──────────────────────┐ │
│ │ Users │ │Predictions│ │ Students │ │
│ └──────────┘ └──────────┘ └──────────────────────┘ │
└─────────────────────────────────────────────────────────┘


---

### 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React.js, Recharts, Axios |
| **Backend** | FastAPI, Python 3.11 |
| **ML** | XGBoost, SHAP, Scikit-learn, Imbalanced-learn |
| **Database** | PostgreSQL (Supabase) |
| **Auth** | JWT, bcrypt |
| **Deployment** | Vercel (Frontend), Render (Backend) |

---

## 📁 Project Structure
FAILSAFE/
├── failsafe-backend/
│ ├── main.py # FastAPI entry point
│ ├── requirements.txt # Python dependencies
│ ├── runtime.txt # Python version for Render
│ ├── models/ # Trained model files
│ ├── utils/
│ │ ├── model_loader.py # Load model & pipeline
│ │ ├── preprocessing.py # Data preprocessing
│ │ ├── pipeline.py # CompletePipeline class
│ │ ├── intervention.py # Intervention generator
│ │ └── auth.py # JWT authentication
│ ├── routes/
│ │ ├── predict.py # Prediction endpoints
│ │ └── auth.py # Login/signup endpoints
│ └── database/
│ ├── connection.py # Supabase connection
│ └── models.py # Database tables
│
├── failsafe-frontend/
│ ├── src/
│ │ ├── pages/
│ │ │ ├── Dashboard.jsx # Main dashboard
│ │ │ └── LoginPage.jsx # Authentication
│ │ ├── components/
│ │ │ └── RiskChart.jsx # Pie & Bar charts
│ │ └── App.jsx # Router setup
│ └── package.json
│
├── colab_notebooks/
│ └── failsafe_model.ipynb # Model training notebook
│
└── README.md


---

## 🔧 Local Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- Supabase account (free)
- Git

### Backend Setup
```bash
cd failsafe-backend
python -m venv failsafe_env
failsafe_env\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

Frontend Setup
cd failsafe-frontend
npm install
npm run dev

Environment Variables (.env)
DATABASE_URL=postgresql://user:pass@host:6543/postgres
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

🎯 Goals Achieved
Goal	Status
Predict at-risk students using attendance, assignments & behavioral data	✅
SHAP explanations for every prediction	✅
Auto-generated personalised intervention plans	✅
Faculty & HOD dashboard with risk trends	✅

👨‍💻 Author
Built with ❤️ as part of the FAILSAFE project.
