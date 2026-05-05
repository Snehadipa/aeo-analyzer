# AI Product Visibility Analyzer — Measure Your Brand’s Presence in AI Recommendations

As users shift from Google search to AI assistants, product discovery is changing.

This tool helps brands understand whether they appear in AI-generated answers — and how they rank.

## 🎯 Problem Solved

Many Amazon sellers don't know whether their products appear in AI-generated answers for customer queries. This tool provides visibility into how frequently their products are recommended by AI systems.

## 💡 How It Works

1. User enters a search query (e.g., "best magnesium supplement for seniors")
2. User enters their product name (e.g., "XYZ Magnesium")
3. System calls OpenAI API with the query
4. System analyzes the response to:
   - Extract all mentioned products
   - Check if the user's product appears
   - Determine its position in the list
   - Calculate a visibility score
5. Returns comprehensive results

## 📊 Output Example

```
Query: "best magnesium supplement for seniors"
Product: "XYZ Magnesium"

Response:
{
  "ai_response": "For seniors, I recommend... XYZ Magnesium offers... Consider Glow Magnesium...",
  "extracted_products": [
    "XYZ Magnesium",
    "Glow Magnesium",
    "Nature Made Magnesium",
    "Quantum Nutrition Labs"
  ],
  "product_found": true,
  "product_position": 1,
  "visibility_score": 100.0,
  "message": "✅ Product 'XYZ Magnesium' found at position 1 out of 4 products mentioned."
}
```

## 🔗 Repository

Source code:
https://github.com/Snehadipa/aeo-analyzer

## 🌐 Live Demo (Public)

The deployed Streamlit app is public by default. Anyone with the link can open it:
https://aeo-analyzer-rohx8fucn2jduvhsd4abrd.streamlit.app/

Avoid entering sensitive data.

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- OpenAI API key (get one at https://platform.openai.com/api-keys)

### Installation

1. **Clone/Navigate to the project folder:**
   ```bash
   cd c:\Users\sneha\aeo-analyzer
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables:**
   - Copy `.env.example` to `.env`:
     ```bash
     copy .env.example .env
     ```
   - Open `.env` and add your OpenAI API key:
     ```
     OPENAI_API_KEY=sk-your-actual-key-here
     ```

### Running the Server

```bash
python main.py
```

You should see:
```
🚀 Starting AI Product Visibility Analyzer on port 8000
📚 API Documentation available at http://localhost:8000/docs
```

## 📡 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. **Analyze Product** (Main Endpoint)
- **URL:** `/analyze`
- **Method:** `POST`
- **Content-Type:** `application/json`

**Request Body:**
```json
{
  "query": "best magnesium supplement for seniors",
  "product_name": "XYZ Magnesium"
}
```

**Response (200 OK):**
```json
{
  "ai_response": "Full AI-generated response text here...",
  "extracted_products": [
    "Product 1",
    "Product 2",
    "Product 3"
  ],
  "product_found": true,
  "product_position": 1,
  "visibility_score": 100.0,
  "message": "✅ Product 'XYZ Magnesium' found at position 1 out of 3 products mentioned."
}
```

**Response Fields:**
- `ai_response` (string): Full response from OpenAI
- `extracted_products` (array): List of product names found in the response
- `product_found` (boolean): Whether user's product appears in the response
- `product_position` (integer | null): Position in the product list (1-indexed), null if not found
- `visibility_score` (number): Score from 0-100 based on position (0 = not found, 100 = first position)
- `message` (string): Human-readable summary

#### 2. **Health Check**
- **URL:** `/health`
- **Method:** `GET`

**Response:**
```json
{
  "status": "healthy",
  "service": "AI Product Visibility Analyzer"
}
```

#### 3. **API Info**
- **URL:** `/`
- **Method:** `GET`

**Response:**
```json
{
  "name": "AI Product Visibility Analyzer",
  "description": "Check if your Amazon product appears in AI-generated responses",
  "version": "1.0.0",
  "endpoints": {...}
}
```

## 🔧 Testing with cURL

### Example 1: Basic Query
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "best energy drink for workouts",
    "product_name": "PowerBoost Energy"
  }'
```

### Example 2: Product Not Found
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "best smartphone",
    "product_name": "Unknown Brand Phone"
  }'
```

### Example 3: Check Health
```bash
curl -X GET "http://localhost:8000/health"
```

## 🌐 Interactive API Documentation

Once the server is running, visit:
```
http://localhost:8000/docs
```

This opens **Swagger UI** where you can:
- See all endpoints
- Try requests directly in the browser
- View response schemas
- Get auto-generated documentation

## 📝 Visibility Score Explanation

The visibility score (0-100%) is calculated as:
- **0%** - Product not found in response
- **100%** - Product is the first mentioned (highest visibility)
- **75%** - Product is the second mentioned
- **50%** - Product is the third mentioned
- Lower scores for products mentioned further down

Example with 3 products:
- Position 1: 100% (most visible)
- Position 2: 75%
- Position 3: 50%

## 🛠️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | Required | Your OpenAI API key |
| `PORT` | 8000 | Server port |

### Customization

Edit `main.py` to:
- Change the OpenAI model (currently using `gpt-3.5-turbo`)
- Adjust temperature for response variation
- Modify `max_tokens` for response length
- Change product extraction patterns
- Adjust visibility score calculation

## 🐛 Troubleshooting

### "OPENAI_API_KEY not found"
- Make sure you created `.env` file in the project root
- Check that your API key is valid at https://platform.openai.com/api-keys
- Verify the API key has sufficient credits

### "Connection refused"
- Make sure the server is running (`python main.py`)
- Check that port 8000 is not in use
- Change `PORT` in `.env` if needed

### "Rate limit exceeded"
- You've hit OpenAI API rate limits
- Wait a moment and try again
- Check your OpenAI account usage at platform.openai.com

### Poor product extraction
- The extraction algorithm uses pattern matching
- Very generic product names might not be extracted well
- Consider the AI model's training data limitations

## 📚 Next Steps

- **Frontend:** Build a React/Vue app to call this API
- **Database:** Add persistence to store queries and results
- **Analytics:** Track product visibility trends over time
- **Multiple Models:** Compare results across GPT-3.5, GPT-4, etc.
- **Advanced Extraction:** Use NLP for better product name identification

## 📄 License

Open source. Use for commercial or personal projects.

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the API docs at `http://localhost:8000/docs`
3. Check your OpenAI API key and credits

---

**Happy analyzing!** 🎉
