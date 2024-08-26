from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import mm
from reportlab.lib import colors
import os

from services.article_parser import ArticleParser
from services.translation_manager import TranslationManager

class PDFGenerator:
    def process_data(self, article_content: str, api_key) -> list[dict]:
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
        translation_manager = TranslationManager(api_key)

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
        # font_path = "fonts/NotoSans.ttf"
        font_path = os.path.join(os.getcwd(), "fonts", "NanumGothic.ttf")
        nihon_font_path = os.path.join(os.getcwd(), "fonts", "ShipporiGothicB2-Bold.ttf")
        pdfmetrics.registerFont(TTFont("NotoSans", font_path))
        pdfmetrics.registerFont(TTFont("NihonFont", nihon_font_path))

        # 마진 설정
        x_margin = 20 * mm
        y_position = height - 20 * mm  # 상단 마진

        # 텍스트 최대 너비 설정
        max_width = width - 2 * x_margin

        # 기사 데이터 추가
        for article in article_data:
            original_sentence = article.get("original_sentence", "")
            translated_sentence = article.get("translated_sentence", "")
            kanji_info = article.get("kanji_info", [])

            # 일본어 문장 추가 (줄바꿈 적용)
            c.setFont("NihonFont", 12)
            y_position = self.multi_line_text(c, f"{original_sentence}", x_margin, y_position, max_width, 12)

            # 번역된 한국어 문장 추가 (줄바꿈 적용)
            c.setFont("NotoSans", 12)
            y_position = self.multi_line_text(c, f"{translated_sentence}", x_margin, y_position, max_width, 12)

            # 한자 정보 추가 (줄바꿈 적용)
            for kanji in kanji_info:
                c.setFont("NihonFont", 12)
                kanji_text = kanji.get("word", "")
                kana_text = kanji.get("kana", "")
                text = f"- {kanji_text}({kana_text})"
                y_position = self.multi_line_text(c, text, x_margin, y_position, max_width, 12, new_line=False)

                
                meaning = kanji.get("meaning", "")
                c.setFont("NotoSans", 12)
                y_position = self.multi_line_text(c, f": {meaning}", x_margin+c.stringWidth(text, "NihonFont", 12), y_position, max_width, 12)
                # 페이지 하단에 도달하면 새로운 페이지 추가
                if y_position < 20 * mm:
                    c.showPage()
                    y_position = height - 20 * mm

            # 섹션 간 여백 추가
            y_position -= 10

            # 페이지 하단에 도달하면 새로운 페이지 추가
            if y_position < 20 * mm:
                c.showPage()
                c.setFont("NotoSans", 12)
                y_position = height - 20 * mm

        # PDF 저장
        c.save()

    def multi_line_text(self, canvas_obj, text, x_margin, y_position, max_width, font_size, new_line=True):
        """
        텍스트를 페이지의 너비에 맞춰 줄바꿈을 하여 출력한다.
        Args:
            canvas_obj: reportlab canvas 객체
            text (str): 출력할 텍스트
            x_margin (int): 좌측 마진
            y_position (int): 출력할 Y 좌표
            max_width (int): 텍스트가 들어갈 최대 너비
            font_size (int): 폰트 크기

        Returns:
            int: 업데이트된 y_position 값
        """
        # 텍스트를 최대 너비에 맞게 줄을 나눕니다.
        line = ''
        for word in text:
            if canvas_obj.stringWidth(line + word, "NotoSans", font_size) <= max_width:
                line += word
            else:
                canvas_obj.drawString(x_margin, y_position, line)
                y_position -= font_size + 2
                line = word + ' '

                # 페이지 하단에 도달하면 페이지 넘김
                if y_position < 20 * mm:
                    canvas_obj.showPage()
                    y_position = A4[1] - 20 * mm

        # 마지막 라인 출력
        if line:
            canvas_obj.drawString(x_margin, y_position, line)
            if new_line:
                y_position -= font_size + 2

        return y_position


if __name__ == "__main__":
    # PDF 생성 예시
    pdf_generator = PDFGenerator()
    article_data = [{'original_sentence': 'TBS NEWS DIG Powered by JNN政府は、総理官邸で開催された能登半島地震の復旧・復興に関する関係閣僚会議で、災害発生時の司令塔機能を強化するため、国の災害対応を統括し、自治体との調整役を担う「防災監」のポストを新たに設ける方針を決めました。', 'translated_sentence': "TBS NEWS DIG Powered by JNN\n정부는 총리관저에 서 열린 노토반도 지진 복구-부흥 관계장관회의에서 재난 발생 시 지휘부 기능을 강화하기 위해 국가의 재난 대응을 총괄하고 지자체와의 조정 역할을 담당하는 '방재감' 직책을 신설할 방침을 정했다.", 'kanji_info': [{'word': '政府', 'kana': 'セイフ', 'meaning': '정부'}, {'word': '総理', 'kana': 'ソウリ', 'meaning': '총리'}, {'word': '官邸', 'kana': 'カンテイ', 'meaning': '관저'}, {'word': '開催', 'kana': 'カイサイ', 'meaning': '개최'}, {'word': '能登', 'kana': 'ノト', 'meaning': '노토'}, {'word': '半島', 'kana': 'ハントウ', 'meaning': '반도'}, {'word': '地震', 'kana': 'ジシン', 'meaning': '지진'}, {'word': '復旧', 'kana': 'フッキュウ', 'meaning': '예전 방식으로 돌아가기'}, {'word': '復興', 'kana': 'フッコウ', 'meaning': '회춘'}, {'word': '関する', 'kana': 'カンスル', 'meaning': '관련'}, {'word': '関係', 'kana': 'カンケイ', 'meaning': '관계'}, {'word': '閣僚', 'kana': 'カクリョウ', 'meaning': '각료'}, {'word': '会議', 'kana': 'カイギ', 'meaning': '회의'}, {'word': '災害', 'kana': 'サイガイ', 'meaning': ' 재해'}, {'word': '発生', 'kana': 'ハッセイ', 'meaning': '발생'}, {'word': '時', 'kana': 'ジ', 'meaning': '時'}, {'word': '司令', 'kana': 'シレイ', 'meaning': 'commander'}, {'word': '塔', 'kana': 'トウ', 'meaning': '塔'}, {'word': '機能', 'kana': 'キノウ', 'meaning': '기능'}, {'word': '強化', 'kana': 'キョウカ', 'meaning': '강화'}, {'word': '国', 'kana': 'クニ', 'meaning': '国'}, {'word': '災害', 'kana': 'サイガイ', 'meaning': '재해'}, {'word': '対応', 'kana': 'タイオウ', 'meaning': '대응'}, {'word': '統括', 'kana': 'トウカツ', 'meaning': '총괄'}, {'word': '自治', 'kana': 'ジチ', 'meaning': '셀프 거버넌스'}, {'word': '体', 'kana': 'タイ', 'meaning': '体'}, {'word': '調整', 'kana': 'チョウセイ', 'meaning': '조정'}, {'word': '役', 'kana': 'ヤク', 'meaning': '役'}, {'word': '担う', 'kana': 'ニナウ', 'meaning': '담당'}, {'word': '防 災', 'kana': 'ボウサイ', 'meaning': '재해 예방'}, {'word': '監', 'kana': 'カン', 'meaning': '監'}, {'word': '新た', 'kana': 'アラタ', 'meaning': '새로운'}, {'word': '設ける', 'kana': 'モウケル', 'meaning': '설치'}, {'word': '方針', 'kana': 'ホウシン', 'meaning': '나침반'}, {'word': '決め', 'kana': 'キメ', 'meaning': '결정'}]}, {'original_sentence': '【写真で見る】政府\xa0「防災監」ポスト新設を決定\u3000災害対応の司令塔機能の強化\u3000自治体との調整役担うまた、各省庁あわせて1000人規模の人員を確保し、災害発生時には国から速やかに応援に入れるようにするとしています。', 'translated_sentence': "사진으로 보는 정부 '방재감' 직위 신설 결정 재난 대응 지휘부 기능 강화 지자체 와의 조정 역할을 담당하고, 각 부처를 합쳐 1000명 규모의 인력을 확보해 재난 발생 시 국가가 신속하게 지원하도록 하겠다고 밝혔다.", 'kanji_info': [{'word': '写真', 'kana': 'シャシン', 'meaning': '사진'}, {'word': '見る', 'kana': 'ミル', 'meaning': '보기'}, {'word': '政府', 'kana': 'セイフ', 'meaning': '정부'}, {'word': '防災', 'kana': ' ボウサイ', 'meaning': '재해 예방'}, {'word': '監', 'kana': 'カン', 'meaning': '監'}, {'word': '新設', 'kana': 'シンセツ', 'meaning': '신설'}, {'word': '決定', 'kana': 'ケッテイ', 'meaning': '결정'}, {'word': '災害', 'kana': 'サイガイ', 'meaning': '재해'}, {'word': '対応', 'kana': 'タイオウ', 'meaning': '대응'}, {'word': '司令', 'kana': 'シレイ', 'meaning': 'commander'}, {'word': '塔', 'kana': 'トウ', 'meaning': '塔'}, {'word': '機能', 'kana': 'キノウ', 'meaning': '기능'}, {'word': '強化', 'kana': ' キョウカ', 'meaning': '강화'}, {'word': '自治', 'kana': 'ジチ', 'meaning': '셀프 거버넌스'}, {'word': '体', 'kana': 'タイ', 'meaning': '体'}, {'word': '調整', 'kana': 'チョウセイ', 'meaning': '조정'}, {'word': '役', 'kana': 'ヤク', 'meaning': '役'}, {'word': '担う', 'kana': 'ニナウ', 'meaning': '담당'}, {'word': '各', 'kana': 'カク', 'meaning': '各'}, {'word': '省庁', 'kana': 'ショウチョウ', 'meaning': '부처'}, {'word': '人', 'kana': 'ニン', 'meaning': '人'}, {'word': '規模', 'kana': 'キボ', 'meaning': '규모'}, {'word': '人員', 'kana': 'ジンイン', 'meaning': '직원'}, {'word': '確保', 'kana': 'カクホ', 'meaning': '확보'}, {'word': '災害', 'kana': 'サイガイ', 'meaning': '재해'}, {'word': '発生', 'kana': 'ハッセイ', 'meaning': '발생'}, {'word': '時', 'kana': 'ジ', 'meaning': '時'}, {'word': '国', 'kana': 'クニ', 'meaning': '国'}, {'word': '速やか', 'kana': 'スミヤカ', 'meaning': '빠른'}, {'word': '応援', 'kana': 'オウエン', 'meaning': '응원'}, {'word': '入れる', 'kana': 'イレル', 'meaning': '넣기'}]}, {'original_sentence': 'また、岸田総理は会議の中で、「復旧・復興をさらに加速させるため、9月上旬をめどに発災から第6弾となる予備費の使用決定を行うべく調整を進めてほ しい」と指示しました。', 'translated_sentence': '또한, 기시다 총리는 회의에서 "복구와 부흥을 더욱 가속화하기 위해 9월 초를 목표로 재해 발생 후 6번째 예비비 사용 결정이 이루어질 수 있도록 조정을 진행해 달라"고 지시했다.', 'kanji_info': [{'word': '岸田', 'kana': 'キシダ', 'meaning': '키시다'}, {'word': '総理', 'kana': 'ソウリ', 'meaning': '총리'}, {'word': '会議', 'kana': 'カイギ', 'meaning': '회의'}, {'word': '中', 'kana': 'ナカ', 'meaning': '中'}, {'word': '復旧', 'kana': 'フッキュウ', 'meaning': ' 예전 방식으로 돌아가기'}, {'word': '復興', 'kana': 'フッコウ', 'meaning': '회춘'}, {'word': '加速', 'kana': 'カソク', 'meaning': '가속'}, {'word': '月', 'kana': 'ガツ', 'meaning': '月'}, {'word': '上旬', 'kana': 'ジョウジュン', 'meaning': '한 달의 첫 3분의 1'}, {'word': '発災', 'kana': 'ハッサイ', 'meaning': '발재'}, {'word': '第', 'kana': 'ダイ', 'meaning': '第'}, {'word': '弾', 'kana': 'ダン', 'meaning': '弾'}, {'word': '予備', 'kana': 'ヨビ', 'meaning': '예비'}, {'word': '費', 'kana': 'ヒ', 'meaning': '費'}, {'word': '使用', 'kana': 'シヨウ', 'meaning': '활용'}, {'word': '決定', 'kana': 'ケッテイ', 'meaning': '결정'}, {'word': '行う', 'kana': 'オコナウ', 'meaning': '하다'}, {'word': '調整', 'kana': 'チョウセイ', 'meaning': '조정'}, {'word': '進め', 'kana': 'ススメ', 'meaning': '진행'}, {'word': '指示', 'kana': 'シジ', 'meaning': '지시어'}]}, {'original_sentence': 'TBSテレビ', 'translated_sentence': 'TBS TV', 'kanji_info': []}]
    pdf_generator.generate_pdf(article_data, "tmp/article_translation.pdf")