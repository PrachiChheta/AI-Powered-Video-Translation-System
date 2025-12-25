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
        print(f"Processing video: {video_path}")
        print(f"Translation: {source_language} -> {target_language}")
        
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
        
        print(f"Translating {len(transcript_segments)} segments...")
        for i, segment in enumerate(transcript_segments, 1):
            print(f"Translating segment {i}/{len(transcript_segments)}")
            
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
        
        print("Video processing complete!")
        
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
        
        print(f"Transcripts saved to {output_dir}")