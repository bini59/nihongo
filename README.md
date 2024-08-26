
# Nihongo PDF Translator

## 개요
**Nihongo PDF Translator**는 일본어 기사를 번역하고, 한자에 대한 히라가나 발음 및 한국어 의미를 포함한 PDF 파일을 생성하는 프로그램입니다. FastAPI와 ReportLab을 사용하여 웹 API 형태로 구현되었으며, PDF 생성 기능을 제공합니다. 번역은 DeepL API를 사용하여 일본어를 한국어로 번역합니다.

## 설치

### 1. 프로젝트의 의존성 설치

이 프로젝트를 실행하기 전에 의존성을 설치해야 합니다. 이를 위해 프로젝트 루트에서 다음 명령어를 실행하세요:

```bash
pip install -r requirements.txt
```

`requirements.txt` 파일에는 프로젝트에 필요한 라이브러리가 포함되어 있습니다:

- **fastapi**: 웹 애플리케이션 프레임워크
- **uvicorn**: FastAPI 서버 실행을 위한 ASGI 서버
- **reportlab**: PDF 생성을 위한 라이브러리
- **fpdf2**: PDF 생성을 위한 또 다른 라이브러리 (옵션)
- **deepl**: DeepL API를 사용하여 번역 기능을 제공

### 2. DeepL API Key 설정

이 프로그램은 **DeepL API**를 사용하여 일본어 문장을 한국어로 번역합니다. 따라서 DeepL API Key가 필요합니다. [DeepL](https://www.deepl.com/pro-api)에서 API Key를 발급받은 후, 프로그램이 이를 사용할 수 있도록 설정해야 합니다.

API 키는 `Translation` 클래스 내에서 `self.api_key` 변수에 설정됩니다.

```python
class Translator:
    def __init__(self):
        self.api_key = "YOUR_DEEPL_API_KEY"  # 여기에 API Key를 설정하세요
        self.translator = deepl.Translator(self.api_key)
```

또는 환경 변수를 사용하여 API Key를 설정할 수도 있습니다.

```bash
export DEEPL_API_KEY=your_deepl_api_key_here
```

## 실행 방법

프로젝트를 실행하기 위해서는 FastAPI 애플리케이션을 실행해야 합니다. 다음 명령어를 사용하여 `main.py` 파일을 실행하세요:

```bash
uvicorn main:app --reload
```

이 명령어를 사용하면 FastAPI 서버가 로컬에서 실행되고, `localhost:8000`에서 API 요청을 받을 수 있습니다.

## 주요 기능

- **/generate-pdf**: 일본어 기사를 번역하고, PDF로 변환하는 API 엔드포인트
- **/news**: 특정 카테고리의 일본어 뉴스를 가져오는 API 엔드포인트