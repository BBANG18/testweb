import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Load environment variables from .env file

app = FastAPI()
templates = Jinja2Templates(directory=".")

# Configure Google Gemini API
# Ensure GOOGLE_API_KEY is set in your environment variables or .env file
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Gemini model
# Using 'gemini-1.5-flash' for the Flash version as requested
model = genai.GenerativeModel('gemini-1.5-flash')

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Serves the index.html file.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat", response_class=HTMLResponse)
async def chat(request: Request, user_input: str = Form(...)):
    """
    Handles chat requests, sends user input to Gemini, and returns the response.
    """
    try:
        # Generate content using the Gemini model
        response = model.generate_content(user_input)
        bot_response = response.text
    except Exception as e:
        bot_response = f"Error: Could not get a response from Gemini. {e}"

    return templates.TemplateResponse("index.html", {"request": request, "user_input": user_input, "bot_response": bot_response})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
