# Quick Setup Guide - AI Product Visibility Analyzer

## ⚡ 2-Minute Setup

### Step 1: Get OpenAI API Key (1 minute)
1. Go to https://platform.openai.com/api-keys
2. Sign in or create account
3. Click "Create new secret key"
4. Copy the key (keep it safe!)

### Step 2: Setup Project (1 minute)

#### Windows Users:
```bash
# Navigate to project folder
cd c:\Users\sneha\aeo-analyzer

# Double-click run.bat
# OR from PowerShell:
.\run.bat
```

#### macOS/Linux Users:
```bash
# Navigate to project folder
cd ~/aeo-analyzer

# Make script executable
chmod +x run.sh

# Run it
./run.sh
```

#### Manual Setup (All Platforms):
```bash
# Navigate to project
cd c:\Users\sneha\aeo-analyzer

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup .env file
copy .env.example .env  # Windows
# OR
cp .env.example .env    # macOS/Linux

# Edit .env and add your API key:
# OPENAI_API_KEY=sk-your-key-here

# Run the server
python main.py
```

### Step 3: Test It Works ✅
Once you see:
```
🚀 Starting AI Product Visibility Analyzer on port 8000
📚 API Documentation available at http://localhost:8000/docs
```

Open http://localhost:8000/docs in your browser!

---

## 🧪 Quick Test

### Option A: Use the interactive docs (Easiest)
1. Go to http://localhost:8000/docs
2. Find the `/analyze` endpoint
3. Click "Try it out"
4. Enter your query and product name
5. Click "Execute"

### Option B: Use Python examples
```bash
# In a new terminal (keep server running):
python examples.py                # Run pre-built examples
python examples.py interactive    # Interactive mode
```

### Option C: Use cURL
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "best energy drink",
    "product_name": "PowerBoost"
  }'
```

---

## 🎯 Example Request/Response

### Request:
```json
{
  "query": "best magnesium supplement for seniors",
  "product_name": "XYZ Magnesium"
}
```

### Response:
```json
{
  "ai_response": "For seniors looking for magnesium supplements... I recommend XYZ Magnesium... Also consider Nature's Bounty...",
  "extracted_products": [
    "XYZ Magnesium",
    "Nature's Bounty Magnesium",
    "Glow Magnesium"
  ],
  "product_found": true,
  "product_position": 1,
  "visibility_score": 100.0,
  "message": "✅ Product 'XYZ Magnesium' found at position 1 out of 3 products mentioned."
}
```

---

## 🔧 Common Issues & Fixes

### Issue: "OPENAI_API_KEY not found"
**Fix:** Make sure `.env` file exists in project root with your API key

### Issue: "Connection refused"
**Fix:** Make sure server is running (step 2)

### Issue: "Import Error: No module named 'openai'"
**Fix:** Did you activate virtual environment? Try:
```bash
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### Issue: Port 8000 already in use
**Fix:** Change PORT in .env file:
```
PORT=8001
```
Then run: `python main.py`

---

## 📚 Documentation Files

- **README.md** - Full documentation
- **config.py** - Customize settings (model, temperature, etc.)
- **main.py** - Main API code
- **examples.py** - Example usage
- **requirements.txt** - Dependencies

---

## 🚀 Next Steps

1. ✅ Run the server and test with examples
2. 📊 Build a frontend to call the API
3. 💾 Add database to store results
4. 📈 Track visibility trends over time

---

## 🆘 Need Help?

1. Check full README.md
2. Visit http://localhost:8000/docs (API docs)
3. Check OpenAI API key at https://platform.openai.com/account/api-keys
4. Verify API has credits: https://platform.openai.com/account/usage/overview

Happy analyzing! 🎉
