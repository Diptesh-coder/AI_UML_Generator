# 🚀 Quick Start Guide

## What You Have Now

Your AI-Based UML Diagram Generator now includes:

### ✅ **Phase 1: Text Analysis & Preprocessing**
- Syntactic analysis (nouns → classes, verbs → relationships)
- Semantic analysis (synonym resolution)
- Multi-format document support (PDF, DOCX, TXT)

### ✅ **Phase 2: Component Identification**
- AI-powered classification of classes, attributes, methods
- Relationship detection (inheritance, association, aggregation, composition, dependency)
- **Confidence scoring** for every component (0.0 to 1.0)

### ✅ **Human-in-the-Loop Interactive Editor**
- Real-time editing of classes and relationships
- Delete/Add/Modify components
- Instant diagram regeneration
- Visual confidence indicators

### ✅ **Multiple Export Formats**
- JSON (for data interchange)
- XMI (XML Metadata Interchange)
- PlantUML (source code)
- PNG/SVG (images)

## How to Use Right Now

### 1. **The Server is Running! 🎉**

Access your application at: **http://localhost:8000**

### 2. **Try a Sample Input**

Copy and paste this into the text area:

```
A Guest can register to become a Customer.
The Customer adds Products to a Shopping Cart.
Customer extends User.
Admin extends User.
Class Order has orderDate, totalAmount, status.
Order contains OrderItems.
Payment processes Orders.
User has name, email, password.
```

Click "Generate UML Diagram"

### 3. **Interactive Editor**

You'll see:
- **Left panel**: Tables with all classes and relationships
- **Right panel**: Live UML diagram
- **Edit buttons**: Click to modify any component
- **Delete buttons**: Remove unwanted elements
- **Confidence scores**: Color-coded bars showing AI certainty

### 4. **Make Changes**

Try this:
1. Click "Edit" on any class
2. Change the name or confidence score
3. Click "Save"
4. Click "🔄 Regenerate" to see updated diagram

### 5. **Export Your Work**

Click any of these buttons:
- **📥 Export JSON**: For data analysis or storage
- **📥 Export XMI**: For importing into UML tools (Enterprise Architect, StarUML)
- **⬇️ Download PNG**: For presentations
- **⬇️ Download SVG**: For vector graphics

## 🔥 Enable Full AI Power (Optional)

Currently running in **rule-based mode** (still works great!).

To enable **LLM-powered semantic analysis** with GPT-3.5/GPT-4:

### Step 1: Get OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Create an account / Sign in
3. Click "Create new secret key"
4. Copy your key

### Step 2: Configure Environment
1. Open the `.env` file in your project folder
2. Replace `your_openai_api_key_here` with your actual key:
   ```
   OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
   AI_MODEL=gpt-3.5-turbo
   ```

### Step 3: Restart Server
```bash
# Press Ctrl+C in the terminal
# Then run again:
python app.py
```

Now you'll see: ✅ **OpenAI LLM initialized successfully**

## 📚 Example Inputs

### E-Commerce System
```
User has email, password, name
Customer extends User
Admin extends User
Product has id, name, price, stock
ShoppingCart contains Products
Order has orderDate, status, total
Customer has a ShoppingCart
Customer places Orders
Order contains Products
Payment processes Order
```

### Library Management
```
Class Library manages Books
Class Book has title, author, ISBN, publishDate
Class Member has memberID, name, email
Class Librarian extends Member
Member borrows Books
Librarian manages Library
```

### Banking System
```
Account has accountNumber, balance
SavingsAccount extends Account
CheckingAccount extends Account
Customer has name, address, phone
Customer owns Accounts
Transaction processes on Account
```

## 🎯 Tips for Best Results

### Without OpenAI (Rule-Based Mode):
✅ Use "Class X has Y, Z"
✅ Use "A extends B" for inheritance
✅ Use "A contains B" for composition
✅ Be explicit and structured

### With OpenAI (LLM Mode):
✅ Use natural language
✅ Be descriptive
✅ The AI understands context
✅ Synonyms are resolved automatically

## 🔍 Understanding Confidence Scores

| Score | Meaning | Color |
|-------|---------|-------|
| 0.9-1.0 | Very confident | Dark Green |
| 0.7-0.89 | Confident | Light Green |
| 0.5-0.69 | Uncertain | Yellow |
| < 0.5 | Low confidence | Orange/Red |

**Low scores?** Click "Edit" and review the component manually!

## 📊 What Makes This Advanced?

### Traditional Tools:
- Manual drawing
- No AI understanding
- Static diagrams

### Your Tool:
- ✅ **AI-powered extraction** from natural language
- ✅ **Confidence scoring** for every component
- ✅ **Interactive editing** with instant updates
- ✅ **Semantic understanding** (synonym resolution)
- ✅ **Multiple export formats** (JSON, XMI, PlantUML)
- ✅ **Document upload** support (PDF, DOCX, TXT)

## 🎓 For Your Project Report

**Phase 1 (Preprocessing)**: ✅ Implemented
- NLP-based text analysis
- Syntactic parsing (nouns/verbs)
- Semantic analysis (synonym resolution)

**Phase 2 (Component Identification)**: ✅ Implemented
- Class extraction with confidence
- Attribute/method detection
- Relationship classification (5 types)

**Advanced Features**: ✅ Implemented
- LangChain + LLM integration
- Human-in-the-loop editing
- Multi-format export
- Real-time regeneration

## 📞 Need Help?

**Server not starting?**
- Check if port 8000 is free
- Verify Python version (3.9-3.13)
- Reinstall dependencies: `pip install -r requirements.txt`

**No diagram generated?**
- Check console for errors
- Try simpler input first
- Verify PlantUML server is accessible

**Want more features?**
- Check `README_COMPLETE.md` for full documentation
- Explore the API endpoints
- Modify `ai_analyzer.py` for custom rules

---

**✨ Your AI UML Generator is ready to use!**
Open http://localhost:8000 and start generating diagrams! 🚀
