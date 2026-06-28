# 🎓 SmartHire — AI Career Guidance Platform

AI-powered resume analysis, job recommendations, skill gap detection and placement exam prep — built with Python + Streamlit.

---

## 🚀 Quick Start (Windows — VS Code)

### Step 1 — Install Python

1. Go to **https://www.python.org/downloads/**
2. Download **Python 3.11** (or 3.10 / 3.12)
3. Run the installer
4. ✅ **IMPORTANT:** Check **"Add Python to PATH"** before clicking Install

   ![Add to PATH](https://i.imgur.com/p9lCzqK.png)

### Step 2 — Open the SmartHire folder in VS Code

```
File → Open Folder → select the SmartHire folder
```

### Step 3 — Run the app (choose one method)

#### ▶ Option A — Double-click `run.bat`
- Just double-click **`run.bat`** in the SmartHire folder
- It auto-installs everything and opens the app

#### ▶ Option B — VS Code Terminal
1. Open Terminal in VS Code: `Ctrl + `` ` `` (backtick)
2. Run these commands one by one:

```bash
# Install all required packages
pip install -r requirements.txt

# Start the app
streamlit run streamlit_app.py
```

#### ▶ Option C — Command Prompt / PowerShell
```cmd
cd path\to\SmartHire
pip install -r requirements.txt
streamlit run streamlit_app.py
```

### Step 4 — Open in browser

After running, Streamlit will print:

```
Local URL: http://localhost:8501
```

Open **http://localhost:8501** in your browser (it usually opens automatically).

---

## 🛠️ Troubleshooting

### ❌ `'streamlit' is not recognized`
Streamlit is not installed yet. Run:
```cmd
pip install streamlit
```

If `pip` is also not found, Python is not in PATH. Re-install Python and check **"Add Python to PATH"**.

### ❌ `pip is not recognized`
Python is not in PATH. Either:
- Re-install Python and check **"Add Python to PATH"**, OR
- Use `python -m pip install streamlit` instead

### ❌ `python is not recognized`
Python is not installed. Download from https://www.python.org/downloads/

### ❌ Package installation fails
Run as Administrator:
```cmd
pip install -r requirements.txt --user
```

### ❌ Port already in use
```cmd
streamlit run streamlit_app.py --server.port 8502
```

---

## 📁 Project Structure

```
SmartHire/
├── streamlit_app.py       ← Main app (run this)
├── run.bat                ← Windows one-click launcher
├── requirements.txt       ← Python dependencies
├── README.md              ← This file
├── utils/
│   ├── auth.py            ← Login / signup
│   ├── styles.py          ← Dark theme CSS
│   └── resume_parser.py   ← PDF/DOCX resume parser
├── models/
│   ├── classifier.py      ← Resume domain classifier
│   ├── recommender.py     ← Job recommender (25 jobs)
│   └── skill_gap.py       ← Skill gap analyser
├── assets/
│   └── student.png        ← Login page image
└── data/
    └── users.json         ← Created automatically on first signup
```

---

## 📋 Pages

| Page | What it does |
|------|-------------|
| 🔐 Login / Sign Up | First page — create account or login |
| 🏠 Dashboard | Stats: Resume Score, Job Match, Tests Taken |
| 📄 Resume Upload | Upload PDF/DOCX/TXT — extracts skills |
| 🔍 Resume Analysis | ML domain prediction + score breakdown |
| 💼 Job Recommendations | 25 real jobs matched to your skills |
| 📊 Skill Gap Report | Shows missing skills for target role |
| 📝 Exams | Easy / Medium / Hard — 10 questions each, auto-graded |
| 📚 Learning Resources | Courses, docs, practice sites |
| 👤 Profile | Edit your details |
| ℹ️ About | About the platform |

---

## 🧠 Exam Section

Three difficulty levels with **placement-type questions** and **automatic grading**:

| Level | Focus |
|-------|-------|
| 🟢 Easy | Python basics, Data Structures, SQL, OOP |
| 🟡 Medium | QuickSort, ACID, Deadlocks, HTTP, Heaps |
| 🔴 Hard | CAP theorem, Dijkstra, Amortised analysis, ML, NP-Complete |

After submitting → instant score (%), grade (A+/A/B/C/D/F), and full answer review with explanations.

---

## 📦 Requirements

```
streamlit>=1.32.0
scikit-learn>=1.3.0
pandas>=2.0.0
numpy>=1.24.0
PyPDF2>=3.0.0
python-docx>=1.1.0
plotly>=5.18.0
pillow>=10.0.0
nltk>=3.8.0
matplotlib>=3.7.0
wordcloud>=1.9.0
```

Install all at once: `pip install -r requirements.txt`

---

## 📌 Notes

- User accounts are stored in `data/users.json` — created automatically
- No internet connection required after install
- Resume scoring uses keyword-based ML (no API needed)
- Works on Windows, Mac and Linux

---

*SmartHire v1.0 — Machine Learning Industrial Project*
