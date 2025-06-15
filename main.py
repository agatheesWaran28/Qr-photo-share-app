from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil
import os
from utils import generate_qr, match_faces

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Homepage: QR Generator
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate_qr")
async def generate_qr_code(name: str = Form(...), event: str = Form(...), email: str = Form(...), date: str = Form(...)):
    url = f"https://qr-photo-share-app.com/event?name={name}&event={event}"
    qr_path = generate_qr(url)
    return FileResponse(qr_path, filename="event_qr.png")

# Upload Photos
@app.post("/upload_photos/")
async def upload_photos(files: list[UploadFile] = File(...)):
    for file in files:
        with open(f"static/uploaded_photos/{file.filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    return {"message": "Photos uploaded successfully."}

# Event Page
@app.get("/event", response_class=HTMLResponse)
async def event_form(request: Request):
    return templates.TemplateResponse("user_form.html", {"request": request})

@app.post("/process_photo/")
async def process_photo(file: UploadFile = File(...)):
    user_path = f"reference_photos/{file.filename}"
    with open(user_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    results = match_faces(user_path, "static/uploaded_photos")
    return templates.TemplateResponse("results.html", {"request": {}, "results": results})
