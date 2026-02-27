"""
AI-Based Automated UML Diagram Generator - Enhanced Version
FastAPI Web Application with LangChain, Interactive Editing, and Export Features
"""
from fastapi import FastAPI, File, UploadFile, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import shutil
import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict
import uvicorn

from render_uml import render_diagram
from text_extractor import extract_text_from_file
from ai_analyzer import get_analyzer, UMLDiagramData, UMLClass, UMLRelationship

app = FastAPI(title="AI UML Diagram Generator")

# Create necessary directories
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)
os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)
os.makedirs("sessions", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")
templates = Jinja2Templates(directory="templates")

# Session storage for diagram data
sessions: Dict[str, UMLDiagramData] = {}

# Initialize AI analyzer
analyzer = get_analyzer()


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
    """Generate UML diagram from text or uploaded file using AI"""
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
        
        # Generate session ID
        session_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Use AI analyzer to extract UML components
        print(f"🤖 Analyzing text with AI (Session: {session_id})...")
        diagram_data = analyzer.analyze(text)
        
        # Store in session
        sessions[session_id] = diagram_data
        
        # Save session to disk
        with open(f"sessions/{session_id}.json", "w") as f:
            f.write(diagram_data.model_dump_json(indent=2))
        
        # Generate PlantUML code
        plantuml_code = analyzer.to_plantuml(diagram_data)
        
        # Save PlantUML file
        puml_file = f"outputs/diagram_{timestamp}.puml"
        with open(puml_file, "w") as f:
            f.write(plantuml_code)
        
        # Render diagrams
        png_file = render_diagram(puml_file, 'png')
        svg_file = render_diagram(puml_file, 'svg')
        
        # Get relative paths for response
        png_url = f"/{png_file.replace(chr(92), '/')}"
        svg_url = f"/{svg_file.replace(chr(92), '/')}"
        
        # Return interactive editor page
        return templates.TemplateResponse("editor.html", {
            "request": request,
            "diagram_url": png_url,
            "svg_url": svg_url,
            "diagram_data": diagram_data,
            "session_id": session_id,
            "source": source,
            "timestamp": timestamp
        })
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
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
        
        # Generate session ID and analyze
        session_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        diagram_data = analyzer.analyze(text)
        sessions[session_id] = diagram_data
        
        # Generate and render
        plantuml_code = analyzer.to_plantuml(diagram_data)
        puml_file = f"outputs/diagram_{timestamp}.puml"
        with open(puml_file, "w") as f:
            f.write(plantuml_code)
        
        png_file = render_diagram(puml_file, 'png')
        svg_file = render_diagram(puml_file, 'svg')
        
        return JSONResponse({
            "success": True,
            "session_id": session_id,
            "plantuml_code": plantuml_code,
            "png_url": f"/{png_file}",
            "svg_url": f"/{svg_file}",
            "diagram_data": json.loads(diagram_data.model_dump_json()),
            "timestamp": timestamp
        })
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


# ===== Interactive Editing API Endpoints =====

@app.get("/api/session/{session_id}")
async def get_session_data(session_id: str):
    """Get diagram data for a session"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return JSONResponse(json.loads(sessions[session_id].model_dump_json()))


@app.post("/api/edit/{session_id}/class")
async def add_class(session_id: str, class_data: UMLClass):
    """Add a new class to the diagram"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    sessions[session_id].classes.append(class_data)
    return JSONResponse({"success": True})


@app.put("/api/edit/{session_id}/class/{class_name}")
async def update_class(session_id: str, class_name: str, class_data: UMLClass):
    """Update an existing class"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    diagram_data = sessions[session_id]
    for i, cls in enumerate(diagram_data.classes):
        if cls.name == class_name:
            diagram_data.classes[i] = class_data
            return JSONResponse({"success": True})
    
    raise HTTPException(status_code=404, detail="Class not found")


@app.delete("/api/edit/{session_id}/class/{class_name}")
async def delete_class(session_id: str, class_name: str):
    """Delete a class from the diagram"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    diagram_data = sessions[session_id]
    diagram_data.classes = [cls for cls in diagram_data.classes if cls.name != class_name]
    
    # Also remove relationships involving this class
    diagram_data.relationships = [
        rel for rel in diagram_data.relationships 
        if rel.from_class != class_name and rel.to_class != class_name
    ]
    
    return JSONResponse({"success": True})


@app.put("/api/edit/{session_id}/relationship/{rel_index}")
async def update_relationship(session_id: str, rel_index: int, rel_data: UMLRelationship):
    """Update an existing relationship"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    diagram_data = sessions[session_id]
    if 0 <= rel_index < len(diagram_data.relationships):
        diagram_data.relationships[rel_index] = rel_data
        return JSONResponse({"success": True})
    
    raise HTTPException(status_code=404, detail="Relationship not found")


@app.delete("/api/edit/{session_id}/relationship/{rel_index}")
async def delete_relationship(session_id: str, rel_index: int):
    """Delete a relationship from the diagram"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    diagram_data = sessions[session_id]
    if 0 <= rel_index < len(diagram_data.relationships):
        diagram_data.relationships.pop(rel_index)
        return JSONResponse({"success": True})
    
    raise HTTPException(status_code=404, detail="Relationship not found")


@app.get("/api/regenerate/{session_id}")
async def regenerate_diagram(session_id: str):
    """Regenerate diagram from current session data"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    try:
        diagram_data = sessions[session_id]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Generate PlantUML code
        plantuml_code = analyzer.to_plantuml(diagram_data)
        
        # Save PlantUML file
        puml_file = f"outputs/diagram_{timestamp}.puml"
        with open(puml_file, "w") as f:
            f.write(plantuml_code)
        
        # Render diagrams
        png_file = render_diagram(puml_file, 'png')
        
        return JSONResponse({
            "success": True,
            "diagram_url": f"/{png_file.replace(chr(92), '/')}"
        })
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


# ===== Export API Endpoints =====

@app.get("/api/export/{session_id}/json")
async def export_json(session_id: str):
    """Export diagram data as JSON"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    json_data = analyzer.to_json(sessions[session_id])
    
    return Response(
        content=json_data,
        media_type="application/json",
        headers={
            "Content-Disposition": f"attachment; filename=uml_diagram_{session_id[:8]}.json"
        }
    )


@app.get("/api/export/{session_id}/xmi")
async def export_xmi(session_id: str):
    """Export diagram data as XMI (XML Metadata Interchange)"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    xmi_data = analyzer.to_xmi(sessions[session_id])
    
    return Response(
        content=xmi_data,
        media_type="application/xml",
        headers={
            "Content-Disposition": f"attachment; filename=uml_diagram_{session_id[:8]}.xmi"
        }
    )


@app.get("/api/export/{session_id}/plantuml")
async def export_plantuml(session_id: str):
    """Export diagram as PlantUML code"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    plantuml_code = analyzer.to_plantuml(sessions[session_id])
    
    return Response(
        content=plantuml_code,
        media_type="text/plain",
        headers={
            "Content-Disposition": f"attachment; filename=uml_diagram_{session_id[:8]}.puml"
        }
    )


if __name__ == "__main__":
    print("=" * 60)
    print("🤖 AI-Based Automated UML Diagram Generator")
    print("=" * 60)
    print("✨ Features:")
    print("   • LangChain + LLM Integration (Phase 1 & 2)")
    print("   • Confidence Scoring")
    print("   • Interactive Human-in-the-Loop Editor")
    print("   • Real-time Diagram Regeneration")
    print("   • Export to JSON/XMI/PlantUML")
    print("=" * 60)
    print("📱 Access the app at: http://localhost:8000")
    print("=" * 60)
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
