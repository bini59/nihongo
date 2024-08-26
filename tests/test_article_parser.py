import pytest
from services.article_parser import ArticleParser

@pytest.fixture
def parser():
    return ArticleParser()

def test_parse_simple_sentences(parser):
    article_content = "今日は天気がいいですね。明日は雨が降るかもしれません！本当にそうですか？"
    expected_sentences = [
        "今日は天気がいいですね。",
        "明日は雨が降るかもしれません！",
        "本当にそうですか？"
    ]
    parsed_sentences = parser.parse_article_to_sentences(article_content)
    assert parsed_sentences == expected_sentences

def test_parse_sentences_with_whitespace(parser):
    article_content = "  今日は天気がいいですね。   明日は雨が降るかもしれません！  "
    expected_sentences = [
        "今日は天気がいいですね。",
        "明日は雨が降るかもしれません！"
    ]
    parsed_sentences = parser.parse_article_to_sentences(article_content)
    assert parsed_sentences == expected_sentences

def test_parse_sentences_with_empty_string(parser):
    article_content = ""
    expected_sentences = []
    parsed_sentences = parser.parse_article_to_sentences(article_content)
    assert parsed_sentences == expected_sentences

def test_parse_sentences_with_complex_punctuation(parser):
    article_content = "これは「テスト」ですか？いいえ、テストではありません。"
    expected_sentences = [
        "これは「テスト」ですか？",
        "いいえ、テストではありません。"
    ]
    parsed_sentences = parser.parse_article_to_sentences(article_content)
    assert parsed_sentences == expected_sentences
