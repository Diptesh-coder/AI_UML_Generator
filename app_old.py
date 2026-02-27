"""
AI-Based Automated UML Diagram Generator
FastAPI Web Application
"""
from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import shutil
from pathlib import Path
from datetime import datetime
import uvicorn

from render_uml import render_diagram
from text_extractor import extract_uml_from_text, extract_text_from_file

app = FastAPI(title="AI UML Diagram Generator")

# Create necessary directories
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)
os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Main page"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate")
async def generate_diagram(
    request: Request,
    text_input: str = Form(None),
    file: UploadFile = File(None)
):
    """Generate UML diagram from text or uploaded file"""
    try:
        # Extract text
        if file and file.filename:
            # Save uploaded file
            file_path = f"uploads/{file.filename}"
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Extract text from file
            text = extract_text_from_file(file_path)
            source = f"File: {file.filename}"
        elif text_input:
            text = text_input
            source = "User Input"
        else:
            return JSONResponse(
                status_code=400,
                content={"error": "Please provide either text or a file"}
            )
        
        # Generate PlantUML code using AI
        plantuml_code = extract_uml_from_text(text)
        
        # Save PlantUML file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        puml_file = f"outputs/diagram_{timestamp}.puml"
        with open(puml_file, "w") as f:
            f.write(plantuml_code)
        
        # Render diagrams
        png_file = render_diagram(puml_file, 'png')
        svg_file = render_diagram(puml_file, 'svg')
        
        # Get relative paths for response
        png_url = f"/{png_file.replace(chr(92), '/')}"
        svg_url = f"/{svg_file.replace(chr(92), '/')}"
        
        return templates.TemplateResponse("result.html", {
            "request": request,
            "png_url": png_url,
            "svg_url": svg_url,
            "plantuml_code": plantuml_code,
            "source": source,
            "timestamp": timestamp
        })
        
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": str(e)
        })


@app.post("/api/generate")
async def api_generate_diagram(
    text_input: str = Form(None),
    file: UploadFile = File(None)
):
    """API endpoint for generating diagrams"""
    try:
        # Extract text
        if file and file.filename:
            file_path = f"uploads/{file.filename}"
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            text = extract_text_from_file(file_path)
        elif text_input:
            text = text_input
        else:
            return JSONResponse(
                status_code=400,
                content={"error": "Please provide either text or a file"}
            )
        
        # Generate PlantUML code
        plantuml_code = extract_uml_from_text(text)
        
        # Save and render
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        puml_file = f"outputs/diagram_{timestamp}.puml"
        with open(puml_file, "w") as f:
            f.write(plantuml_code)
        
        png_file = render_diagram(puml_file, 'png')
        svg_file = render_diagram(puml_file, 'svg')
        
        return JSONResponse({
            "success": True,
            "plantuml_code": plantuml_code,
            "png_url": f"/{png_file}",
            "svg_url": f"/{svg_file}",
            "timestamp": timestamp
        })
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


if __name__ == "__main__":
    print("🚀 Starting AI UML Diagram Generator...")
    print("📱 Access the app at: http://localhost:8000")
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
