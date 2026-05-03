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
    Ask OpenAI for the answer and product analysis.
    Simple version without structured JSON output.
    """
    prompt = f"""You are an AI product analysis assistant. Answer this query with product recommendations.

Query: {query}

Return your response in this format:
1. First, give your recommendation (2-3 sentences)
2. Then list specific product names you mentioned, one per line, starting with "PRODUCTS:"

Example:
For budget wireless headphones, I recommend Anker products for value or Sony for premium features.

PRODUCTS:
Anker Soundcore Life Q20
Sony WH-1000XM5
JBL Tune 500BT"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        
        content = response.choices[0].message.content
        if not content:
            raise ValueError("OpenAI returned empty response")
        
        # Parse response
        parts = content.split("PRODUCTS:")
        ai_response = parts[0].strip() if parts else content
        
        products = []
        if len(parts) > 1:
            product_lines = parts[1].strip().split('\n')
            for line in product_lines:
                line = line.strip()
                if line and len(line) > 2:
                    products.append(line)
        
        # Check if product is in the list
        product_found = False
        product_position = None
        
        product_lower = product_name.lower()
        for idx, prod in enumerate(products, 1):
            if product_lower in prod.lower() or prod.lower() in product_lower:
                product_found = True
                product_position = idx
                break
        
        return {
            "ai_response": ai_response,
            "products": products,
            "found": product_found,
            "position": product_position,
        }
    except Exception as e:
        print(f"ERROR in analyze_with_structure: {e}")
        raise


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


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "client_initialized": client is not None
    }


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
        # Check if client is initialized
        if client is None:
            raise HTTPException(status_code=500, detail="OpenAI client not initialized. Check OPENAI_API_KEY.")
        
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
        print(f"UNHANDLED ERROR: {e}")
        import traceback
        traceback.print_exc()
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
