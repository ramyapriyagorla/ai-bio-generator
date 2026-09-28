# ✨ AI Bio Generator

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B.svg)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-Generative%20AI-orange.svg)](https://aistudio.google.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An intelligent, production-ready web application built with **Python, Streamlit, NLP, and Generative AI (Google Gemini)** that crafts natural, polished, and grammatically flawless biographical summaries tailored to your professional identity.

---

## 🌟 Key Features

- **🎯 Zero-Hallucination Guarantee**: Strict prompt engineering and grounding rules instruct the AI model to use *only* the user's explicitly provided facts without inventing degrees, dates, metrics, or companies.
- **📑 5 Bio Styles**:
  - **Professional**: Balanced executive summary highlighting core competencies, achievements, and track record.
  - **Student**: Academic focus emphasizing coursework, university projects, research, and career ambitions.
  - **LinkedIn**: Modern "About" section with an engaging hook, formatted value proposition, and networking CTA.
  - **Short**: Concise 2–4 sentence elevator pitch.
  - **Detailed**: Comprehensive 3–4 paragraph biographical narrative.
- **🎭 4 Tone Options**:
  - `Professional`: Formal, articulate, and authoritative.
  - `Friendly`: Warm, relatable, and approachable.
  - `Simple`: Clear, jargon-free plain English.
  - `Confident`: Bold, dynamic, and high-impact.
- **⚡ 1-Click Quick Presets**: Test instantly using realistic sample profiles (*Senior Software Engineer*, *AI/ML Student*, *Lead Product Manager*).
- **📊 NLP Metrics**: Live counters for **Word Count**, **Character Count**, **Sentence Count**, and **Estimated Silent Reading Time**.
- **🛠️ Action Controls**:
  - **🚀 Generate Bio**: Instant synthesis with loading indicator.
  - **🔄 Regenerate**: Generate creative alternative variations with adjusted temperature.
  - **🗑️ Clear**: Reset all fields with one click.
  - **📋 Copy to Clipboard**: Built-in 1-click code copy button.
  - **📥 Download as TXT**: Export structured text file with metadata, timestamp, and source facts.
- **🛡️ Secure Credential Management**: Reads API keys from `.env` via `python-dotenv` or dynamic UI sidebar input.
- **🧠 Resilient NLP Fallback**: If an API key is not yet set or quota is limited, a deterministic local NLP synthesizer ensures the app remains fully functional and testable.

---

## 🏗️ Project Architecture

```
ai-bio-generator/
│
├── app.py                # Main Streamlit web application & UI
├── bio_generator.py      # Gemini AI integration, prompt guardrails & NLP synthesizer
├── utils.py              # NLP metrics calculation, TXT export formatter & sample presets
├── test_generator.py     # Automated test suite
├── requirements.txt      # Project dependencies
├── .env.example          # Environment variable template
├── .env                  # Local environment file (git-ignored)
├── .gitignore            # Git exclusion rules
└── README.md             # Project documentation
```

---

## 🚀 Quickstart & Installation

### 1. Prerequisites
- Python 3.10 or higher
- Git (optional)

### 2. Clone or Navigate to the Project
```bash
cd C:\Users\ramya\.gemini\antigravity\scratch\ai-bio-generator
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Google Gemini API Key (Optional)
To use the Google Gemini Generative AI model:
1. Obtain a free API key at [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Open `.env` (or copy from `.env.example`):
   ```env
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   ```
*(Note: You can also enter or override your API key directly in the web app sidebar at runtime! If no key is set, the app runs seamlessly in Offline NLP mode.)*

### 5. Launch the Application
Run the Streamlit app:
```bash
streamlit run app.py
```

The application will launch in your browser at `http://localhost:8501`.

---

## 🧪 Running Automated Tests

Run the test suite to verify prompt formatting, NLP metrics, and generation across all bio types and tones:

```bash
python -m unittest test_generator.py -v
```

---

## 🔒 Security Best Practices
- The `.env` file containing sensitive credentials is listed in `.gitignore` and is never committed to source control.
- An `.env.example` template is provided for quick onboarding.

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
