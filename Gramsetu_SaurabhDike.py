# GraminSetu AI © 2026 Saurabh Dike. All rights reserved.
import streamlit as st
import asyncio
import edge_tts
import os
from google import genai
from google.genai import types 
from PIL import Image
from langdetect import detect # For auto-language detection

# --- 1. CONFIGURATION ---
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key = api_key)

# Maps language codes to high-quality Indian voices
VOICE_MAP = {
    "hi": "hi-IN-MadhurNeural",     # Hindi Male
    "mr": "mr-IN-ManoharNeural",   # Marathi Male
    "en": "en-IN-PrabhatNeural",   # Indian English Male
    "default": "hi-IN-MadhurNeural" 
}

# Instructs Gemini to mirror the user's language
SYSTEM_PROMPT = """
You are 'Graminsetu', an Indian rural assistant. 
1. Identify the language of the user's question (Hindi, Marathi, or English).
2. Respond ONLY in that same language.
3. Keep advice simple, practical, and respectful.
"""

async def generate_voice(text):
    """Detects language and picks the right voice."""
    if os.path.exists("response.mp3"):
        os.remove("response.mp3")
    
    try:
        lang = detect(text) # Detects 'hi', 'mr', or 'en'
    except:
        lang = "hi" # Default to Hindi if detection fails
        
    selected_voice = VOICE_MAP.get(lang, VOICE_MAP["default"])
    communicate = edge_tts.Communicate(text, selected_voice)
    await communicate.save("response.mp3")
    return "response.mp3"

# --- 2. UI ---
def main():
    st.set_page_config(page_title="Gramsetu Multilingual", page_icon="🌾")
    st.title("🌾 Graminsetu: Bharat Assistant")
    
    # Multilingual Labels
    uploaded_image = st.file_uploader("Upload Crop Photo / फोटो अपलोड करा", type=["jpg", "jpeg", "png"])
    recorded_audio = st.audio_input("Record Voice / आवाज रेकॉर्ड करा")
    user_query = st.text_input("Type your question / तुमचा प्रश्न लिहा:")

    if st.button("Get Advice / सल्ला मिळवा"):
        content_parts = [SYSTEM_PROMPT]
        
        if user_query: content_parts.append(user_query)
        if uploaded_image:
            img_bytes = uploaded_image.getvalue()
            content_parts.append(types.Part.from_bytes(data=img_bytes, mime_type=uploaded_image.type))
        if recorded_audio:
            audio_bytes = recorded_audio.getvalue()
            content_parts.append(types.Part.from_bytes(data=audio_bytes, mime_type="audio/wav"))

        if len(content_parts) > 1:
            with st.spinner("Analyzing..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash", 
                        contents=content_parts
                    )
                    ans_text = response.text
                    st.write(ans_text)
                    
                    # Voice switches to match the detected language
                    audio_path = asyncio.run(generate_voice(ans_text))
                    st.audio(audio_path)
                    
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please provide input / कृपया प्रश्न विचारा।")

if __name__ == "__main__":
    main()

#python -m streamlit run Gramsetu_SaurabhDike.py