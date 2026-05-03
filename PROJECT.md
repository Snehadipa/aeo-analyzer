# Project Structure & Files

## 📁 Project Layout
```
aeo-analyzer/
├── main.py                 # 🎯 Main FastAPI application
├── config.py               # ⚙️ Configuration settings
├── examples.py             # 🧪 Test/example usage
├── requirements.txt        # 📦 Python dependencies
├── .env.example            # 🔑 Environment template
├── .env                    # 🔐 Your API keys (create from .env.example)
├── .gitignore             # 📝 Git ignore rules
├── run.bat                # 🪟 Windows startup script
├── run.sh                 # 🐧 Linux/Mac startup script
├── README.md              # 📚 Full documentation
├── QUICKSTART.md          # ⚡ Quick setup guide
└── PROJECT.md             # 📋 This file
```

---

## 📄 File Descriptions

### `main.py` 
**The Core Application**
- FastAPI application with all API endpoints
- OpenAI integration for generating responses
- Product extraction logic
- Visibility score calculation
- CORS middleware for frontend integration

**Key Functions:**
- `extract_products_from_response()` - Extracts product names from AI response
- `find_product_position()` - Finds where user's product appears
- `calculate_visibility_score()` - Computes visibility metric
- `analyze_product()` - Main endpoint handler

**Key Endpoints:**
- `POST /analyze` - Main analysis endpoint
- `GET /health` - Health check
- `GET /` - API info

---

### `config.py`
**Customization Hub**
- OpenAI model and temperature settings
- Port configuration
- Product extraction parameters
- Visibility score calculation constants
- CORS settings
- System prompt for OpenAI

**Edit this to:**
- Switch from GPT-3.5 to GPT-4
- Adjust response creativity (temperature)
- Change how visibility is scored
- Customize error messages

---

### `requirements.txt`
**Dependencies**
```
fastapi          - Web framework
uvicorn          - ASGI server
openai           - OpenAI API client
pydantic         - Data validation
python-dotenv    - Environment variable loading
```

**Install with:**
```bash
pip install -r requirements.txt
```

---

### `examples.py`
**Testing & Examples**
- Pre-built example queries
- Interactive query mode
- Health check testing
- Pretty-prints results

**Run with:**
```bash
python examples.py                # Run examples
python examples.py interactive    # Interactive mode
```

---

### `.env.example`
**Environment Template**
```ini
OPENAI_API_KEY=sk-your-key-here
PORT=8000
```

**How to use:**
1. Copy to `.env`
2. Add your actual OpenAI API key
3. Never commit `.env` to git (it's in .gitignore)

---

### `.gitignore`
**Git Ignore Rules**
Prevents committing:
- Virtual environment (`venv/`)
- Environment variables (`.env`)
- Python cache (`__pycache__/`)
- IDE files (`.vscode/`, `.idea/`)
- Logs

---

### `run.bat` (Windows)
**Windows Startup Script**
- Sets up virtual environment
- Installs dependencies
- Prompts for API key setup
- Starts the server

**Usage:**
```bash
# Double-click the file, OR
.\run.bat
```

---

### `run.sh` (macOS/Linux)
**Unix Startup Script**
- Sets up virtual environment
- Installs dependencies
- Prompts for API key setup
- Starts the server

**Usage:**
```bash
chmod +x run.sh
./run.sh
```

---

### `README.md`
**Comprehensive Documentation**
- Full API reference
- Installation instructions
- Example requests
- Troubleshooting guide
- Feature explanations
- Next steps suggestions

---

### `QUICKSTART.md`
**2-Minute Setup Guide**
- Quick installation steps
- Platform-specific instructions
- Common issues and fixes
- Quick testing methods

---

## 🔄 Data Flow

```
User Request
    ↓
POST /analyze (FastAPI endpoint)
    ↓
Validate input (query & product_name)
    ↓
Call OpenAI API with query
    ↓
Get AI response
    ↓
Extract products from response
    ↓
Check if user's product is found
    ↓
Find product position
    ↓
Calculate visibility score
    ↓
Return JSON response
    ↓
User sees results
```

## 📊 API Request/Response Flow

```
REQUEST:
{
  "query": "best magnesium supplement",
  "product_name": "XYZ Magnesium"
}
         ↓
    [Processing]
         ↓
RESPONSE:
{
  "ai_response": "Full AI text...",
  "extracted_products": ["Product1", "Product2", ...],
  "product_found": true/false,
  "product_position": 1 (or null),
  "visibility_score": 85.0,
  "message": "Summary message"
}
```

---

## 🎯 Key Features Explained

### 1. Product Extraction
- Uses regex patterns to identify product names
- Looks for bulleted/numbered lists
- Handles quoted product names
- Removes duplicates
- Limits to top 10 products

### 2. Position Matching
- Finds user's product in extracted list
- Performs case-insensitive matching
- Returns 1-indexed position (first = 1, not 0)

### 3. Visibility Score
- Formula: `100 - (position - 1) * 25`
- Position 1: 100% (most visible)
- Position 2: 75%
- Position 3: 50%
- Not found: 0%

### 4. Error Handling
- Validates empty inputs
- Catches OpenAI API errors
- Returns meaningful error messages
- HTTP status codes for debugging

---

## 🚀 How to Run

### Quick Start (Recommended)
```bash
# Windows
.\run.bat

# macOS/Linux
./run.sh
```

### Manual Start
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate (Windows)
pip install -r requirements.txt
python main.py
```

### Access the App
- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc Docs**: http://localhost:8000/redoc

---

## 🔧 Customization Guide

### Change OpenAI Model
Edit `config.py`:
```python
OPENAI_MODEL = "gpt-4"  # Was "gpt-3.5-turbo"
```

### Adjust Visibility Score
Edit `config.py`:
```python
VISIBILITY_SCORE_FIRST_POSITION = 100
VISIBILITY_SCORE_POSITION_DECREMENT = 25
```

### Change Server Port
Edit `.env`:
```
PORT=8001
```

### Modify System Prompt
Edit `config.py`:
```python
SYSTEM_PROMPT = "Your custom prompt..."
```

---

## 📦 Dependencies Explained

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | 0.104.1 | Web framework |
| uvicorn | 0.24.0 | ASGI server |
| openai | 1.3.9 | OpenAI API client |
| pydantic | 2.5.0 | Data validation |
| python-dotenv | 1.0.0 | Load .env files |

---

## 🧪 Testing

### Option 1: Swagger UI (Easiest)
Visit http://localhost:8000/docs and try the `/analyze` endpoint directly

### Option 2: Python Examples
```bash
python examples.py
python examples.py interactive
```

### Option 3: cURL
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"query": "best energy drink", "product_name": "PowerBoost"}'
```

### Option 4: Python Requests
```python
import requests

response = requests.post(
    "http://localhost:8000/analyze",
    json={
        "query": "best magnesium supplement",
        "product_name": "XYZ Magnesium"
    }
)
print(response.json())
```

---

## 🐛 Debug Tips

### Check if API is running:
```bash
curl http://localhost:8000/health
```

### Check API key is set:
```bash
python -c "import os; print('API Key Set:', bool(os.getenv('OPENAI_API_KEY')))"
```

### View API documentation:
- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Enable verbose logging:
Edit `main.py` to add logging statements

---

## 📈 Next Steps

1. **Frontend**: Build UI to call the API
2. **Database**: Store queries and results
3. **Analytics**: Track visibility trends
4. **Comparison**: Compare multiple models
5. **Batch Processing**: Analyze multiple products at once
6. **Caching**: Cache results to save API costs

---

## 📞 Support

- Check QUICKSTART.md for quick fixes
- See README.md for detailed documentation
- Visit http://localhost:8000/docs for API documentation
- Check OpenAI status: https://status.openai.com

---

**Happy coding!** 🎉
