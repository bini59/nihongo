from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import mm
import os

from services.article_parser import ArticleParser
from services.translation_manager import TranslationManager

class PDFGenerator:
    def process_data(self, article_content: str) -> list[dict]:
        """
        뉴스 기사 본문을 문장 단위로 분해하여 처리한다.
        Args:
            article_content (str): 뉴스 기사 본문

        Returns:
            list[dict]: {
                "original_sentence": str,
                "translated_sentence": str,
                "kanji_info": list[dict] # [{"kanji": "漢", "kana": "かん", "meaning": "한"}]
            }
        """
        article_parser = ArticleParser()
        translation_manager = TranslationManager()

        sentences = article_parser.parse_article_to_sentences(article_content)
        processed_data = []
        for sentence in sentences:
            processed_data.append(translation_manager.process_sentence(sentence))
        return processed_data

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
        # PDF 생성
        c = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4

        # 유니코드 폰트 등록 (Noto Sans CJK 폰트 사용)
        font_path = "fonts/NotoSans.ttf"
        pdfmetrics.registerFont(TTFont("NotoSans", font_path))

        # 폰트 설정
        c.setFont("NotoSans", 12)

        # 마진 설정
        x_margin = 20 * mm
        y_position = height - 20 * mm  # 상단 마진

        # 기사 데이터 추가
        for article in article_data:
            original_sentence = article.get("original_sentence", "")
            translated_sentence = article.get("translated_sentence", "")
            kanji_info = article.get("kanji_info", [])

            # 일본어 문장 추가
            c.setFont("NotoSans", 12)
            c.drawString(x_margin, y_position, f"일본어: {original_sentence}")
            y_position -= 15  # 라인 간격 조정

            # 번역된 한국어 문장 추가
            c.drawString(x_margin, y_position, f"한국어: {translated_sentence}")
            y_position -= 15  # 라인 간격 조정

            # 한자 정보 추가
            for kanji in kanji_info:
                kanji_text = kanji.get("word", "")
                kana_text = kanji.get("kana", "")
                meaning = kanji.get("meaning", "")

                # 한자 정보 출력 - 포맷: "- 한자(히라가나): 한국어 뜻"
                c.drawString(x_margin, y_position, f"- {kanji_text}({kana_text}): {meaning}")
                y_position -= 15  # 라인 간격 조정

            # 섹션 간 여백 추가
            y_position -= 10

            # 페이지 하단에 도달하면 새로운 페이지 추가
            if y_position < 20 * mm:
                c.showPage()
                c.setFont("NotoSans", 12)
                y_position = height - 20 * mm

        # PDF 저장
        c.save()


if __name__ == "__main__":
    # PDF 생성 예시
    pdf_generator = PDFGenerator()
    article_data = [
        {
            "original_sentence": "漢字を学ぶ。",
            "translated_sentence": "한자를 공부하다.",
            "kanji_info": [
                {"word": "漢字", "kana": "カンジ", "meaning": "한자"},
                {"word": "学ぶ", "kana": "マナブ", "meaning": "공부하다"}
            ]
        }
    ]
    pdf_generator.generate_pdf(article_data, "example.pdf")