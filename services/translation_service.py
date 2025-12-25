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