from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from api.news_api import news_router
from api.pdf_api import pdf_router

app = FastAPI()
# 정적 파일 서빙 (CSS, JS 등)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 템플릿 설정
templates = Jinja2Templates(directory="templates")
@app.get("/")
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# 라우터 등록
app.include_router(news_router, prefix="/news")
app.include_router(pdf_router, prefix="/pdf")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
