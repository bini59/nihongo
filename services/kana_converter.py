import fugashi
import re

class KanaConverter:
    def __init__(self):
        self.tagger = fugashi.Tagger('-Owakati')
        self.kanji_pattern = re.compile(r'[\u4e00-\u9faf]+')


    def convert_sentence_to_kana(self, sentence: str) -> list[dict]:
        """
        문장을 받아서, 한자가 포함된 단어의 표면, 히라가나 발음 및 뜻을 반환한다.
        Args:
            sentence (str): 문장

        Returns:
            list[dict]: 각 단어의 정보 리스트 (예: [{"word": "漢字", "kana": "かんじ", "meaning": "漢字"}])
        """
        kana_list = []
        for word in self.tagger(sentence):
            if self.kanji_pattern.search(word.surface):  # 한자 포함 여부를 검색
                kana_list.append({
                    "word": word.surface,
                    "kana": getattr(word.feature, 'kana', "") or "",
                    "meaning": getattr(word.feature, 'lemma', "") or ""
                })
        return kana_list
