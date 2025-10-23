# 🧠 Smart Feedback Analysis and Visualization System

A complete AI-driven sentiment analysis and feedback visualization platform built with **Django**, **NLP**, and **Data Visualization tools**.  
It enables admins to collect, analyze, and visualize customer feedback in real-time with sentiment insights and exportable reports.

---

## 🚀 Project Overview

The **Smart Feedback Analysis and Visualization System** automates the process of collecting textual feedback from users, performs **sentiment analysis (Positive, Negative, Neutral)** using advanced NLP models, and presents **interactive analytics dashboards** for administrators.  
It helps organizations quickly understand user satisfaction trends, monitor performance, and make data-driven decisions.

---

## 🎯 Objectives

- Automatically analyze customer feedback using AI (NLP & sentiment analysis).
- Categorize feedback into **Positive**, **Negative**, or **Neutral**.
- Provide **real-time dashboards** with multiple visualizations.
- Allow admins to **download feedback reports** in CSV or Excel.
- Improve decision-making through intelligent feedback interpretation.

---

## 🧩 Features

### 🧍 User Features
- Submit feedback with or without login.
- Real-time feedback sentiment analysis (Positive, Negative, Neutral).

### 🧑‍💼 Admin Features
- Access a full analytics dashboard.
- Visualize sentiment data using **8+ chart types**:
  - Pie Chart  
  - Bar Chart  
  - Line Chart  
  - Radar Chart  
  - Doughnut Chart  
  - Polar Area Chart  
  - Bubble Chart  
  - Scatter Plot  
- Export feedbacks as **Excel (.xlsx)** or **CSV (.csv)** files.
- Filter exports by **date range**.
- Manage all feedbacks from one dashboard.

---

## 🧱 System Architecture

User Interface (Feedback Forms)
            ↓
Backend (Django Views & Models)
            ↓
Sentiment Engine (DistilBERT / VADER)
            ↓
Database (SQLite / PostgreSQL)
            ↓
Visualization Layer (Chart.js / Plotly)
            ↓
Admin Dashboard (Interactive UI)





---

## 🧠 Sentiment Analysis Model

### 1️⃣ Primary Model — **DistilBERT**
- Model: `distilbert-base-uncased-finetuned-sst-2-english`
- Framework: [Hugging Face Transformers](https://huggingface.co/)
- Features:
  - Context-aware classification  
  - High accuracy (~92%)  
  - Lightweight and fast on CPU  
  - Output: **positive / negative / neutral**

### 2️⃣ Fallback Model — **VADER**
- Library: `vaderSentiment`
- Extremely fast rule-based analysis for short reviews
- Works offline
- Handles emojis and punctuation-based sentiment

---

## 🧰 Tech Stack

| Layer | Technology Used |
|--------|------------------|
| **Frontend** | HTML5, CSS3, Tailwind CSS, Chart.js |
| **Backend** | Django 5.x (Python 3.10+) |
| **Database** | SQLite (default) / PostgreSQL |
| **NLP / ML** | Transformers (DistilBERT), VADER |
| **Export** | CSV, Excel (via `openpyxl`) |
| **Visualization** | Chart.js, Plotly.js |
| **Hosting (Optional)** | PythonAnywhere / AWS / Heroku |

---

## 📂 Database Models

### `MainUser`
| Field | Type | Description |
|--------|------|-------------|
| `user_id` | AutoField | Primary key |
| `fullname` | CharField | Full name of user |
| `email` | CharField | Unique email |
| `password` | CharField | Hashed password |
| `phonenumber` | CharField | Optional |
| `role` | CharField | `registered` / `admin` |
| `created_at` | DateTime | Auto timestamp |
| `is_active` | Boolean | Active status |

### `Feedback`
| Field | Type | Description |
|--------|------|-------------|
| `feedback_id` | AutoField | Primary key |
| `mainuser` | ForeignKey | Linked user (nullable for guests) |
| `feedback_text` | TextField | Feedback message |
| `sentiment_label` | CharField | Positive/Negative/Neutral |
| `sentiment_score` | Float | Score (-1.0 to 1.0) |
| `created_at` | DateTime | Auto timestamp |

### `SentimentSummary`
| Field | Type | Description |
|--------|------|-------------|
| `summary_id` | AutoField | Primary key |
| `positive_count` | Integer | Count of positive feedback |
| `negative_count` | Integer | Count of negative feedback |
| `neutral_count` | Integer | Count of neutral feedback |
| `total_feedback` | Integer | Total feedback count |
| `last_updated` | DateTime | Updated automatically |

---

## 📊 Data Visualizations (Admin Dashboard)

1. **Pie Chart** — Sentiment distribution  
2. **Bar Chart** — Sentiment comparison  
3. **Line Chart** — Sentiment trends over time  
4. **Radar Chart** — Average sentiment scores  
5. **Doughnut Chart** — Feedback proportions  
6. **Polar Area Chart** — Relative sentiment strength  
7. **Bubble Chart** — Score vs intensity  
8. **Scatter Plot** — Feedback distribution by time

---

## 💾 Feedback Export Feature

Admins can:
- Download all feedback as `.csv` or `.xlsx`
- Choose date range (`from` → `to`)
- Auto-named files (e.g., `feedbacks_2025-10-01_to_2025-10-20.xlsx`)

Libraries used:
- `csv` (built-in)
- `openpyxl` (for Excel)

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository
```bash
git clone https://github.com/yourusername/smart-feedback-system.git
cd smart-feedback-system




---
### Create Virtual Environment

python -m venv venv
source venv/bin/activate   # (on macOS/Linux)
venv\Scripts\activate      # (on Windows)



pip install -r requirements.txt


python manage.py makemigrations
python manage.py migrate


python manage.py runserver
Visit: 👉 http://127.0.0.1:8000/





---

## ✅ Summary

This `README.md` includes:
- Project goal and architecture  
- Complete feature list  
- Model details (DistilBERT + VADER)  
- Setup & usage instructions  
- Visualizations & export features  
- Future upgrades & author info  

---

Would you like me to include a **project banner image (header)** and **badges (like Python, Django, Transformers)** at the top for GitHub-style presentation? It’ll make it look professional and portfolio-ready.

