# 🚀 Content Engine Pro

> Generate an end-to-end AI-powered marketing campaign from a single product brief.

Content Engine Pro extends the original AI Content Engine with production-ready capabilities including AI self-critique, automatic regeneration, voiceover generation, and multi-channel content adaptation.

---

# 📌 Project Stages

## Stage 1 – AI Content Engine

The original project generates a complete marketing campaign from a single product brief using Generative AI.

### Features

Generate in one click:

* ✅ Campaign Tagline
* ✅ 200-word Blog Introduction
* ✅ Social Media Posts
* ✅ Hero Image
* ✅ Promotional Video
* ✅ Prompt Chaining
* ✅ Streamlit Interface

---

## Stage 2 – Content Engine Pro

Stage 2 upgrades the project with three production-ready capabilities.

### 🤖 AI Self-Critique Loop

* Reviews tagline, blog, and social posts automatically
* Validates tone, audience, length, and product accuracy
* Automatically regenerates weak outputs
* Maximum 2 retries
* Displays PASS/FAIL verdict

### 🎙 Voiceover Generation

* Converts blog into a narration script
* Adds punctuation for natural pauses
* Removes visual references
* Generates playable MP3 audio

### 🔄 Multi-Channel Adaptation

Supports:

* B2B LinkedIn
* Gen-Z TikTok
* Parents Facebook

Rewrites:

* Campaign Tagline
* Blog Introduction
* Social Media Posts

Hero Image and Promotional Video remain unchanged.

---

# ✨ Features

Generate in one click:

* ✅ Campaign Tagline
* ✅ Blog Introduction
* ✅ Social Media Posts
* ✅ Hero Image
* ✅ Promotional Video

Additional Content Engine Pro features:

* 🤖 AI Self-Critique
* 🔁 Automatic Regeneration
* 🎙 Voiceover Generation
* 🔄 Multi-Channel Adaptation

---

# 🖥️ Demo Workflow

Input

* Product Name
* Target Audience
* Brand Tone

↓

Generate

↓

AI creates

* Tagline
* Blog
* Social Posts
* Hero Image
* Promotional Video

↓

AI Self-Critique

↓

Voiceover

↓

Channel Adaptation

↓

Display Final Campaign

---

# 🏗 Tech Stack

## Frontend

* Streamlit

## Backend

* Python

## AI

### Text Generation

* OpenAI GPT-5
* OpenRouter (Optional Text Models)

### Image Generation

* Gemini Image Generation

### Video Generation

* Gemini Video Generation

### Voice Generation

* OpenAI TTS / ElevenLabs

---

# 📂 Project Structure

```text
content_engine/

├── app.py
├── config.py
├── text_gen.py
├── image_gen.py
├── video_gen.py
├── critic.py
├── voiceover.py
├── adaptation.py
├── utils/
├── assets/
├── requirements.txt
├── .env
└── README.md
```

---

# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/ContentEnginePro.git

cd ContentEnginePro
```

Create virtual environment

```bash
python -m venv .venv
```

Activate environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux/macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file

```env
OPENAI_API_KEY=

OPENROUTER_API_KEY_FOR_IMAGE_AND_VIDEO=

ELEVENLABS_API_KEY=
```

---

# ▶ Run

```bash
streamlit run app.py
```

---

# 🤖 AI Pipeline (Stage 1)

```text
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

# 🚀 Content Engine Pro Workflow (Stage 2)

```text
User Brief
    ↓
Generate Text Assets
    ↓
AI Self-Critique
    ├── PASS → Continue
    └── FAIL → Regenerate (Max 2)
    ↓
Hero Image
    ↓
Promotional Video
    ↓
Voiceover
    ↓
Channel Adaptation
    ↓
Final Campaign
```

---

# 🧠 Prompt Engineering Techniques

### Campaign Tagline

* Few-shot Prompting

### Blog

* Role-based Prompting

### Social Posts

* Structured Output

### Hero Image

* Prompt Formula

### Promotional Video

* Motion Prompting

### AI Self-Critique

* Self-Evaluation Prompting
* Reflection-based Prompting

### Voiceover

* Prompt Transformation

### Multi-Channel Adaptation

* Persona-based Prompting

---

# 🌐 APIs Used

### Text

* OpenAI GPT-5
* OpenRouter

### Image

* Gemini Image API

### Video

* Gemini Video API

### Voice

* OpenAI TTS / ElevenLabs

---

# 📁 Folder Responsibilities

### app.py

Main Streamlit UI

### text_gen.py

Generates

* Tagline
* Blog
* Social Posts

### image_gen.py

Creates hero image.

### video_gen.py

Creates promotional video.

### critic.py

Evaluates generated content and triggers automatic regeneration when required.

### voiceover.py

Generates narration script and voice audio.

### adaptation.py

Creates platform-specific marketing content.

### config.py

Stores configuration and API settings.

---

# ⚠ Error Handling

* Empty input validation
* Missing API keys
* Network failures
* AI generation failures
* Critique retry handling
* Voice generation failures
* Adaptation failures

---

# 🚀 Future Improvements

* Campaign PDF Export
* Cost Tracking
* A/B Testing
* Brand Memory
* Campaign History
* Multilingual Support

---

# 🎓 Learning Outcomes

This project demonstrates:

* Prompt Engineering
* Prompt Chaining
* AI Self-Evaluation
* AI Orchestration
* Multi-modal AI
* Voice Synthesis
* Content Adaptation
* Streamlit Development
* Production-ready AI Pipelines
* API Integration
* Error Handling

---

# 📄 License

This project was developed for educational purposes as part of the **Content Engine Pro** assignment.
