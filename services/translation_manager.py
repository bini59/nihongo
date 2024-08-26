class TranslationManager:
    def process_sentence(self, sentence: str) -> dict:
        """
        문장을 번역하고 한자 정보를 포함한 결과를 반환한다.
        Args:
            sentence (str): 원문

        Returns:
            dict: {
                "original_sentence": str,
                "translated_sentence": str,
                "kanji_info": list[dict] # [{"kanji": "漢", "kana": "かん", "meaning": "한"}]
            }
        """
        pass
