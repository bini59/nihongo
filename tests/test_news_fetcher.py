import pytest
from unittest.mock import patch, MagicMock
from services.news_fetcher import NewsFetcher

@pytest.fixture
def news_fetcher():
    return NewsFetcher()

@patch('services.news_fetcher.requests.get')
def test_fetch_articles_by_category(mock_get, news_fetcher):
    # Mock response for the Yahoo News topics page
    mock_topics_response = MagicMock()
    mock_topics_response.status_code = 200
    mock_topics_response.text = '''
    <html>
        <body>
            <a class="newsFeed_item_link" href="https://example.com/article1">Article 1</a>
            <a class="newsFeed_item_link" href="https://example.com/article2">Article 2</a>
        </body>
    </html>
    '''
    
    # Mock response for article summary pages
    mock_summary_response_1 = MagicMock()
    mock_summary_response_1.status_code = 200
    mock_summary_response_1.text = '''
    <html>
        <body>
            <a href="https://example.com/article1_full">記事全文を読む</a>
        </body>
    </html>
    '''
    
    mock_summary_response_2 = MagicMock()
    mock_summary_response_2.status_code = 200
    mock_summary_response_2.text = '''
    <html>
        <body>
            <a href="https://example.com/article2_full">記事全文を読む</a>
        </body>
    </html>
    '''

    # Set side effect for sequential requests
    mock_get.side_effect = [mock_topics_response, mock_summary_response_1, mock_summary_response_2]

    articles = news_fetcher.fetch_articles_by_category("category")
    assert len(articles) == 2
    assert articles[0]["title"] == "Article 1"
    assert articles[0]["url"] == "https://example.com/article1_full"
    assert articles[1]["title"] == "Article 2"
    assert articles[1]["url"] == "https://example.com/article2_full"

@patch('services.news_fetcher.requests.get')
def test_fetch_article_content(mock_get, news_fetcher):
    # Mock response for the article page
    mock_article_response = MagicMock()
    mock_article_response.status_code = 200
    mock_article_response.text = '''
    <html>
        <body>
            <div class="article_body">
                <p>First paragraph of the article.</p>
                <p>Second paragraph of the article.</p>
            </div>
        </body>
    </html>
    '''
    
    mock_get.return_value = mock_article_response

    content = news_fetcher.fetch_article_content("https://example.com/article1")
    assert "First paragraph of the article." in content
    assert "Second paragraph of the article." in content
