import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from google.generativeai import GenerativeModel, configure

GOOGLE_API_KEY = os.getenv("GOOGLE_API") # 여기가 GOOGLE_API_KEY -> GOOGLE_API 로 변경되었습니다.
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API 환경 변수가 설정되지 않았습니다. Render 환경 변수를 확인하세요.")

configure(api_key=GOOGLE_API_KEY)

model = GenerativeModel('gemini-1.5-flash-latest')

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    루트 경로에 접속했을 때 index.html을 렌더링합니다.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat", response_class=HTMLResponse)
async def chat(request: Request, user_message: str = Form(...)):
    """
    사용자의 메시지를 받아 Gemini 모델에 전달하고 응답을 반환합니다.
    """
    try:
        response = model.generate_content(user_message)
        gemini_response = response.text
    except Exception as e:
        gemini_response = f"오류 발생: {e}"

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "user_message": user_message, "gemini_response": gemini_response}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
