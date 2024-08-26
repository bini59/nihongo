import pytest
from unittest.mock import patch, MagicMock
from services.translation import Translator

@pytest.fixture
def translator():
    return Translator()

@patch('services.translation.deepl.Translator.translate_text')
def test_translate_sentence(mock_translate_text, translator):
    # Mock DeepL API response
    mock_translate_text.return_value.text = "번역된 문장"

    result = translator.translate_sentence("This is a test sentence.", source_lang="en", target_lang="KO")
    assert result == "번역된 문장"

@patch('services.translation.deepl.Translator.translate_text')
def test_translate_sentence_error_handling(mock_translate_text, translator):
    # Mock DeepL API to raise an exception
    mock_translate_text.side_effect = Exception("Translation failed")

    result = translator.translate_sentence("This is a test sentence.", source_lang="en", target_lang="KO")
    assert result == ""
