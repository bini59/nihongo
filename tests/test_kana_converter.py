import pytest
from services.kana_converter import KanaConverter

@pytest.fixture
def kana_converter():
    return KanaConverter()

def test_convert_sentence_to_kana_simple(kana_converter):
    sentence = "漢字を学ぶ。"
    expected_output = [
        {"word": "漢字", "kana": "カンジ", "meaning": "漢字"},
        {"word": "学ぶ", "kana": "マナブ", "meaning": "学ぶ"}
    ]
    
    result = kana_converter.convert_sentence_to_kana(sentence)
    assert result == expected_output

# def test_convert_sentence_with_kana_and_kanji(kana_converter):
#     sentence = "私は日本語を勉強しています。"
#     expected_output = [
#         {"word": "私", "kana": "ワタシ", "meaning": "私"},
#         {"word": "日本語", "kana": "ニホンゴ", "meaning": "日本語"},
#         {"word": "勉強", "kana": "ベンキョウ", "meaning": "勉強"}
#     ]

#     result = kana_converter.convert_sentence_to_kana(sentence)
#     assert result == expected_output

def test_convert_sentence_with_punctuation(kana_converter):
    sentence = "これは「テスト」ですか？"
    expected_output = [
    ]
    
    result = kana_converter.convert_sentence_to_kana(sentence)
    assert result == expected_output

def test_convert_sentence_with_mixed_kanji_and_hiragana(kana_converter):
    sentence = "彼は学校へ行きました。"
    expected_output = [
        {"word": "彼", "kana": "カレ", "meaning": "彼"},
        {"word": "学校", "kana": "ガッコウ", "meaning": "学校"},
        {"word": "行き" , "kana": "イキ", "meaning": "行く"},
    ]
    
    result = kana_converter.convert_sentence_to_kana(sentence)
    assert result == expected_output

def test_convert_empty_sentence(kana_converter):
    sentence = ""
    expected_output = []
    
    result = kana_converter.convert_sentence_to_kana(sentence)
    assert result == expected_output
