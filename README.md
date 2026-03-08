---
title: Intervexa
emoji: 🎓
colorFrom: green
colorTo: green
sdk: gradio
sdk_version: 6.9.0
app_file: app.py
pinned: false
license: mit
short_description: "Ai Coach for interviews "
---

# 🎓 Intervexa: AI Mock Interview Coach

An AI-powered interview simulator that conducts **realistic job interviews** and gives **honest, structured feedback**.

## Testing on Huggingface:

Link:https://huggingface.co/spaces/m3n99/Intervexa

## Features

- 🎯 Pick your role, company type, and experience level
- 🤖 AI interviewer powered by **LLaMA 3.3 70B via Groq**
- 💬 6 questions: behavioral, technical, situational, culture fit
- 📋 Final score + detailed evaluation report
- ⚡ Ultra-fast responses via Groq inference

## How to Run Locally

```bash
pip install -r requirements.txt
export GROQ_API_KEY=your_key_here
python app.py
```

Get your free Groq API key at: https://console.groq.com

## System Prompt Design

The interviewer persona is fully engineered via a dynamic system prompt that adapts based on:

- **Role** → changes technical question topics
- **Company type** → shifts focus (scale vs. ownership vs. process)
- **Experience level** → calibrates question depth and expectations

## Tech Stack

- **LLM**: LLaMA 3.3 70B (via Groq API)
- **Interface**: Gradio 6.x
- **Hosting**: Hugging Face Spaces
