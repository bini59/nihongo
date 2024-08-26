class NewsFetcher:
    def fetch_articles_by_category(self, category: str) -> list[dict]:
        """
        주어진 카테고리에 맞는 뉴스 기사 10개를 불러온다.
        Args:
            category (str): 뉴스 카테고리

        Returns:
            list[dict]: 뉴스 기사 리스트 (title, url 등 포함)
        """
        pass

    def fetch_article_content(self, url: str) -> str:
        """
        주어진 뉴스 기사 URL로부터 본문을 가져온다.
        Args:
            url (str): 뉴스 기사 URL

        Returns:
            str: 뉴스 기사 본문
        """
        pass
