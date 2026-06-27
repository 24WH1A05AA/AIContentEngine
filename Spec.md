# AI Content Engine - Technical Specification

## Project Overview

AI Content Engine is a multi-modal Streamlit application that generates a complete marketing campaign from a single product brief. Using multiple AI services, the application produces five creative assets including text, image, and video.

The project demonstrates prompt engineering, AI orchestration, and multi-model pipelines by chaining multiple AI calls together.

---

## Objectives

- Accept a simple marketing brief.
- Generate multiple campaign assets automatically.
- Demonstrate prompt chaining across multiple AI models.
- Produce professional marketing content with one click.

---

# Inputs

The application accepts:

| Field | Type | Description |
|-------|------|-------------|
| Product Name | String | Name of the product |
| Target Audience | String | Intended audience |
| Brand Tone | Dropdown | Brand personality (Premium, Eco, Playful, etc.) |

---

# Outputs

The application generates:

1. Campaign Tagline
2. Blog Introduction (200 words)
3. Social Media Posts
4. Hero Image
5. Promotional Video

---

# Functional Requirements

## FR1 — Campaign Tagline

Generate:

- Maximum 10 words
- Few-shot prompting
- Matches brand tone
- No hashtags

---

## FR2 — Blog Introduction

Generate:

- Exactly 200 words
- Role-based prompt
- Uses generated tagline
- Matches target audience

---

## FR3 — Social Media Posts

Generate JSON output containing:

```json
{
  "twitter": "...",
  "instagram": "...",
  "linkedin": "..."
}
```

Character Limits

Twitter ≤280

Instagram ≤2200

LinkedIn ≤700

---

## FR4 — Hero Image

Generate one hero image using GPT Image API.

Image Prompt Formula

Subject

↓

Style (derived from tone)

↓

Composition

↓

Constraints

Example

Photorealistic

16:9

Centered composition

No text

No logos

---

## FR5 — Promotional Video

Generate:

- Image-to-video
- 5–8 seconds
- Runway API
- Motion prompt
- Cinematic push-in

---

# Prompt Chain

User Brief
      │
      ▼
Tagline
      │
      ▼
Blog Introduction
      │
      ▼
Image Prompt
      │
      ▼
Hero Image
      │
      ▼
Runway Motion Prompt
      │
      ▼
Promotional Video

---

# Application Workflow

1. User enters product information.
2. User clicks Generate.
3. Generate tagline.
4. Generate blog.
5. Generate social media posts.
6. Generate hero image.
7. Generate promotional video.
8. Display all generated assets.

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
├── assets/
├── utils/
├── requirements.txt
├── .env
└── README.md
```

---

# AI Models

## Text Generation

- OpenRouter
- GPT models

## Image Generation

- GPT Image API
- gpt-image-2

## Video Generation

- Runway API

---

# APIs

OpenRouter API

GPT Image API

Runway API

---

# Environment Variables

```
OPENROUTER_API_KEY=
OPENAI_API_KEY=
RUNWAY_API_KEY=
```

---

# Error Handling

- Empty input validation
- API retry logic
- Invalid API key handling
- Network timeout handling
- Graceful error messages

---

# Future Enhancements

- Voice-over generation
- Download campaign as ZIP
- Multiple tagline variants
- Campaign history
- Prompt editor
- Multi-language generation

---

# Success Criteria

The application successfully generates:

- Brand-consistent tagline
- 200-word blog
- Platform-specific social posts
- Hero image
- 5–8 second promotional video

from one product brief using one Generate button.
