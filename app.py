import streamlit as st
import io
import asyncio
import time
from streamlit_mic_recorder import mic_recorder
from openai import AsyncOpenAI
from openai import APIError
from dotenv import load_dotenv
import os

#CONFIGURATION & INITIALIZATION 

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
aclient = AsyncOpenAI(api_key=openai_api_key) 

# Custom CSS - Minimal white space
st.markdown("""
<style>
    /* Dark gradient background */
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #7e22ce 100%);
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 900px;
    }
    
    /* Header */
    .voice-header {
        text-align: center;
        color: white;
        padding: 20px;
        font-size: 2.5em;
        font-weight: bold;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.4);
        margin-bottom: 50px;
    }
    
    /* Chat messages container */
    .chat-messages {
        min-height: 300px;
        max-height: 500px;
        overflow-y: auto;
        padding: 20px 10px;
        margin-bottom: 20px;
    }
    
    .chat-messages::-webkit-scrollbar {
        width: 6px;
    }
    
    .chat-messages::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
    }
    
    .chat-messages::-webkit-scrollbar-thumb {
        background: rgba(255,255,255,0.3);
        border-radius: 10px;
    }
    
    .user-msg {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 14px 18px;
        border-radius: 18px 18px 5px 18px;
        margin: 12px 0 12px auto;
        max-width: 75%;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        display: block;
        clear: both;
        text-align: left;
    }
    
    .bot-msg {
        background: rgba(255, 255, 255, 0.95);
        color: #1a1a1a;
        padding: 14px 18px;
        border-radius: 18px 18px 18px 5px;
        margin: 12px auto 12px 0;
        max-width: 75%;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        display: block;
        clear: both;
        text-align: left;
    }
    
    /* Recording controls - transparent background */
    .recorder-section {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    
    .status-indicator {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 10px 20px;
        border-radius: 25px;
        margin-bottom: 15px;
        font-weight: 600;
        font-size: 1.1em;
    }
    
    .status-processing {
        background: rgba(255, 165, 0, 0.2);
        color: #ffa500;
        border: 2px solid rgba(255, 165, 0, 0.4);
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }
    
    .helper-text {
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.95em;
        margin-top: 12px;
    }
    
    /* Welcome screen */
    .welcome-screen {
        text-align: center;
        color: white;
        padding: 60px 20px;
    }
    
    .welcome-screen h2 {
        font-size: 2.2em;
        margin-bottom: 15px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .welcome-screen p {
        font-size: 1.2em;
        opacity: 0.9;
        margin: 10px 0;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Hide the specific audio player used for automatic TTS playback */
    .hidden-autoplay-audio > div {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "processing" not in st.session_state:
    st.session_state.processing = False
if "last_audio_bytes" not in st.session_state:
    st.session_state.last_audio_bytes = None
if "session_id" not in st.session_state:
    st.session_state.session_id = 0
    
# State for reliable, single-run auto-playback of the TTS audio
if "tts_to_play" not in st.session_state:
    st.session_state.tts_to_play = None


# TTS PLAYBACK SECTION
st.markdown('<div class="hidden-autoplay-audio">', unsafe_allow_html=True)
if st.session_state.tts_to_play is not None:
    # The autoplay attribute handles the voice playback automatically after a rerun
    st.audio(st.session_state.tts_to_play, format="audio/mp3", autoplay=True)
    st.toast(" Playing AI voice response.")
    st.session_state.tts_to_play = None # Clear the state after attempting playback
st.markdown('</div>', unsafe_allow_html=True)



st.markdown('<div class="voice-header">🤖 AI Voice Assistant</div>', unsafe_allow_html=True)

# Chat area
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class="welcome-screen">
        <p>Your AI voice assistant is ready</p>
        <p style="font-size: 1em; margin-top: 20px;"> Click the microphone below to start talking</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Display messages with user/bot styling
    for i, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            st.markdown(f'<div class="user-msg"> {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-msg"> {msg["content"]}</div>', unsafe_allow_html=True)
            
            if "latency" in msg:
                # Display the full pipeline latency
                st.markdown(f'<small style="color: rgba(255,255,255,0.7); margin-left: 5px;"> ⚡Total Latency: {msg["latency"]:.2f}s</small>', unsafe_allow_html=True)

# Recording section
# st.markdown('<div class="recorder-section">', unsafe_allow_html=True)

# Status indicator
if st.session_state.processing:
    st.markdown('<div class="status-indicator status-processing"> Processing your voice...</div>', unsafe_allow_html=True)

# Microphone recorder
recorder_key = f"recorder_{st.session_state.session_id}"

audio = mic_recorder(
    start_prompt="Start Recording",
    stop_prompt="Stop Recording",
    key=recorder_key
)

st.markdown('<p class="helper-text">Click Start • Speak clearly • Click Stop</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Process audio
if audio and not st.session_state.processing:
    audio_bytes = audio.get("bytes")
    
    if audio_bytes and audio_bytes != st.session_state.last_audio_bytes:
        st.session_state.last_audio_bytes = audio_bytes
        st.session_state.processing = True
        
        # Create placeholders for immediate feedback
        progress = st.progress(0)
        status_text = st.empty()
        
        start_time = time.time()
        
        async def process():
            try:
                # Step 1: Whisper STT (Speech-to-Text)
                status_text.info("Transcribing...")
                progress.progress(30)
                
                audio_file = io.BytesIO(audio_bytes)
                audio_file.name = "audio.wav"
                
                transcript = await aclient.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
                user_text = transcript.strip()
                
                if not user_text:
                    status_text.error("No speech detected")
                    return None
                
                # Step 2: GPT-4o-mini (LLM)
                status_text.info("Thinking...")
                progress.progress(60)
                
                # Send the last 10 messages for context (increased from 4)
                messages = [{"role": "system", "content": "You are a friendly, concise voice assistant. Your responses must be extremely brief."}]
                messages.extend([{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-30:]])
                messages.append({"role": "user", "content": user_text})
                
                completion = await aclient.chat.completions.create(
                    model="gpt-4o-mini", 
                    messages=messages,
                    max_tokens=100, # REDUCED from 60 to 40 for speed
                    temperature=0.7
                )
                reply = completion.choices[0].message.content.strip()
                
                # Step 3: TTS (Text-to-Speech)
                status_text.info("Creating voice...")
                progress.progress(90)
                
                speech = await aclient.audio.speech.create(
                    model="tts-1",
                    voice="alloy",
                    input=reply,
                    speed=1.25 # INCREASED from 1.15 to 1.25 for aggressive speed reduction
                )
                audio_response = speech.read()
                
                progress.progress(100)
                
                return {
                    "user": user_text,
                    "assistant": reply,
                    "audio": audio_response
                }
                
            except APIError as e:
                status_text.error(f"API Error: {e.status_code}. Check API key or rate limits.")
                return None
            except Exception as e:
                status_text.error(f" An unexpected error occurred: {str(e)}")
                return None
        
        # Run pipeline synchronously (Streamlit requirement)
        result = asyncio.run(process())
        
        if result:
            elapsed = time.time() - start_time
            
            # Save messages
            st.session_state.messages.append({"role": "user", "content": result["user"]})
            st.session_state.messages.append({
                "role": "assistant",
                "content": result["assistant"],
                "latency": elapsed,
                "audio_bytes": result["audio"]
            })
            
            status_text.success(f"Done in {elapsed:.1f}s")
            
            # Set the audio bytes for the top-level auto-playback before rerun
            st.session_state.tts_to_play = result["audio"]
            
            # Reset state and trigger rerun to display new chat and play audio
            st.session_state.processing = False
            st.session_state.session_id += 1
            time.sleep(0.8)
            st.rerun()
        else:
            # If processing failed, reset state to allow new recording
            st.session_state.processing = False
            st.session_state.session_id += 1
            time.sleep(0.5)
            st.rerun()
        
        # Clear immediate feedback elements
        progress.empty()
        status_text.empty()

# Sidebar
with st.sidebar:
    st.markdown("###  Controls")
    
    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.processing = False
        st.session_state.last_audio_bytes = None
        st.session_state.session_id = 0
        st.session_state.tts_to_play = None
        st.rerun()
    
    if len(st.session_state.messages) > 0:
        chat_text = "\n\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages])
        st.download_button(
            "Export Chat",
            chat_text,
            file_name=f"chat_{int(time.time())}.txt",
            use_container_width=True
        )
    
    st.markdown("---")
    
    st.markdown(f"""
    ###  Stats
    
    **Messages:** {len(st.session_state.messages)} 
    **Status:** {"Processing" if st.session_state.processing else "Ready"}
    
    ### Performance
    
    **Target:** under 3 seconds 
    **LLM Model:** GPT-4o-mini 
    **TTS Speed:** 1.25 (Aggressively Optimized for speed) 
    
    ### Tips for Low Latency
    
     Keep speech **short** and clear. 
     Ensure a **fast internet** connection. 
     Responses are limited to a **single, short sentence**. 
    """)
    
    with st.expander(" Debug"):
        st.json({
            "processing": st.session_state.processing,
            "messages": len(st.session_state.messages),
            "session_id": st.session_state.session_id
        })

# Footer
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.7); padding: 20px; margin-top: 20px;">
    <small>⚡ Powered by OpenAI | Optimized for Low-Latency Voice AI</small>
</div>
""", unsafe_allow_html=True)
