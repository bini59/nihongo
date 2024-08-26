from fastapi import APIRouter, HTTPException
from typing import List
from services.news_fetcher import NewsFetcher

news_router = APIRouter()

@news_router.get("/get_articles", response_model=List[dict])
async def get_articles(category: str):
    """
    카테고리에 맞는 뉴스 기사 10개를 가져오는 엔드포인트
    Args:
        category (str): 뉴스 카테고리

    Returns:
        List[dict]: 뉴스 기사 리스트
    """
    try:
        news_fetcher = NewsFetcher()
        articles = news_fetcher.fetch_articles_by_category(category)
        return articles
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
