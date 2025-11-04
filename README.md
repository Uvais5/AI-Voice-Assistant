# 🎙️ AI Voice Assistant  
> 🧠 Whisper STT → 💬 GPT-4o-mini → 🔊 TTS  
> A real-time, low-latency voice chatbot built with Streamlit and OpenAI APIs.

---

## 🌟 Overview  

This project is an **AI Voice Assistant** powered by OpenAI's latest APIs and optimized for **speed** and **smooth user interaction**.  
Users can speak directly into the mic 🎤, get transcriptions using **Whisper STT**, receive instant replies from **GPT-4o-mini**, and hear responses back via **TTS** — all inside an elegant, minimal **Streamlit UI**.  

The system is fully asynchronous ⚡ and built for ultra-low latency voice interaction.  

---

## 🖥️ Features  

 **🎤 Real-Time Speech Recognition** using `Whisper-1`  
 **🤖 AI Chat Responses** powered by `GPT-4o-mini`  
 **🔊 Instant Text-to-Speech (TTS)** via `tts-1`  
 **⚡ Optimized Latency** (avg. < 3 seconds)  
 **📂 Chat Export** option to save your conversations  
 **🧭 Clear & Restart Controls**  
 **🎨 Stunning Gradient UI** with smooth chat bubbles  

---

## 🧰 Tech Stack  

| Component | Technology |
|------------|-------------|
| 🎛️ Frontend | [Streamlit](https://streamlit.io) |
| 🎙️ Mic Recorder | [streamlit-mic-recorder](https://pypi.org/project/streamlit-mic-recorder/) |
| 🧠 AI Models | [OpenAI GPT-4o-mini](https://platform.openai.com/docs) |
| 🗣️ Speech-to-Text | Whisper-1 |
| 🔉 Text-to-Speech | TTS-1 |
| ⚙️ Environment Management | python-dotenv |
| 🪶 Styling | Custom CSS |

---

## 🚀 Setup Instructions  

### 1. Clone the repository  
```bash
git clone https://github.com/Uvais5/AI-Voice-Assistant
cd AI-Voice-Assistant
```
### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate
```
### 3. Install dependencies
```
 pip install -r requirements.txt
```
### 4. Enter Api key in .env file
```
OPENAI_API_KEY=your_api_key_here

```
### 4. Run the App
```
streamlit run app.py
```

