import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import logging

class NewsFetcher:
    def fetch_articles_by_category(self, category: str) -> List[Dict[str, str]]:
        """
        주어진 카테고리에 맞는 뉴스 기사 10개를 불러온다.
        Args:
            category (str): 뉴스 카테고리

        Returns:
            List[Dict[str, str]]: 뉴스 기사 제목과 URL이 담긴 리스트
        """

        url = f'https://news.yahoo.co.jp/topics/{category}'
        response = requests.get(url)

        if response.status_code != 200:
            logging.error(f"Failed to retrieve data: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('a', class_='newsFeed_item_link', limit=10)
        top10_titles = []

        for article in articles:
            title = article.get_text(strip=True)
            summary_link = article['href']

            # 요약 페이지에서 전체 기사 링크 찾기
            try:
                summary_response = requests.get(summary_link)
                if summary_response.status_code != 200:
                    logging.error(f"Failed to retrieve summary page: {summary_response.status_code}")
                    continue

                summary_soup = BeautifulSoup(summary_response.text, 'html.parser')
                article_link_tag = summary_soup.find('a', href=True, string='記事全文を読む')

                if article_link_tag and 'href' in article_link_tag.attrs:
                    article_url = article_link_tag['href']
                    top10_titles.append({
                        "title": title,
                        "url": article_url
                    })
                else:
                    logging.warning("Could not find the full article link.")
            except Exception as e:
                logging.error(f"Error processing article: {e}")

        return top10_titles

    def fetch_article_content(self, url: str) -> str:
        """
        주어진 뉴스 기사 URL로부터 본문을 가져온다.
        Args:
            url (str): 뉴스 기사 URL

        Returns:
            str: 뉴스 기사 본문
        """

        try:
            response = requests.get(url)

            if response.status_code != 200:
                logging.error(f"Failed to retrieve news content: {response.status_code}")
                return ""

            soup = BeautifulSoup(response.text, 'html.parser')
            article_body = soup.find('div', class_='article_body')

            if not article_body:
                logging.warning("Could not find the article body.")
                return ""

            paragraphs = article_body.find_all('p')
            content = "\n".join([p.get_text(strip=True) for p in paragraphs])

            return content

        except Exception as e:
            logging.error(f"Error retrieving article content: {e}")
            return ""
