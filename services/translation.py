import os
import deepl
import logging

class Translator:
    def __init__(self):
        self.api_key = os.getenv("DEEPL_API_KEY")
        self.translator = deepl.Translator(self.api_key)

    def translate_sentence(self, sentence: str, source_lang: str = "JA", target_lang: str = "KO") -> str:
        """
        문장을 일본어에서 한국어로 번역한다.
        Args:
            sentence (str): 원문
            source_lang (str): 원문 언어 (기본값: 일본어)
            target_lang (str): 목표 언어 (기본값: 한국어)

        Returns:
            str: 번역된 문장
        """
        try:
            translation = self.translator.translate_text(sentence, target_lang=target_lang)
            return translation.text  # 반환 타입이 객체일 수 있으므로 .text로 명시적 접근
        except Exception as e:
            logging.error(f"Failed to translate: {e}")
            return ""
