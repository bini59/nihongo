import re

class ArticleParser:
    def parse_article_to_sentences(self, article_content: str) -> list[str]:
        """
        뉴스 기사 본문을 문장 단위로 분해한다.
        Args:
            article_content (str): 뉴스 기사 본문

        Returns:
            list[str]: 문장 리스트
        """
        # 다양한 구두점을 기준으로 문장을 분리한다.
        # 일본어와 한국어에서 일반적으로 사용하는 구두점을 기준으로 분리
        sentences = re.split(r'(?<=[。！？\?])', article_content)
        
        # 문장 양 끝 공백 제거 및 빈 문장 제거
        sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
        
        return sentences
