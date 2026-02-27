# 🤖 AI-Based Automated UML Diagram Generator

An intelligent web application that automatically generates UML diagrams from text descriptions or uploaded documents using AI and NLP.

## 🚀 Features

- **AI-Powered Extraction**: Automatically extracts classes, attributes, and relationships from natural language
- **Multi-Format Support**: Upload PDF, DOCX, or TXT files
- **Beautiful Web Interface**: Modern, responsive design
- **Multiple Output Formats**: Generate PNG and SVG diagrams
- **PlantUML Integration**: Uses PlantUML for professional diagram rendering
- **FastAPI Backend**: High-performance async web framework

## 📋 Requirements

All dependencies are listed in `requirements.txt`:
- FastAPI & Uvicorn for web server
- SpaCy & Transformers for NLP
- PlantUML for diagram generation
- pdfplumber & python-docx for document parsing

## 🛠️ Installation

1. Create and activate virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## ▶️ Usage

### Start the Web Server

```bash
python app.py
```

Access the application at: http://localhost:8000

### Use the Web Interface

1. **Option 1**: Enter a text description of your system
   ```
   Class User has name, email, password
   Class Admin inherits from User
   Class Product has id, name, price
   User has many Orders
   ```

2. **Option 2**: Upload a document (PDF, DOCX, TXT) describing your system

3. Click "Generate UML Diagram"

4. View and download your generated diagrams!

### Use the Python Module Directly

```python
from render_uml import render_diagram

# Render a PlantUML file
render_diagram('mydiagram.puml', 'png')
render_diagram('mydiagram.puml', 'svg')
```

## 📁 Project Structure

```
.
├── app.py                 # FastAPI web application
├── render_uml.py          # UML rendering module
├── text_extractor.py      # AI text extraction module
├── requirements.txt       # Python dependencies
├── diagram.puml          # Example PlantUML file
├── templates/            # HTML templates
│   ├── index.html        # Main page
│   ├── result.html       # Results page
│   └── error.html        # Error page
├── static/               # Static files (CSS, JS)
├── uploads/              # Uploaded documents
└── outputs/              # Generated diagrams
```

## 🎨 How It Works

1. **Input Processing**: Text or documents are processed to extract natural language descriptions
2. **AI Analysis**: NLP algorithms identify classes, attributes, methods, and relationships
3. **PlantUML Generation**: Structured PlantUML code is generated from extracted information
4. **Diagram Rendering**: PlantUML code is rendered to PNG/SVG using remote server
5. **Result Display**: Generated diagrams are displayed with downloadable links

## 📝 Tips for Best Results

- Use clear class declarations: "Class [Name] has [attributes]"
- Specify relationships explicitly: "inherits from", "has many", "uses"
- Mention multiple classes to see their connections
- Provide structured descriptions for better extraction

## 🔧 API Endpoints

- `GET /` - Main web interface
- `POST /generate` - Generate diagram (form submit)
- `POST /api/generate` - Generate diagram (JSON API)

## 📄 License

MIT License

## 👨‍💻 Author

*Diptesh Maji*

AI-Based Automated UML Diagram Generator
