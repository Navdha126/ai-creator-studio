# ✦ AI Creator Studio

I built this during my 3rd year of BTech because I kept seeing Instagram creators struggle with the same problems — inconsistent branding, generic captions, no idea what colors actually work for their niche. I wanted to build something that actually solves that, not just another chatbot demo.



![AI Creator Studio](https://img.shields.io/badge/Status-Active-brightgreen) ![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-blue) ![React](https://img.shields.io/badge/React-18-61DAFB) ![Python](https://img.shields.io/badge/Python-3.13-yellow)

---



The color intelligence feature came from a personal idea I had about brand identity — most creators have no idea what their visual archetype is or whether their color palette even matches their niche. I built a system that tells them that automatically.

---

## 🚀 What It Does

### 🧠 AI Content Generation
- Generates Instagram captions, hashtags, and hook lines
- Personalized to creator's niche, tone, and target audience
- Memory-aware — remembers user preferences across sessions so you never have to repeat yourself

### 📚 RAG Knowledge Base
- Upload any marketing PDF or guide
- AI retrieves the most relevant knowledge before answering your question
- Built with ChromaDB and Sentence Transformers — not just keyword search, actual semantic understanding

### 🎨 Brand Color Intelligence
- Upload multiple Instagram screenshots
- Extracts dominant colors using K-Means clustering
- Detects your visual archetype from 8 possible archetypes
- Tells you whether your current palette actually aligns with your niche
- Recommends specific colors for 20+ creator niches
- Generates light, dark, and complementary variations of your brand colors

### 👤 Creator Memory System
- Saves your profile once, uses it forever
- Every content generation automatically uses your stored niche, tone, and audience
- No more repeating yourself every session

### 🔥 Automated Trends Feed
- Pulls real articles daily from Buffer, Sprout Social, and Social Media Examiner
- AI reads those articles and extracts trending hook templates automatically
- 12 battle-tested hook frameworks built in
- 6 trending content formats with step-by-step filming instructions
- Refreshes itself every 24 hours — no manual work needed

### 🖼️ AI Image Generation (Coming Soon)
- Stable Diffusion via Hugging Face Inference API
- Generates brand-aligned images based on your detected archetype and color palette
- Currently pending network configuration for cloud deployment

---

## 🏗️ Architecture

User
↓
React Frontend
↓
FastAPI Backend
↓
┌─────────────────────────────────┐
│  Memory System (JSON)           │
│  RAG Pipeline (ChromaDB)        │
│  Color Intelligence (OpenCV)    │
│  Trends Engine (RSS + Groq)     │
│  LLM (Groq - Llama 3.3 70B)    │
└─────────────────────────────────┘

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React, Axios |
| Backend | Python, FastAPI |
| LLM | Groq (Llama 3.3 70B) |
| Vector DB | ChromaDB |
| Embeddings | Sentence Transformers (Hugging Face) |
| Computer Vision | OpenCV, Pillow |
| ML | Scikit-learn (K-Means Clustering) |
| Trends | FeedParser, APScheduler, BeautifulSoup |
| Image Gen | Stable Diffusion (Hugging Face) |

---

## ⚙️ Setup

### Prerequisites
- Python 3.13+
- Node.js 24+
- Groq API Key — free at console.groq.com
- Hugging Face Token — free at huggingface.co

### Backend

```bash
cd backend
pip install -r requirements.txt
```


Run the server:
```bash
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm start
```

Opens at http://localhost:3000

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/save-profile` | Save creator profile |
| GET | `/get-profile/{user_id}` | Get creator profile |
| POST | `/generate-caption` | Generate captions + hashtags |
| POST | `/analyze-colors` | Analyze brand color palette |
| POST | `/ask-knowledge-base` | RAG-powered strategy Q&A |
| POST | `/generate-smart-content` | Unified content generation |
| POST | `/color-variations` | Get color variations |
| GET | `/trends` | Get trending hooks and formats |
| POST | `/refresh-trends` | Manually refresh trends |
| POST | `/generate-image` | Generate AI image |
| POST | `/generate-post` | Generate complete post |

---

## 🎨 Visual Archetypes

One of my favorite features. The system analyzes uploaded images and classifies the creator's visual style into one of 8 archetypes — then checks if that archetype actually matches their niche.

| Archetype | Description |
|-----------|-------------|
| Luxury Mystic | Dark, rich, opulent. Mystery and exclusivity |
| Soft Healer | Pastels and warm neutrals. Safe and nurturing |
| Corporate Authority | Dark blues and whites. Professional trust |
| High Energy | Bold reds and blacks. Action and motivation |
| Futuristic | Cyber tones. Innovation and modernity |
| Earthy Natural | Browns and greens. Authenticity and nature |
| Soft Feminine | Blush pinks and lavenders. Delicate and warm |
| Dark Feminine | Deep crimsons and blacks. Powerful and magnetic |

---

## 🧠 How RAG Works
PDF Upload
↓
Text Extraction (pypdf)
↓
Chunking (500 words/chunk)
↓
Embeddings (Sentence Transformers)
↓
Storage (ChromaDB)
↓
Query → Semantic Search → Relevant Chunks → LLM → Answer

The key difference from a regular chatbot: the LLM doesn't answer from its training data alone. It first retrieves the most relevant chunks from your uploaded documents, then answers using that context. That's what makes it actually useful for niche-specific knowledge.

---

## 🔥 How the Trends Engine Works
RSS Feeds (Buffer, Sprout Social, Social Media Examiner)
↓
Article Fetching every 24 hours (FeedParser)
↓
Hook Extraction via Groq LLM
↓
Combined with Built-in Hook Library (12 frameworks)
↓
Displayed in frontend with category, example, and why it works

I didn't want to manually update a trends database. So I built a background scheduler that fetches new marketing articles daily and uses the LLM to extract hook patterns automatically. It runs silently in the background — you never have to touch it.

---

## 👩‍💻 About Me

Hi, I'm Navdha — a 3rd year BTech CSE student focused on AI/ML. 
I built this project to get hands-on experience with RAG pipelines, 
vector databases, computer vision, and LLM integration. 


This project taught me more than any course did. I ran into real problems — model deprecations, network restrictions, Python version conflicts, Git history issues — and figured them out. That's the part that actually matters.

If you want to talk about the architecture or anything in here, feel free to reach out.

**What this project covers:**
- LLM Integration and Prompt Engineering
- RAG Architecture with Vector Databases
- Computer Vision and Color Analysis
- REST API Design with FastAPI
- React Frontend Development
- Background Job Scheduling
- Git Version Control