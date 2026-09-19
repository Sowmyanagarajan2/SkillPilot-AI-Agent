Deployed Link : https://skillpilot-ai-agent-nstfhqrnomjovkuefznrff.streamlit.app/

Another Models : GPT-Transcribe, GPT-4o Transcribe, and GPT-4o mini Transcribe.

Flow of the AI Agent:

                 QUESTION
                     ↓
              🤖 SKILLPILOT
                     ↓
              "What do I need?"
                     ↓
        ┌────────────┴────────────┐
        ↓                         ↓
  Student Analysis           Career Knowledge
   Pandas + NumPy                  RAG
        ↓                         ↓
        └────────────┬────────────┘
                     ↓
                 🧠 LLM
                     ↓
          Personalized Answer
VS Code
   │
   ├── Python
   │
   ├── LangChain
   ├── LangGraph
   ├── RAG + FAISS
   ├── Pandas + NumPy
   └── Streamlit
            ↓
      🌐 Browser
   localhost:8501
