from dotenv import load_dotenv
import os
load_dotenv()

class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

    ALLOWED_MODEL_NAMES = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "llama3-70b-8192",      # ← add this
        "llama3-8b-8192",       # ← add this
    ]

settings = Settings()