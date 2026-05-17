# GraminSetu AI © 2026 Saurabh Dike. All rights reserved.
import streamlit as st
import asyncio
import edge_tts
import os
from google import genai
from google.genai import types 
from PIL import Image
from langdetect import detect # For auto-language detection

# Setting and styling
st.set_page_config(page_title="GraminSetu AI", page_icon="🌿", layout = "wide")

# CSS code for a better UI
st.markdown("""
    <style>
    .main {background-color: #fdfaf5;}
    .stButton>button{
        width: 100%;
        border-radius: 15px;
        height: 3em;
        background-color: #2e7d32;
        color: white;
        font-weight: bold;
        border: none;
    }
    st.button>button:hover{ background-color: #1b5e20; color: #e8f5e9; }
    .instruction-card{
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #2e7d32;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# ---  CONFIGURATION ---
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
# SYSTEM_PROMPT = """
# You are 'Graminsetu', an Indian rural assistant. 
# 1. Identify the language of the user's question (Hindi, Marathi, or English).
# 2. Respond ONLY in that same language.
# 3. Keep advice simple, practical, and respectful.
# """

# Initialize chat memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

async def generate_voice(text, manual_lang):
    """Detects language and picks the right voice."""
    if os.path.exists("response.mp3"):
        os.remove("response.mp3")
    
    # Map the sidebar string to the voice codes
    lang_code_map = {"हिंदी": "hi", "मराठी": "mr", "English": "en"}
    lang = lang_code_map.get(manual_lang, "hi")
        
    selected_voice = VOICE_MAP.get(lang, VOICE_MAP["default"])
    communicate = edge_tts.Communicate(text, selected_voice)
    await communicate.save("response.mp3")
    return "response.mp3"

# --- 2. UI ---
def main():
    if "selected_lang" not in st.session_state:
        st.session_state.selected_lang = "English"
#Define your Translation Dictionary
    # This translates every UI label dynamically based on selection
    labels = {
        "English": {
            "title": "🌾 GraminSetu: Digital Mitra",
            "subtitle": "Your AI Expert",
            "tab1": "💬 Ask Advice",
            "tab2": "📜 Previous Conversations",
            "step1": "<b>Step 1: Provide Input</b><br>Type, speak, or upload a photo.",
            "step2": "<b>Step 2: AI Diagnosis</b><br>The response will appear here.",
            "input_label": "Type your question:",
            "upload_label": "Upload Crop Photo",
            "audio_label": "Record Voice",
            "btn_label": "🚀 Get Expert Solution",
            "history_empty": "No history yet."
        },
        "हिंदी": {
            "title": "🌾 ग्रामीणसेतु: डिजिटल मित्र",
            "subtitle": "आपका एआई विशेषज्ञ",
            "tab1": "💬 सलाह लें",
            "tab2": "📜 पिछला इतिहास",
            "step1": "<b>चरण 1: इनपुट प्रदान करें</b><br>लिखें, बोलें या फ़ोटो अपलोड करें।",
            "step2": "<b>चरण 2: एआई निदान</b><br>जवाब यहां दिखाई देगा।",
            "input_label": "अपना प्रश्न लिखें:",
            "upload_label": "फसल का फोटो अपलोड करें",
            "audio_label": "अपनी आवाज रिकॉर्ड करें",
            "btn_label": "🚀 विशेषज्ञ समाधान प्राप्त करें",
            "history_empty": "अभी तक कोई इतिहास नहीं है।"
        },
        "मराठी": {
            "title": "🌾 ग्रामीणसेतू: डिजिटल मित्र",
            "subtitle": "तुमचा एआय तज्ञ",
            "tab1": "💬 सल्ला मिळवा",
            "tab2": "📜 मागील संभाषण",
            "step1": "<b>पायरी १: माहिती द्या</b><br>लिहा, बोला किंवा फोटो अपलोड करा.",
            "step2": "<b>पायरी २: एआय निदान</b><br>उत्तर येथे दिसेल.",
            "input_label": "तुमचा प्रश्न लिहा:",
            "upload_label": "पिकाचा फोटो अपलोड करा",
            "audio_label": "तुमचा आवाज रेकॉर्ड करा",
            "btn_label": "🚀 तज्ज्ञ उपाय मिळवा",
            "history_empty": "अद्याप कोणताही इतिहास नाही."
        }
    }

    # 3. Fetch current localized strings map shortcut
    lang = st.session_state.selected_lang
    ui = labels[lang]


    st.markdown(f"<h1 style= 'text-align: center; color: #2e7d32;'>{ui['title']}</h1>", unsafe_allow_html = True)
    st.markdown(f"<p style= 'text-align: center; font-size: 1.2em;'>{ui['subtitle']}</p>", unsafe_allow_html = True)
    
    # for a sidebar of history
    with st.sidebar:
        st.header("⚙️ Settings")
        st.session_state.selected_lang = st.radio("Primary Language / मुख्य भाषा", ["English", "हिंदी", "मराठी"], index=["English", "हिंदी", "मराठी"].index(st.session_state.selected_lang))
        
        st.divider()
        if st.button("🗑️ Clear Chat History"):
            st.session_state_chat_history = []
            st.rerun()


# main interaction:
    tab1, tab2 = st.tabs([ui["tab1"], ui["tab2"]])

    with tab1:
        col1, col2 = st.columns([1,1])

        with col1:
            st.markdown(f"<div class= 'instruction-card'>{ui['step1']}</div><br>", unsafe_allow_html=True)
        # Multilingual Labels
            user_query = st.text_input(ui["input_label"])
            uploaded_image = st.file_uploader(ui["upload_label"], type=["jpg", "jpeg", "png"])
            recorded_audio = st.audio_input(ui["audio_label"])

            submit_btn = st.button(ui["btn_label"])

        with col2:
            st.markdown(f"<div class='instruction-card'>{ui['step2']}</div><br>", unsafe_allow_html=True)
            if submit_btn:
                # Build the Advanced System Instruction
                prompt_context = f"""
                You are 'GraminSetu', a helpful Indian rural assistant. 
                INSTRUCTION: Please respond strictly in {st.session_state.selected_lang}.
                Keep advice simple, practical, and respectful.
                    
                Previous Conversation Context for reference: 
                {str(st.session_state.chat_history[-2:])}
                """
                content_parts = [prompt_context]
                
                if user_query: content_parts.append(user_query)
                if uploaded_image:
                    img_bytes = uploaded_image.getvalue()
                    content_parts.append(types.Part.from_bytes(data=img_bytes, mime_type=uploaded_image.type))
                if recorded_audio:
                    audio_bytes = recorded_audio.getvalue()
                    content_parts.append(types.Part.from_bytes(data=audio_bytes, mime_type="audio/wav"))

                if len(content_parts) > 1:
                    with st.spinner("Conecting to Expert AI..."):
                        try:
                            response = client.models.generate_content(
                                model="gemini-2.5-flash", 
                                contents=content_parts
                            )
                            ans_text = response.text

                            st.subheader("✅ Recommendation:")
                            st.write(ans_text)
                            
                            # Voice switches to match the detected language
                            audio_path = asyncio.run(generate_voice(ans_text, st.session_state.selected_lang))
                            st.audio(audio_path, format= "audio/mp3", autoplay= True)
                            
                            st.session_state.chat_history.append({"user": user_query or "Audio/Image Input", "bot": ans_text})
                    
                        except Exception as e:
                            st.error(f"Error: {e}")
                else:
                    st.warning("Please provide input / कृपया प्रश्न विचारा।")

    with tab2:
        if not st.session_state.chat_history:
            st.info(ui["history_empty"])
        for chat in reversed(st.session_state.chat_history):
            with st.expander(f"Question: {chat['user'][:50]}..."):
                st.write(f"**You:** {chat['user']}")
                st.write(f"**GraminSetu:** {chat['bot']}")

if __name__ == "__main__":
    main()

#python -m streamlit run Gramsetu_SaurabhDike.py
