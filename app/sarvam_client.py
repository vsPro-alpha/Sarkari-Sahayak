import logging
import base64
import json
import httpx
from typing import Optional, Dict, Any, List
from app import config

logger = logging.getLogger("sarvam_client")
logging.basicConfig(level=logging.INFO)

class SarvamClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or config.SARVAM_API_KEY
        self.base_url = config.SARVAM_BASE_URL

    @property
    def has_api_key(self) -> bool:
        return bool(self.api_key and self.api_key.strip() and not self.api_key.startswith("your_"))

    def _get_headers(self) -> Dict[str, str]:
        headers = {}
        if self.api_key:
            headers["api-subscription-key"] = self.api_key
        return headers

    async def speech_to_text(
        self,
        audio_bytes: bytes,
        filename: str = "audio.wav",
        language_code: Optional[str] = None,
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Transcribe audio using Sarvam Saaras API (Speech-to-Text).
        """
        if not self.has_api_key:
            logger.warning("No Sarvam API key provided. Using simulation mode for STT.")
            return {
                "transcript": "नमस्ते, मेरी समस्या यह है कि मेरा पीएम किसान सम्मान निधि का पैसा पिछले छह महीने से नहीं आया है। मैंने पटवारी को भी बताया लेकिन कोई सुनवाई नहीं हुई। कृपया मेरी मदद करें।",
                "language_code": language_code or "hi-IN",
                "simulated": True
            }

        endpoint = f"{self.base_url}/speech-to-text"
        headers = self._get_headers()
        model_name = model or config.MODEL_STT

        files = {
            "file": (filename, audio_bytes, "audio/wav")
        }
        data = {
            "model": model_name
        }
        if language_code and language_code != "auto":
            data["language_code"] = language_code

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(endpoint, headers=headers, files=files, data=data)
                response.raise_for_status()
                result = response.json()
                return {
                    "transcript": result.get("transcript", ""),
                    "language_code": result.get("language_code", language_code or "auto"),
                    "simulated": False
                }
            except httpx.HTTPStatusError as e:
                logger.error(f"Sarvam STT HTTP error: {e.response.status_code} - {e.response.text}")
                raise RuntimeError(f"Sarvam STT failed ({e.response.status_code}): {e.response.text}")
            except Exception as e:
                logger.error(f"Sarvam STT exception: {str(e)}")
                raise

    async def text_to_speech(
        self,
        text: str,
        language_code: str = "hi-IN",
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Convert text into natural Indic speech using Sarvam Bulbul API.
        """
        if not self.has_api_key:
            logger.warning("No Sarvam API key provided. Skipping live Bulbul TTS audio generation.")
            return {
                "audio_base64": None,
                "language_code": language_code,
                "simulated": True,
                "message": "Add SARVAM_API_KEY in Settings or .env to enable realistic Bulbul voice playback."
            }

        endpoint = f"{self.base_url}/text-to-speech"
        headers = {
            **self._get_headers(),
            "Content-Type": "application/json"
        }
        payload = {
            "text": text[:1500],  # keep within API payload limit
            "model": model or config.MODEL_TTS,
            "language_code": language_code
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(endpoint, headers=headers, json=payload)
                response.raise_for_status()
                result = response.json()
                audios = result.get("audios", [])
                audio_base64 = audios[0] if audios else None
                return {
                    "audio_base64": audio_base64,
                    "language_code": language_code,
                    "simulated": False
                }
            except httpx.HTTPStatusError as e:
                logger.error(f"Sarvam TTS HTTP error: {e.response.status_code} - {e.response.text}")
                return {"audio_base64": None, "error": f"{e.response.status_code}: {e.response.text}", "simulated": False}
            except Exception as e:
                logger.error(f"Sarvam TTS exception: {str(e)}")
                return {"audio_base64": None, "error": str(e), "simulated": False}

    async def translate(
        self,
        input_text: str,
        source_language_code: str = "auto",
        target_language_code: str = "en-IN",
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Translate between Indian languages and English using Sarvam Translate.
        """
        if not self.has_api_key:
            return {
                "translated_text": f"[Translated to {target_language_code}]: {input_text}",
                "simulated": True
            }

        endpoint = f"{self.base_url}/translate"
        headers = {
            **self._get_headers(),
            "Content-Type": "application/json"
        }
        payload = {
            "input": input_text,
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
            "model": model or config.MODEL_TRANSLATE
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(endpoint, headers=headers, json=payload)
                response.raise_for_status()
                result = response.json()
                return {
                    "translated_text": result.get("translated_text", ""),
                    "simulated": False
                }
            except httpx.HTTPStatusError as e:
                logger.error(f"Sarvam Translate error: {e.response.status_code} - {e.response.text}")
                return {"translated_text": input_text, "error": str(e), "simulated": False}
            except Exception as e:
                logger.error(f"Sarvam Translate exception: {str(e)}")
                return {"translated_text": input_text, "error": str(e), "simulated": False}

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.3
    ) -> str:
        """
        Execute chat completions using Sarvam-105B Indic LLM (OpenAI-compatible endpoint).
        """
        if not self.has_api_key:
            # We will use an intelligent local rule-based synthesizer when API key is missing
            return ""

        endpoint = f"{self.base_url}/v1/chat/completions"
        headers = {
            **self._get_headers(),
            "Content-Type": "application/json"
        }
        payload = {
            "model": model or config.MODEL_CHAT,
            "messages": messages,
            "temperature": temperature
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(endpoint, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                choices = data.get("choices", [])
                if choices:
                    return choices[0].get("message", {}).get("content", "")
                return ""
            except Exception as e:
                logger.error(f"Sarvam Chat completion error: {str(e)}")
                return ""
