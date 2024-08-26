from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from services.news_fetcher import NewsFetcher
from pdf.pdf_generator import PDFGenerator
import os

pdf_router = APIRouter()

@pdf_router.post("/download_article_pdf")
async def download_article_pdf(url: str, api_key: str = None):
    """
    뉴스기사 URL로부터 번역 후 PDF로 변환하여 다운로드
    Args:
        url (str): 뉴스 기사 URL

    Returns:
        FileResponse: 변환된 PDF 파일
    """
    try:
        news_fetcher = NewsFetcher()
        pdf_generator = PDFGenerator()

        # 기사 본문 가져오기
        article_content = news_fetcher.fetch_article_content(url)

        # 기사 본문 번역 및 처리
        # 번역 및 데이터 가공 작업은 별도 서비스에서 진행
        article_data = pdf_generator.process_data(article_content, api_key=api_key)

        # PDF 파일 생성
        pdf_file_path = os.path.join(os.getcwd(), "tmp", "article_translation.pdf")
        # pdf_file_path = "tmp/article_translation.pdf"
        pdf_generator.generate_pdf(article_data=article_data, file_path=pdf_file_path)

        # 파일 반환
        return FileResponse(pdf_file_path, media_type='application/pdf', filename="article_translation.pdf")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # # 임시로 저장된 PDF 파일 제거
        # if os.path.exists(pdf_file_path):
        #     os.remove(pdf_file_path)
        pass
