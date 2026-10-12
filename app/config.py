import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from project root
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY", "").strip()
SARVAM_BASE_URL = os.getenv("SARVAM_BASE_URL", "https://api.sarvam.ai").rstrip("/")

# Default Models
MODEL_STT = os.getenv("MODEL_STT", "saaras:v4")
MODEL_TTS = os.getenv("MODEL_TTS", "bulbul:v4-flash")
MODEL_TRANSLATE = os.getenv("MODEL_TRANSLATE", "mayura:v1")
MODEL_CHAT = os.getenv("MODEL_CHAT", "sarvam-105b")

SUPPORTED_LANGUAGES = {
    "hi-IN": {"name": "Hindi", "native": "हिन्दी"},
    "ta-IN": {"name": "Tamil", "native": "தமிழ்"},
    "te-IN": {"name": "Telugu", "native": "తెలుగు"},
    "bn-IN": {"name": "Bengali", "native": "বাংলা"},
    "mr-IN": {"name": "Marathi", "native": "मराठी"},
    "gu-IN": {"name": "Gujarati", "native": "ગુજરાતી"},
    "kn-IN": {"name": "Kannada", "native": "ಕನ್ನಡ"},
    "ml-IN": {"name": "Malayalam", "native": "മലയാളം"},
    "pa-IN": {"name": "Punjabi", "native": "ਪੰਜਾਬੀ"},
    "od-IN": {"name": "Odia", "native": "ଓଡ଼ିଆ"},
    "en-IN": {"name": "English (India)", "native": "English"}
}
