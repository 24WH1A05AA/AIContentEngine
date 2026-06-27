# 🚀 AI Content Engine

Generate an entire marketing campaign from a single product brief using Generative AI.

AI Content Engine is a Streamlit application that combines text generation, image generation, and video generation into one seamless workflow.

---

## ✨ Features

Generate in one click:

✅ Campaign Tagline

✅ 200-word Blog Introduction

✅ Social Media Posts

✅ Hero Image

✅ Promotional Video

---

## 🖥️ Demo Workflow

Input

- Product Name
- Target Audience
- Brand Tone

↓

Generate

↓

AI creates

- Tagline
- Blog
- Social Posts
- Hero Image
- Video

↓

Display all assets

---

# Tech Stack

Frontend

- Streamlit

Backend

- Python

AI

- OpenRouter
- GPT Models
- GPT Image API
- Runway API

---

# Project Structure

```
content_engine/
│
├── app.py
├── config.py
├── text_gen.py
├── image_gen.py
├── video_gen.py
├── requirements.txt
├── .env
└── README.md
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/username/AIContentEngine.git

cd AIContentEngine
```

Create virtual environment

```bash
python -m venv .venv
```

Activate environment

Windows

```bash
.venv\Scripts\activate
```

Mac/Linux

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file

```env
OPENROUTER_API_KEY=your_key
OPENAI_API_KEY=your_key
RUNWAY_API_KEY=your_key
```

---

# Run

```bash
streamlit run app.py
```

---

# AI Pipeline

```
User Brief
      │
      ▼
Tagline
      │
      ▼
Blog Introduction
      │
      ▼
Social Media Posts
      │
      ▼
Hero Image
      │
      ▼
Promotional Video
```

---

# Prompt Engineering Techniques

### Campaign Tagline

- Few-shot Prompting

### Blog

- Role-based Prompting

### Social Posts

- Structured Output

### Hero Image

- Prompt Formula

### Promotional Video

- Motion Prompting

---

# APIs Used

- OpenRouter
- GPT Image API
- Runway API

---

# Folder Responsibilities

### app.py

Main Streamlit UI

### text_gen.py

Generates

- Tagline
- Blog
- Social Posts

### image_gen.py

Creates image prompt and hero image.

### video_gen.py

Creates motion prompt and promotional video.

### config.py

Stores configuration and API settings.

---

# Future Improvements

- Voice-over generation
- Campaign export
- Download ZIP
- Campaign history
- Multiple image styles
- Tone switcher
- Regenerate individual assets

---

# Learning Outcomes

This project demonstrates:

- Prompt Engineering
- Prompt Chaining
- AI Orchestration
- Multi-modal AI
- Streamlit Development
- OpenRouter Integration
- GPT Image API
- Runway Integration
- API Error Handling

---

# License

This project is intended for educational and learning purposes.
