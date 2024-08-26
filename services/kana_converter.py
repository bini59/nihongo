import fugashi

class KanaConverter:
    def __init__(self):
        self.tagger = fugashi.Tagger()

    def convert_sentence_to_kana(self, sentence: str) -> list[dict]:
        """
        문장을 받아서, 각 단어의 표면, 히라가나 발음 및 뜻을 반환한다.
        Args:
            sentence (str): 문장

        Returns:
            list[dict]: 각 단어의 정보 리스트 (예: [{"kanji": "漢字", "kana": "かんじ", "meaning": "한자"}])
        """
        kana_list = []
        for word in self.tagger(sentence):
            kana_list.append({
                "word": word.surface,
                "kana": word.feature.kana or "",
                "meaning": word.feature.lemma or ""
            })
        return kana_list
