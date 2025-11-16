# BrandTrack – Real-Time Brand Mention & Reputation Tracker

BrandTrack is a real-time dashboard that monitors brand mentions across online platforms, analyzes sentiment, detects spikes, and helps marketing teams understand brand perception instantly.

Built in under 48 hours for a hackathon, BrandTrack combines fast data ingestion, lightweight NLP, clustering, and a modern dashboard UI.

---

## ⭐ Key Features

### 🔍 Multi-Source Mention Aggregation  
Fetches real-time mentions from:
- Reddit (public API)
- News sources (NewsAPI)
- Fallback demo generator for consistent testing

### 😊 Sentiment Analysis  
Classifies every mention as:
- Positive  
- Negative  
- Neutral  

Using **VADER Sentiment** from the NLTK ecosystem.

### 🧠 Topic Clustering  
Groups mentions by theme using:
- TF-IDF vectorization  
- KMeans clustering

Helps identify what people are talking about.

### 🚨 Spike Alerts  
Automatically detects sudden jumps in activity and creates alerts stored in Postgres.

### 📊 Clean Monitoring Dashboard  
Frontend built with:
- React + Vite  
- Material UI  
- Chart.js for real-time visualization

Includes:
- Mentions timeline  
- Sentiment distribution  
- Alerts panel  
- Recent mentions feed  
- Brand search & tracking  

---

# 🛠️ Tech Stack

### **Backend**
- Python + Django REST Framework  
- PostgreSQL (Render)  
- VADER Sentiment  
- scikit-learn (TF-IDF + KMeans)  
- Docker + Gunicorn  

### **Frontend**
- React  
- Vite  
- Material UI  
- Axios  
- Chart.js  

### **Deployment**
- Backend → Render  
- Frontend → Vercel  

---

# 🧱 Architecture Overview

                ┌────────────────────┐
                │   React Frontend   │
                │      (Vercel)      │
                └─────────┬──────────┘
                          │ API Calls
                          ▼
              ┌────────────────────────┐
              │     Django Backend     │
              │       (Render)         │
              ├──────────┬────────────--
              │ Sentiment│Clustering  │
              │ Analysis │ Engine     │
              └───────┬──┴────────────┘
                      ▼
             ┌──────────────────────┐
             │      PostgreSQL      │
             │   Mentions + Alerts  │
             └──────────────────────┘


---

# ⚙️ Local Setup

## **1. Clone the repository**
- https://github.com/Utkarsh-32/brandtrack.git

## **2. Backend Setup**
- cd backend
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py runserver


## **3. Frontend Setup**
- cd frontend
- npm install
- npm run dev

Your frontend will run on `http://localhost:5173`  
Backend on `http://localhost:8000`

---

# 🔄 Real-Time Ingestion

The backend includes a scheduler that periodically fetches mentions using:
fetch_and_ingest_for_brand()
It stores:
- text  
- source (reddit/news/demo)  
- timestamp  
- sentiment score  
- cluster ID  

This lets the dashboard show trends in real time.

---

# 🧪 Approach & Key Decisions

### **1. Choose NLP that fits hackathon speed**
Instead of heavy models, I used:
- VADER (fast, no GPU, high accuracy for social text)  
- TF-IDF for vectorization  
- KMeans for unsupervised topic grouping  

This allowed us to process mentions in milliseconds.

### **2. Use Postgres for reliability**
SQLite was too slow and unsafe for deployments, so I upgraded to Render’s Postgres.

This gave:
- better concurrency  
- stable ingestion  
- persistent storage  
- indexing for spikes  

### **3. Poll instead of websockets**
Real-time *feeling* without websocket complexity.
The frontend fetches updates every 5 seconds.

### **4. Separate frontend + backend deployment**
- React served through Vercel’s CDN  
- Django handled through Render  
This keeps both scalable and independent.

### **5. Demo Mode**
To guarantee a smooth hackathon demo, I built a fallback:
- synthetic mentions generator  
- ingestion script  
- clustering refresh  

This ensures consistent data even if external APIs rate-limit.

---

# 🧩 Challenges Faced

- Render Postgres migration failures  
- Django worker boot errors due to missing environment variables  
- CORS issues between Vercel and Render  
- Handling sentiment for noisy, short text  
- Fixing React crashes when switching between brands  
- Deployment debugging under time pressure  

These issues shaped the final architecture.

---

# 🚀 Deployment Links

- **Frontend (Live):** https://brandtrack-rouge.vercel.app/
- **Backend (API):** https://brandtrack.onrender.com/

---

# 📌 Future Improvements

- WebSocket-based real-time dashboard  
- Multi-brand comparison  
- Advanced topic modeling (BERTopic / LDA)  
- Social listening from more sources (YouTube, X/Twitter, Blogs)  
- Exportable reports  

---

# 👤 Author
Built solo in under 48 hours for a hackathon.


