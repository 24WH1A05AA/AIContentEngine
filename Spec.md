# AI Content Engine Pro - Technical Specification

## Project Overview

AI Content Engine Pro extends the original AI Content Engine by adding production-ready capabilities while preserving all existing functionality.

The application generates a complete marketing campaign from a single product brief using multiple Generative AI models. In Stage 2, it introduces AI quality evaluation, automatic regeneration, voiceover generation, and multi-channel adaptation.

---

# Project Stages

## Stage 1 – AI Content Engine

Generates:

1. Campaign Tagline
2. Blog Introduction
3. Social Media Posts
4. Hero Image
5. Promotional Video

---

## Stage 2 – Content Engine Pro

Adds:

1. AI Self-Critique Loop
2. Voiceover Generation
3. Multi-Channel Adaptation

---

# Objectives

- Accept a marketing brief.
- Generate complete campaign assets.
- Validate generated content automatically.
- Regenerate weak content.
- Generate voice narration.
- Adapt campaigns for multiple audiences.

---

# Inputs

| Field | Type | Description |
|------|------|-------------|
| Product Name | String | Product name |
| Target Audience | String | Intended audience |
| Brand Tone | Dropdown | Premium, Eco, Playful, etc. |
| Adaptation Channel | Dropdown | LinkedIn, TikTok, Facebook |

---

# Outputs

## Stage 1

- Campaign Tagline
- Blog Introduction
- Social Media Posts
- Hero Image
- Promotional Video

## Stage 2

- AI Critique Report
- Regenerated Content (if required)
- Voiceover Script
- MP3 Audio
- Adapted Campaign

---

# Functional Requirements

## FR1 — Campaign Tagline

- Max 10 words
- Few-shot prompting
- Brand-aware

## FR2 — Blog Introduction

- Approximately 200 words
- Uses generated tagline
- Audience-specific

## FR3 — Social Media Posts

Generate JSON:

```json
{
  "twitter":"",
  "instagram":"",
  "linkedin":""
}
```

## FR4 — Hero Image

Generate one hero image using prompt engineering.

## FR5 — Promotional Video

Generate 5–8 second promotional video.

## FR6 — AI Self-Critique Loop

Automatically evaluates:

- Tone
- Audience
- Length
- Product consistency

Returns:

```json
{
  "tagline":{"pass":true,"issue":null},
  "blog":{"pass":false,"issue":"Length exceeded"},
  "social":{"pass":true,"issue":null}
}
```

Behavior

- Automatic evaluation
- Maximum 2 retries
- Feedback injected into regeneration prompt
- Warning displayed if still failing

## FR7 — Voiceover Generation

- Convert blog to narration script
- Add punctuation cues
- Remove visual references
- Generate MP3 audio

## FR8 — Multi-Channel Adaptation

Supported channels:

- B2B LinkedIn
- Gen-Z TikTok
- Parents Facebook

Rewrites:

- Tagline
- Blog
- Social Posts

Keeps:

- Hero Image
- Promotional Video

---

# Workflow

```text
User Brief
    ↓
Generate Text Assets
    ↓
AI Self-Critique
    ├── PASS
    └── FAIL → Retry (Max 2)
    ↓
Hero Image
    ↓
Promotional Video
    ↓
Voiceover
    ↓
Channel Adaptation
    ↓
Display Results
```

---

# Project Structure

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
└── README.md
```

---

# AI Models

## Text

- OpenAI GPT-5
- OpenRouter

## Image

- Gemini Image Generation

## Video

- Gemini Video Generation

## Audio

- OpenAI TTS / ElevenLabs

---

# Environment Variables

```env
OPENAI_API_KEY=
OPENROUTER_API_KEY_FOR_IMAGE_AND_VIDEO=
ELEVENLABS_API_KEY=
```

---

# Error Handling

- Empty input validation
- Missing API keys
- Network failures
- Retry logic
- Voice generation failures
- Adaptation failures
- Graceful error messages

---

# Future Enhancements

- A/B Testing
- Campaign PDF Export
- Cost Tracker
- Campaign History
- Multilingual Support
- Brand Memory

---

# Success Criteria

The application successfully:

- Generates all Stage 1 campaign assets.
- Validates content using AI.
- Automatically regenerates weak outputs.
- Produces a playable voiceover.
- Adapts campaign text for multiple channels.
- Preserves image and video during adaptation.
- Handles invalid input gracefully.
