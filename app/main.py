import os
import io
import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app import config
from app.sarvam_client import SarvamClient
from app.scheme_engine import match_schemes, GOVERNMENT_SCHEMES
from app.grievance_engine import analyze_and_draft_grievance
from app.doc_parser import parse_citizen_document

logger = logging.getLogger("main")
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Sarkari Sahayak & Grievance Drafter",
    description="Multilingual Voice-First Citizen Agent powered by Sarvam AI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Client
sarvam = SarvamClient()

# Static folder setup
STATIC_DIR = config.BASE_DIR / "static"
if not STATIC_DIR.exists():
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Request Models
class UserProfileRequest(BaseModel):
    age: Optional[int] = 32
    gender: Optional[str] = "male"
    occupation: Optional[str] = "farmer"
    annual_income_lakhs: Optional[float] = 1.5
    has_land: Optional[bool] = True
    is_rural: Optional[bool] = True
    is_taxpayer: Optional[bool] = False
    state: Optional[str] = "Uttar Pradesh"
    district: Optional[str] = "Varanasi"
    language_code: Optional[str] = "hi-IN"

class GrievanceDraftRequest(BaseModel):
    raw_text: str
    citizen_name: Optional[str] = "Ramesh Kumar"
    location: Optional[str] = "Varanasi, Uttar Pradesh"
    contact_phone: Optional[str] = "+91 98765 43210"
    language_code: Optional[str] = "hi-IN"
    generate_audio: Optional[bool] = True

class TTSRequest(BaseModel):
    text: str
    language_code: Optional[str] = "hi-IN"

class SettingsUpdateRequest(BaseModel):
    api_key: str

# Endpoints
@app.get("/", response_class=FileResponse)
async def serve_home():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return HTMLResponse("<h2>Sarkari Sahayak is initializing...</h2>")

@app.get("/api/health")
async def get_health():
    return {
        "status": "online",
        "sarvam_api_connected": sarvam.has_api_key,
        "models": {
            "stt": config.MODEL_STT,
            "tts": config.MODEL_TTS,
            "translate": config.MODEL_TRANSLATE,
            "chat": config.MODEL_CHAT
        },
        "supported_languages": config.SUPPORTED_LANGUAGES,
        "schemes_count": len(GOVERNMENT_SCHEMES)
    }

@app.post("/api/settings")
async def update_settings(req: SettingsUpdateRequest):
    global sarvam
    sarvam.api_key = req.api_key.strip()
    return {
        "success": True,
        "sarvam_api_connected": sarvam.has_api_key,
        "message": "Sarvam API Key updated successfully!" if sarvam.has_api_key else "Key removed; running in simulation mode."
    }

@app.get("/api/schemes/list")
async def list_schemes(category: Optional[str] = None):
    if category and category != "all":
        filtered = [s for s in GOVERNMENT_SCHEMES if category.lower() in s["category"].lower()]
        return {"schemes": filtered}
    return {"schemes": GOVERNMENT_SCHEMES}

@app.post("/api/voice/transcribe")
async def transcribe_voice(
    file: UploadFile = File(...),
    language_code: Optional[str] = Form("hi-IN")
):
    try:
        content = await file.read()
        filename = file.filename or "recording.wav"
        result = await sarvam.speech_to_text(content, filename=filename, language_code=language_code)
        return {
            "success": True,
            "transcript": result.get("transcript", ""),
            "language_code": result.get("language_code", language_code),
            "simulated": result.get("simulated", False)
        }
    except Exception as e:
        logger.error(f"STT Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/voice/synthesize")
async def synthesize_speech(req: TTSRequest):
    try:
        result = await sarvam.text_to_speech(req.text, language_code=req.language_code or "hi-IN")
        return {
            "success": True,
            "audio_base64": result.get("audio_base64"),
            "simulated": result.get("simulated", False),
            "message": result.get("message")
        }
    except Exception as e:
        logger.error(f"TTS Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/schemes/match")
async def match_citizen_schemes(req: UserProfileRequest):
    try:
        profile_dict = req.dict()
        match_result = match_schemes(profile_dict)
        
        # Audio guidance generation
        audio_base64 = None
        spoken_text = match_result["hindi_summary"] if req.language_code.startswith("hi") else match_result["english_summary"]
        tts_res = await sarvam.text_to_speech(spoken_text, language_code=req.language_code or "hi-IN")
        if tts_res.get("audio_base64"):
            audio_base64 = tts_res["audio_base64"]

        return {
            "success": True,
            **match_result,
            "spoken_audio": audio_base64
        }
    except Exception as e:
        logger.error(f"Scheme Matching Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/grievance/draft")
async def draft_grievance(req: GrievanceDraftRequest):
    try:
        draft = analyze_and_draft_grievance(
            raw_text=req.raw_text,
            citizen_name=req.citizen_name or "Aggrieved Citizen",
            location=req.location or "Uttar Pradesh, India",
            contact_phone=req.contact_phone or "+91 98765 43210"
        )

        audio_base64 = None
        if req.generate_audio:
            tts_res = await sarvam.text_to_speech(draft["spoken_summary_hi"], language_code=req.language_code or "hi-IN")
            if tts_res.get("audio_base64"):
                audio_base64 = tts_res["audio_base64"]

        return {
            "success": True,
            **draft,
            "spoken_audio": audio_base64
        }
    except Exception as e:
        logger.error(f"Grievance Draft Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/document/parse")
async def parse_document(
    file: UploadFile = File(...),
    auto_match_schemes: Optional[bool] = Form(True)
):
    try:
        content = await file.read()
        filename = file.filename or "doc.jpg"
        
        # Try decoding as text if text file, or use heuristic parser
        text_content = ""
        try:
            text_content = content.decode("utf-8", errors="ignore")
        except Exception:
            text_content = ""
        
        if not text_content or len(text_content.strip()) < 10:
            # Fallback simulated text for binary image upload
            text_content = f"UIDAI Government of India\nName: Ramesh Kumar\nDOB: 1988\nGender: Male\nAddress: Gram Panchayat Kalyanpur, District Varanasi, Uttar Pradesh 221001\nKhasra No: 412/1 (2.4 Hectares agricultural land)\nAnnual income: 1.2 Lakh"

        parsed = parse_citizen_document(text_content, filename=filename)
        
        scheme_matches = None
        if auto_match_schemes:
            scheme_matches = match_schemes(parsed["extracted_profile"])

        return {
            "success": True,
            **parsed,
            "matched_schemes": scheme_matches
        }
    except Exception as e:
        logger.error(f"Document Parse Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
