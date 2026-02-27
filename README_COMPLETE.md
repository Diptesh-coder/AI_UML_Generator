# 🤖 AI-Based Automated UML Diagram Generator

## 🎯 Project Overview

An **intelligent web application** that automatically generates UML class diagrams from natural language text or uploaded documents. Implements **Phase 1 (Preprocessing & Text Analysis)** and **Phase 2 (Component Identification & Classification)** using advanced AI/NLP techniques.

## ✨ Key Features

### Phase 1: Text Analysis & Preprocessing
- **Syntactic Analysis**: Identifies nouns as potential classes and verbs as relationships
- **Semantic Analysis**: Resolves synonyms (e.g., "Client" = "Customer")
- **Multi-format Support**: PDF, DOCX, TXT file uploads

### Phase 2: AI-Powered Component Identification
- **Classes**: Automatically extracts entity classes
- **Attributes**: Identifies properties with data types
- **Methods**: Detects behaviors and operations
- **Relationships**: 
  - Inheritance (is-a)
  - Association (has-a)
  - Aggregation (contains)
  - Composition (owns)
  - Dependency (uses)
- **Confidence Scoring**: 0.0 to 1.0 certainty rating for each component

### Advanced Features
- **🔥 LangChain + LLM Integration**: Uses GPT-3.5/GPT-4 for semantic understanding
- **📊 Interactive Editor**: Human-in-the-loop with real-time editing
- **🔄 Live Regeneration**: Instant diagram updates after changes
- **📥 Multiple Export Formats**: JSON, XMI, PlantUML
- **⚡ Fast & Responsive**: FastAPI async backend
- **🎨 Beautiful UI**: Modern gradient design with confidence indicators

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python, FastAPI |
| **AI/NLP** | LangChain, OpenAI API (GPT-3.5/GPT-4) |
| **Fallback NLP** | Rule-based pattern matching |
| **Diagramming** | PlantUML (via web server) |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Data Formats** | JSON, XML/XMI |

## 📋 Requirements

```txt
# Core NLP and ML
spacy>=3.7.0
transformers>=4.30.0
torch>=2.0.0
scikit-learn>=1.3.0

# LangChain & AI
langchain>=0.1.0
langchain-openai>=0.0.5
openai>=1.12.0

# Text processing
nltk>=3.8.0
pdfplumber>=0.10.0
python-docx>=1.0.0

# UML Generation
plantuml>=0.3.0
requests>=2.31.0

# Web Framework
fastapi>=0.104.0
uvicorn>=0.24.0
```

## 🚀 Installation & Setup

### 1. Clone or Navigate to Project Directory

```bash
cd "D:\AI-Based Automated UML Diagram Generator"
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure OpenAI API (Optional but Recommended)

For **full LLM-powered analysis**, configure your OpenAI API key:

```bash
# Copy the example environment file
copy .env.example .env

# Edit .env and add your API key
OPENAI_API_KEY=your_actual_api_key_here
AI_MODEL=gpt-3.5-turbo
AI_TEMPERATURE=0.3
AI_MAX_TOKENS=2000
```

**Without OpenAI API**: The system will use rule-based NLP (still functional but less accurate).

## ▶️ Usage

### Start the Server

```bash
python app.py
```

Access at: **http://localhost:8000**

### Using the Web Interface

#### Option 1: Text Input
1. Navigate to http://localhost:8000
2. Enter a description like:
   ```
   A Guest can register to become a Customer.
   The Customer adds Products to a Shopping Cart.
   Customer extends User.
   Order contains OrderItems.
   Payment processes Orders.
   ```
3. Click "Generate UML Diagram"

#### Option 2: File Upload
1. Upload a PDF, DOCX, or TXT file containing your system description
2. Click "Generate UML Diagram"

### Interactive Editor

After generation, you'll see:

- **Left Panel**: Component editor with tables showing:
  - Classes with attributes, methods, and confidence scores
  - Relationships with types and confidence scores
  - Edit/Delete buttons for each component

- **Right Panel**: Live diagram preview

**Actions Available:**
- ✏️ **Edit**: Modify class names, relationships, confidence scores
- 🗑️ **Delete**: Remove classes or relationships
- ➕ **Add**: Create new classes
- 🔄 **Regenerate**: Update diagram after changes
- 📥 **Export**: Download as JSON, XMI, or PlantUML

## 📖 Examples

### Example 1: E-Commerce System

**Input:**
```
Class User has email, password, name
Class Customer extends User
Class Admin extends User
Class Product has id, name, price, description
Class ShoppingCart contains Products
Class Order has orderDate, total
Customer has a ShoppingCart
Customer places Orders
Order contains Products
Payment processes Order
```

**Output:**
- UML diagram with 6 classes
- Inheritance relationships (Customer → User, Admin → User)
- Composition relationships (ShoppingCart ⬥→ Product)
- Association relationships (Customer → Order)

### Example 2: From Document

Upload a requirements document (PDF/DOCX) describing your system. The AI will:
1. Extract entity mentions (User, Product, Order, etc.)
2. Identify relationships from natural language
3. Assign confidence scores
4. Generate editable UML diagram

## 🔬 How It Works

### Phase 1: Preprocessing & Text Analysis

```python
# Text → AI Analyzer
text = "User has email and password. Admin extends User."

# Syntactic Analysis (via LLM or rules)
nouns = ["User", "Admin", "email", "password"]
verbs = ["has", "extends"]

# Semantic Analysis
synonyms = resolve_synonyms(nouns)  # "Client" → "Customer"
```

### Phase 2: Component Classification

```python
# Classify components with confidence scores
classes = [
    UMLClass(name="User", attributes=[...], confidence=0.95),
    UMLClass(name="Admin", attributes=[...], confidence=0.90)
]

relationships = [
    UMLRelationship(
        from_class="Admin",
        to_class="User",
        type="inheritance",
        confidence=0.92
    )
]
```

### Phase 3: Diagram Generation

```python
# Convert to PlantUML
plantuml_code = analyzer.to_plantuml(diagram_data)

# Render via PlantUML server
render_diagram(plantuml_file, format='png')
```

## 📁 Project Structure

```
.
├── app.py                    # Main FastAPI application
├── ai_analyzer.py            # LangChain + LLM analyzer (Phase 1 & 2)
├── text_extractor.py         # Document text extraction
├── render_uml.py             # PlantUML rendering
├── requirements.txt          # Python dependencies
├── .env.example              # Environment configuration template
├── .env                      # Your API keys (create this)
├── templates/
│   ├── index.html           # Landing page
│   ├── editor.html          # Interactive editor (human-in-the-loop)
│   ├── result.html          # Simple results view
│   └── error.html           # Error page
├── static/
│   └── style.css            # Additional styles
├── uploads/                  # Uploaded documents
├── outputs/                  # Generated diagrams
└── sessions/                 # Session data (JSON)
```

## 🔧 API Endpoints

### Generation
- `GET /` - Main page
- `POST /generate` - Generate diagram (returns editor page)
- `POST /api/generate` - Generate diagram (returns JSON)

### Interactive Editing
- `GET /api/session/{session_id}` - Get session data
- `POST /api/edit/{session_id}/class` - Add class
- `PUT /api/edit/{session_id}/class/{class_name}` - Update class
- `DELETE /api/edit/{session_id}/class/{class_name}` - Delete class
- `PUT /api/edit/{session_id}/relationship/{index}` - Update relationship
- `DELETE /api/edit/{session_id}/relationship/{index}` - Delete relationship
- `GET /api/regenerate/{session_id}` - Regenerate diagram

### Export
- `GET /api/export/{session_id}/json` - Export as JSON
- `GET /api/export/{session_id}/xmi` - Export as XMI
- `GET /api/export/{session_id}/plantuml` - Export PlantUML code

## 💡 Tips for Best Results

### With LLM (OpenAI API configured):
- Use natural language descriptions
- Be descriptive about relationships
- The AI will understand context and synonyms

### Without LLM (Rule-based):
- Use explicit patterns: "Class X has Y"
- Specify relationships clearly: "A extends B", "C contains D"
- Use consistent naming conventions

### General:
- Mention multiplicities when known
- Describe entity behaviors for methods
- Review and edit confidence scores manually

## 🐛 Troubleshooting

### LangChain Not Available
**Issue**: Warning "LangChain not available"
**Solution**: 
1. Check if `langchain` and `langchain-openai` are installed
2. Verify Python version compatibility (3.9-3.13 recommended)
3. System will still work with rule-based extraction

### OpenAI API Errors
**Issue**: "OpenAI API key not configured"
**Solution**: 
1. Create `.env` file from `.env.example`
2. Add your OpenAI API key
3. Restart the server

### No Diagram Generated
**Issue**: Blank or error page
**Solution**:
1. Check if text contains recognizable entities
2. Use explicit class declarations
3. Check browser console for JavaScript errors

## 🎓 Academic Context

This project implements concepts from:
- **Natural Language Processing (NLP)**
- **Software Engineering (UML Modeling)**
- **Human-Computer Interaction (Interactive Editing)**
- **Machine Learning (LLM Integration)**

Perfect for:
- Final year projects
- Academic research
- Software engineering courses
- AI/ML demonstrations

## 📄 License

MIT License

## 👨‍💻 Author

AI-Based Automated UML Diagram Generator
Powered by LangChain, OpenAI, and PlantUML

---

**🌟 Star this project if you find it useful!**
