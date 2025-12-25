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