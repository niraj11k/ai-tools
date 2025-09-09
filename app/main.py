# main.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.prompt_generator import create_prompt ,create_short_prompt
from app.api.chatbot_routes import router as chatbot_router
import os

# load_dotenv()  # Load .env variables

app = FastAPI()

print(f"Current working directory: {os.getcwd()}")
print(f"Templates folder path: {os.path.join(os.getcwd(), 'templates')}")

# Provide a default value (e.g., for local development if the env var isn't set)
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "*")

# Split the string by comma to create a list of origins
# and strip any leading/trailing whitespace from each origin
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",")]

# If you want to allow all origins if the environment variable is "*"
if "*" in allowed_origins and len(allowed_origins) == 1:
    pass
elif allowed_origins_str == "*": # A common way to signify all origins in env
    allowed_origins = ["*"]
elif not any(allowed_origins): # If the env var is empty or only commas
    allowed_origins = [] # Or a sensible default like your local dev URL

# Allow HTML/JS on localhost to call FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # For development only, allows all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(chatbot_router, prefix="/api")

# Templates
templates = Jinja2Templates(directory="templates")
# Import functions and variables from prompt_generator.py
@app.get("/", response_class=HTMLResponse)
async def prompt_page(request: Request):
    return templates.TemplateResponse("generate_prompt.html", {"request": request})


# @app.get("/", response_class=HTMLResponse)
# async def read_root(request: Request):
#     return RedirectResponse(url="/home")

@app.post("/generate")
async def generate_prompt(request: Request):
    body = await request.json()
    task_description = body.get("task")
    provider = body.get("provider")
    if not task_description:
        return {"error": "Please provide a 'task'"}
    if not provider:
        return {"error": "Please select a 'provider'"}
    prompt = create_prompt(task_description, provider)
    return {"prompt": prompt}
@app.post("/generate-short")
async def generate_short_prompt(request: Request):
    data = await request.json()
    task = data.get("task")
    provider = data.get("provider")
    if not task:
        return {"error": "Please provide a 'task'"}
    if not provider:
        return {"error": "Please select a 'provider'"}

    try:
        prompt = create_short_prompt(task, provider)
        return JSONResponse({"prompt": prompt})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
