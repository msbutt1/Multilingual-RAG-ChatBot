"""
Translation module using Google Cloud Translation API
"""
import os
from typing import Tuple
from google.cloud import translate_v2 as translate


class TranslationService:
    """Handles language detection and translation using GCP Translation API"""
    
    def __init__(self):
        """Initialize the translation client."""
        self.client = translate.Client()
    
    def detect_language(self, text: str) -> str:
        """
        Detect the language of the input text
        
        Args:
            text: Input text to detect language
            
        Returns:
            Language code (e.g., 'en', 'es', 'fr')
        """
        result = self.client.detect_language(text)
        return result['language']
    
    def translate_to_english(self, text: str) -> str:
        """
        Translate text to English
        
        Args:
            text: Input text to translate
            
        Returns:
            Translated English text
        """
        if self.detect_language(text) == 'en':
            return text
        
        result = self.client.translate(text, target_language='en')
        return result['translatedText']
    
    def translate_from_english(self, text: str, target_language: str) -> str:
        """
        Translate English text to target language
        
        Args:
            text: English text to translate
            target_language: Target language code (e.g., 'es', 'fr')
            
        Returns:
            Translated text in target language
        """
        if target_language == 'en':
            return text
        
        result = self.client.translate(text, target_language=target_language)
        return result['translatedText']
    
    def translate_with_detection(self, text: str) -> Tuple[str, str]:
        """
        Detect language and translate to English in one call
        
        Args:
            text: Input text
            
        Returns:
            Tuple of (detected_language, translated_text)
        """
        detected_lang = self.detect_language(text)
        translated = self.translate_to_english(text)
        return detected_lang, translated

