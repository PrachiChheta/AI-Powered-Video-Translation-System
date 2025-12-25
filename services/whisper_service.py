import whisper
from typing import List, Dict
from config.settings import settings

class WhisperService:
    def __init__(self):
        self.model = None
    
    def load_model(self):
        """Load Whisper model"""
        if self.model is None:
            print(f"Loading Whisper model: {settings.WHISPER_MODEL}")
            self.model = whisper.load_model(settings.WHISPER_MODEL)
        return self.model
    
    def transcribe_video(self, video_path: str) -> List[Dict]:
        """Transcribe video audio to text with timestamps"""
        print(f"Transcribing video: {video_path}")
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
        
        print(f"Transcription complete: {len(transcript)} segments")
        return transcript
