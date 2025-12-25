# ============================================================================
# FILE: main.py (Root FastAPI Application)
# ============================================================================
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from pathlib import Path
import shutil
from typing import Optional

from services.video_service import VideoTranslationService
from models.schemas import TranslationResponse, ErrorResponse
from config.settings import settings

app = FastAPI(
    title="Video Translation API",
    description="Transcribe and translate video audio using AI",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize service
video_service = VideoTranslationService()

# Create required directories
Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
Path(settings.OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "Video Translation API", "status": "running"}

@app.post("/api/translate-video", response_model=TranslationResponse)
async def translate_video(
    file: UploadFile = File(...),
    source_language: str = Form(...),
    target_language: str = Form(...)
):
    """
    Upload a video file and translate its audio content
    """
    if not file.content_type.startswith('video/'):
        raise HTTPException(status_code=400, detail="File must be a video")
    
    # Save uploaded file
    file_path = Path(settings.UPLOAD_DIR) / file.filename
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process video
        result = await video_service.process_video(
            str(file_path),
            source_language,
            target_language
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup uploaded file
        if file_path.exists():
            file_path.unlink()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# ============================================================================
# FILE: config/settings.py (Configuration)
# ============================================================================
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    UPLOAD_DIR: str = "uploads"
    OUTPUT_DIR: str = "outputs"
    WHISPER_MODEL: str = "small"
    GPT_MODEL: str = "gpt-4"
    MAX_FILE_SIZE: int = 500 * 1024 * 1024  # 500MB
    
    class Config:
        env_file = ".env"

settings = Settings()


# ============================================================================
# FILE: models/schemas.py (Pydantic Models)
# ============================================================================
from pydantic import BaseModel
from typing import List, Optional

class TranscriptSegment(BaseModel):
    sentence: str
    timestamp_start: float
    timestamp_end: float

class TranslationResponse(BaseModel):
    success: bool
    original_transcript: str
    translated_transcript: str
    segments: List[TranscriptSegment]
    message: str

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    detail: Optional[str] = None


# ============================================================================
# FILE: services/whisper_service.py (Whisper Transcription)
# ============================================================================
import whisper
from typing import List, Dict
from config.settings import settings

class WhisperService:
    def __init__(self):
        self.model = None
    
    def load_model(self):
        """Load Whisper model"""
        if self.model is None:
            self.model = whisper.load_model(settings.WHISPER_MODEL)
        return self.model
    
    def transcribe_video(self, video_path: str) -> List[Dict]:
        """Transcribe video audio to text with timestamps"""
        model = self.load_model()
        
        # Transcribe with detailed timestamps
        result = model.transcribe(video_path, verbose=True)
        
        # Process segments into sentences with timestamps
        transcript = []
        sentence = ""
        start_time = 0
        
        for segment in result["segments"]:
            if segment["start"] != start_time and sentence:
                transcript.append({
                    "sentence": sentence.strip() + ".",
                    "timestamp_start": start_time,
                    "timestamp_end": segment["start"]
                })
                sentence = ""
                start_time = segment["start"]
            
            sentence += segment["text"] + " "
        
        # Add final sentence
        if sentence:
            transcript.append({
                "sentence": sentence.strip() + ".",
                "timestamp_start": start_time,
                "timestamp_end": result["segments"][-1]["end"]
            })
        
        return transcript


# ============================================================================
# FILE: services/translation_service.py (GPT Translation)
# ============================================================================
from openai import OpenAI
from config.settings import settings

class TranslationService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def translate_text(
        self, 
        text: str, 
        source_language: str, 
        target_language: str
    ) -> str:
        """Translate text using GPT"""
        response = self.client.chat.completions.create(
            model=settings.GPT_MODEL,
            messages=[
                {"role": "system", "content": "You are a professional translator."},
                {
                    "role": "user",
                    "content": f"Translate the following {source_language} text to {target_language}. "
                              f"Keep the translation natural and suitable for video subtitles. "
                              f"Return only the translated text without any explanation: '{text}'"
                }
            ],
            max_tokens=1500,
            temperature=0.3
        )
        
        translated_text = response.choices[0].message.content if response.choices else text
        return translated_text.strip()


# ============================================================================
# FILE: services/video_service.py (Main Video Processing)
# ============================================================================
from typing import Dict
from pathlib import Path

from services.whisper_service import WhisperService
from services.translation_service import TranslationService
from models.schemas import TranslationResponse, TranscriptSegment
from config.settings import settings

class VideoTranslationService:
    def __init__(self):
        self.whisper_service = WhisperService()
        self.translation_service = TranslationService()
    
    async def process_video(
        self,
        video_path: str,
        source_language: str,
        target_language: str
    ) -> TranslationResponse:
        """
        Complete workflow:
        1. Transcribe video audio
        2. Translate transcription
        3. Format and return results
        """
        # Step 1: Transcribe video
        transcript_segments = self.whisper_service.transcribe_video(video_path)
        
        # Step 2: Create formatted original transcript
        original_lines = []
        for segment in transcript_segments:
            line = f"{segment['timestamp_start']:.2f}s to {segment['timestamp_end']:.2f}s: {segment['sentence']}"
            original_lines.append(line)
        
        original_transcript = "\n".join(original_lines)
        
        # Step 3: Translate each segment
        translated_lines = []
        translated_segments = []
        
        for segment in transcript_segments:
            translated_text = self.translation_service.translate_text(
                segment['sentence'],
                source_language,
                target_language
            )
            
            line = f"{segment['timestamp_start']:.2f}s to {segment['timestamp_end']:.2f}s: {translated_text}"
            translated_lines.append(line)
            
            translated_segments.append(TranscriptSegment(
                sentence=translated_text,
                timestamp_start=segment['timestamp_start'],
                timestamp_end=segment['timestamp_end']
            ))
        
        translated_transcript = "\n".join(translated_lines)
        
        # Step 4: Save to files
        self._save_transcripts(original_transcript, translated_transcript)
        
        return TranslationResponse(
            success=True,
            original_transcript=original_transcript,
            translated_transcript=translated_transcript,
            segments=translated_segments,
            message=f"Successfully translated from {source_language} to {target_language}"
        )
    
    def _save_transcripts(self, original: str, translated: str):
        """Save transcripts to files"""
        output_dir = Path(settings.OUTPUT_DIR)
        
        with open(output_dir / "original_transcript.txt", "w", encoding="utf-8") as f:
            f.write(original)
        
        with open(output_dir / "translated_transcript.txt", "w", encoding="utf-8") as f:
            f.write(translated)


