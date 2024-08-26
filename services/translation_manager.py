from translation import Translation
from kana_converter import KanaConverter

class TranslationManager:
    def __init__(self):
        self.translator = Translation()
        self.kana_converter = KanaConverter()

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
        result = {
            "original_sentence": sentence,
            "translated_sentence": "",
            "kanji_info": []
        }
        
        # 문장 번역
        result["translated_sentence"] = self.translator.translate_sentence(sentence)
        
        # 한자 정보 추출
        kanji_info_list = self.kana_converter.convert_sentence_to_kana(sentence)
        
        # 각 한자의 meaning(뜻)을 번역
        for kanji_info in kanji_info_list:
            kanji_info["meaning"] = self.translator.translate_sentence(kanji_info["meaning"])
        
        # 결과에 한자 정보 저장
        result["kanji_info"] = kanji_info_list
        
        return result
