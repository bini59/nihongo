class PDFGenerator:
    def generate_pdf(self, article_data: list[dict], file_path: str) -> None:
        """
        번역된 뉴스 기사 데이터를 PDF로 변환하여 저장한다.
        Args:
            article_data (list[dict]): {
                "original_sentence": str,
                "translated_sentence": str,
                "kanji_info": list[dict]
            }
            file_path (str): 저장할 PDF 파일 경로
        """
        pass
