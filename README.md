# 🌾 GraminSetu: A Multimodal Rural Empowerment AI Agent

**Developed by:** Saurabh Dike  
**Role:** Computer Engineering Student, Savitribai Phule Pune University (SPPU)  
**Project Type:** Microsoft Elevate AICTE Capstone Project (Jan 2026)

## 🚀 Overview
GraminSetu is a specialized AI assistant designed to bridge the digital divide in rural India. By utilizing **Gemini 3 Flash**, it provides a multimodal interface where users can interact via **Text, Voice, and Images** to receive advice on agricultural best practices and government schemes.

## ✨ Key Features
* **Multilingual Support**: Real-time interaction in Marathi, Hindi, and English.
* **Multimodal Input**: Upload crop photos for disease analysis or record voice queries for ease of use.
* **Voice Response**: Integrated with `edge-tts` to provide localized, high-quality audio responses.
* **Secure & Scalable**: Implemented with industry-standard secret management and RAG (Retrieval-Augmented Generation) principles.

## 🛠️ Tech Stack
- **Language:** Python 3.11+
- **AI Model:** Gemini 3 Flash (Google GenAI SDK)
- **Framework:** Streamlit
- **Voice Synthesis:** Edge-TTS
- **Language Detection:** Langdetect

## ⚙️ Installation & Setup
1. Clone this repository:
   `git clone https://github.com/yourusername/GraminSetu.git`
2. Install dependencies:
   `pip install -r requirements.txt`
3. Set up your `.streamlit/secrets.toml` with your `GEMINI_API_KEY`.
4. Run locally:
   `python -m streamlit run Gramsetu_SaurabhDike.py`

---
© 2026 Saurabh Dike. All rights reserved.