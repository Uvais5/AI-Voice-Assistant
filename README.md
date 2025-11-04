#Low-Latency AI Voice Assistant (Streamlit/OpenAI)

This project implements an **aggressively optimized voice conversation system** designed for near-real-time performance. It uses Streamlit for the UI and the OpenAI API for a complete pipeline: Speech-to-Text (STT), Large Language Model (LLM) response, and Text-to-Speech (TTS).

The primary goal of this configuration is to minimize the total latency to **under 3 seconds** for a fluid, instantaneous user experience.

---

## 🚀 Key Features

* **Ultra-Low Latency Focus:** Achieved through aggressive configuration of LLM and TTS parameters.
* **Complete Voice Pipeline:** Integrates Whisper (STT), GPT-4o-mini (LLM), and TTS-1 (TTS).
* **Fast LLM:** Uses **GPT-4o-mini** and limits output to **40 tokens** (one short sentence) for speed.
* **High-Speed TTS:** Generates audio at a rate of **1.25x** normal speed.
* **Extended Context:** The LLM retains the **last 10 turns** of conversation history.
* **Asynchronous API Calls:** Utilizes `AsyncOpenAI` for efficient processing.
* **Streamlit UI:** Provides a simple, modern interface with real-time status updates.

---

## 🛠️ Setup and Installation

### 1. Prerequisites

Ensure you have Python installed.

### 2. Install Dependencies

Install the required Python libraries using pip:

```bash
pip install streamlit openai streamlit-mic-recorder
