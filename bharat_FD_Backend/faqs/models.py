from django.db import models
from ckeditor.fields import RichTextField
from django.core.cache import cache
from googletrans import Translator
import json

translator = Translator()

class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField()
    translations = models.JSONField(default=dict)  

    def translate_text(self, text, lang_code):
        try:
            return translator.translate(text, dest=lang_code).text
        except Exception:
            return translator.translate(text, dest='en').text  
    
    def get_translated_question(self, lang_code):
        return self.translations.get(f'question_{lang_code}', self.question)
    
    def get_translated_answer(self, lang_code):
        return self.translations.get(f'answer_{lang_code}', self.answer)
    
    def save(self, *args, **kwargs):
        supported_languages = ['hi', 'bn', 'fr', 'es']  
        for lang in supported_languages:
            if f'question_{lang}' not in self.translations:
                self.translations[f'question_{lang}'] = self.translate_text(self.question, lang)
            if f'answer_{lang}' not in self.translations:
                self.translations[f'answer_{lang}'] = self.translate_text(self.answer, lang)
        cache.set(f'faq_{self.id}', self.translations, timeout=86400)  
        super().save(*args, **kwargs)

    def __str__(self):
        return self.question[:50]
