import streamlit as st

from audio_recorder_streamlit import audio_recorder

from openai import OpenAI

from dotenv import load_dotenv

import tempfile
import os

from agent import ask_agent


load_dotenv()

client = OpenAI()


# --------------------------------
# Page
# --------------------------------
import os
import tempfile
import streamlit as st

from openai import OpenAI
from audio_recorder_streamlit import audio_recorder

from agent import ask_agent


client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)
st.set_page_config(
    page_title="SkillPilot AI",
    page_icon="🤖",
    layout="centered"
)


st.title("🤖 SkillPilot AI")

st.subheader(
    "AI Learning & Career Agent"
)

st.write(
    "Ask questions using your voice or type them below."
)


# --------------------------------
# Student
# --------------------------------

student = st.selectbox(
    "Select Student",
    [
        "Arun",
        "Priya",
        "Rahul",
        "Divya",
        "Kavin",
        "Meena"
    ]
)


# --------------------------------
# Voice
# --------------------------------

st.write("### 🎙️ Ask the Agent")

audio_bytes = audio_recorder(
    text="Click to record",
    recording_color="#ff4b4b",
    neutral_color="#6c757d",
    icon_name="microphone",
    icon_size="2x"
)


voice_question = None


if audio_bytes:

    st.audio(
        audio_bytes,
        format="audio/wav"
    )

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    ) as audio_file:

        audio_file.write(audio_bytes)

        audio_path = audio_file.name


    with open(
        audio_path,
        "rb"
    ) as audio:

        transcription = client.audio.transcriptions.create(
        model="gpt-4o-mini-transcribe",
        file=audio)


    voice_question = transcription.text

    os.remove(audio_path)

    st.success(
        "You said: " + voice_question
    )


# --------------------------------
# Text Input
# --------------------------------

typed_question = st.text_input(
    "Or type your question",
    placeholder=(
        "Example: What should Arun learn next?"
    )
)


# --------------------------------
# Select Question
# --------------------------------

question = None

if voice_question:

    question = voice_question

elif typed_question:

    question = typed_question


# --------------------------------
# Run Agent
# --------------------------------

if st.button(
    "🚀 Ask SkillPilot",
    use_container_width=True
):

    if not question:

        st.warning(
            "Please type a question or record your voice."
        )

    else:

        # Automatically add selected student
        final_question = f"""
Selected student: {student}

User question:
{question}
"""

        with st.spinner(
            "🤖 Agent is thinking..."
        ):

            answer = ask_agent(
                final_question
            )


        st.success(
            "Agent completed the task!"
        )


        st.write("### 🤖 Agent Response")

        st.write(answer)


        # --------------------------------
        # Text To Speech
        # --------------------------------

        with st.spinner(
            "🔊 Creating voice response..."
        ):

            speech = client.audio.speech.create(
                model="gpt-4o-mini-tts",
                voice="alloy",
                input=answer
            )


            speech_path = "response.mp3"

            speech.stream_to_file(
                speech_path
            )


        st.audio(
            speech_path,
            format="audio/mp3"
        )