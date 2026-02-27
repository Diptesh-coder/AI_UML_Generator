# Fix Python 3.14 Compatibility Issue

## Problem
LangChain doesn't support Python 3.14 yet. Your venv uses Python 3.14.3.

## Solution: Recreate with Python 3.12

### Step 1: Remove old virtual environment
```powershell
Remove-Item -Recurse -Force .venv
```

### Step 2: Create new venv with Python 3.12
```powershell
# Find Python 3.12 installation (adjust path as needed)
py -3.12 -m venv .venv

# OR if you have python3.12 directly:
python3.12 -m venv .venv
```

### Step 3: Activate new venv
```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 4: Install all packages
```powershell
pip install -r requirements.txt
```

### Step 5: Configure Groq API key
Edit `.env` file and add your key:
```
GROQ_API_KEY=gsk_your_actual_key_here
```

Get free key at: https://console.groq.com/keys

### Step 6: Run app
```powershell
python app.py
```

You should now see:
```
✅ Groq LLM initialized successfully
```

## Alternative: Use Fallback Mode Now

If you don't want to reinstall Python, the app **already works** in rule-based fallback mode.

Just visit: http://localhost:8000

It will extract UML components using NLP patterns instead of LLM (slightly lower accuracy but functional).
