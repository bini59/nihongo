from fastapi import FastAPI
from api.news_api import news_router
from api.pdf_api import pdf_router

app = FastAPI()

# 라우터 등록
app.include_router(news_router, prefix="/news")
app.include_router(pdf_router, prefix="/pdf")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
