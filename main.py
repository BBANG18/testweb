import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from google.generativeai import GenerativeModel, configure

# Google API 키 설정 (환경 변수에서 불러옴)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY 환경 변수가 설정되지 않았습니다.")

configure(api_key=GOOGLE_API_KEY)

# Gemini Flash 모델 초기화
# Gemini 1.5 Flash는 'gemini-1.5-flash' 또는 'gemini-1.5-flash-latest'로 지정할 수 있습니다.
# 여기서는 'gemini-1.5-flash-latest'를 사용합니다.
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
        # Gemini 모델에 메시지 전달 및 응답 생성
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
    # 애플리케이션 실행: 터미널에서 `uvicorn main:app --reload` 명령으로 실행 가능
    uvicorn.run(app, host="0.0.0.0", port=8000)
