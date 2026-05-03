"""
FastAPI backend for Amazon Product AI Visibility Analyzer
Checks if a product appears in AI-generated responses for a given query
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="AI Product Visibility Analyzer",
    description="Check if your product appears in AI-generated responses",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client (lazy initialization)
client = None

@app.on_event("startup")
async def startup_event():
    global client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not set!")
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    try:
        client = OpenAI(api_key=api_key)
        print("✅ OpenAI client initialized successfully")
    except Exception as e:
        print(f"ERROR initializing OpenAI client: {e}")
        raise


# Request model
class AnalyzeRequest(BaseModel):
    query: str
    product_name: str


# Response model
class AnalyzeResponse(BaseModel):
    ai_response: str
    extracted_products: list[str]
    product_found: bool
    product_position: int | None
    visibility_score: float
    message: str


def analyze_with_structure(query: str, product_name: str) -> dict:
    """
    Ask OpenAI for the answer and product visibility analysis in one structured JSON response.
    """
    prompt = f"""
You are an AI product analysis system.

Given a user query and a product name, do the following:
1. Answer the query with concise product recommendations.
2. Extract ONLY specific branded product names (like "Sony WH-1000XM5", "Bang Energy").
 Do NOT include generic terms like "magnesium supplement" or "laptop".
3. Check if the given product is present in that product list.
4. Provide the 1-indexed position if found.

Return ONLY valid JSON in this exact shape:

{{
    "ai_response": "...",
    "products": ["Product A", "Product B"],
    "found": true,
    "position": 1
}}

Use false for "found" and null for "position" when the product is not present.

Query: {query}
Product: {product_name}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=1200,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    if not content:
        raise ValueError("OpenAI returned an empty response")

    data = json.loads(content)

    products = data.get("products", [])
    if not isinstance(products, list):
        products = []

    cleaned_products = []
    seen = set()
    for product in products:
        if not isinstance(product, str):
            continue

        name = product.strip()
        if not name:
            continue

        key = name.lower()
        if key not in seen:
            seen.add(key)
            cleaned_products.append(name)

    found = bool(data.get("found"))
    position = data.get("position")
    if not isinstance(position, int):
        position = None

    if not found:
        position = None

    return {
        "ai_response": str(data.get("ai_response", "")),
        "products": cleaned_products,
        "found": found,
        "position": position,
    }


def calculate_visibility_score(
    product_found: bool,
    position: int | None,
    total_products: int
) -> float:
    """
    Calculate visibility score (0-100%).
    - 0 if product not found
    - Decreases based on position in the list
    - Earlier position = higher score
    """
    if not product_found or position is None:
        return 0.0
    
    if total_products == 0:
        return 100.0
    
    # Score: first product = 100%, second = 90%, third = 80%, etc.
    # Decrement by 10% for each position (more granular)
    score = max(0, 100 - (position - 1) * 10)
    return score


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_product(request: AnalyzeRequest):
    """
    Main endpoint: Analyze if a product appears in AI-generated response.
    
    Args:
        query: Search query (e.g., "best magnesium supplement for seniors")
        product_name: Product name to check (e.g., "XYZ Magnesium")
    
    Returns:
        JSON with AI response, extracted products, and visibility analysis
    """
    try:
        # Validate inputs
        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        if not request.product_name or not request.product_name.strip():
            raise HTTPException(status_code=400, detail="Product name cannot be empty")
        
        try:
            analysis = analyze_with_structure(
                request.query.strip(),
                request.product_name.strip()
            )
        except Exception as e:
            print(f"ERROR in analyze_with_structure: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
        
        ai_response = analysis["ai_response"]
        extracted_products = analysis["products"]
        product_found = analysis["found"]
        product_position = analysis["position"]
        
        # Calculate visibility score
        visibility_score = calculate_visibility_score(
            product_found,
            product_position,
            len(extracted_products)
        )
        
        # Create response message
        if product_found:
            message = f"✅ Product '{request.product_name}' found at position {product_position} out of {len(extracted_products)} products mentioned."
        else:
            message = f"❌ Product '{request.product_name}' not found in AI response. {len(extracted_products)} other products were mentioned."
        
        return AnalyzeResponse(
            ai_response=ai_response,
            extracted_products=extracted_products,
            product_found=product_found,
            product_position=product_position,
            visibility_score=visibility_score,
            message=message
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "AI Product Visibility Analyzer"}


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "AI Product Visibility Analyzer",
        "description": "Check if your Amazon product appears in AI-generated responses",
        "version": "1.0.0",
        "endpoints": {
            "POST /analyze": "Analyze product visibility",
            "GET /health": "Health check",
            "GET /docs": "API documentation (Swagger UI)"
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment or default to 8000
    port = int(os.getenv("PORT", 8000))
    
    print(f"🚀 Starting AI Product Visibility Analyzer on port {port}")
    print(f"📚 API Documentation available at http://localhost:{port}/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=port)
