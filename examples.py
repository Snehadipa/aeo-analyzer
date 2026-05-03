"""
Example usage of the AI Product Visibility Analyzer API
Run this file to test the API after starting the server
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"


def analyze_product(query: str, product_name: str) -> dict:
    """
    Call the analyze endpoint and return results
    
    Args:
        query: Search query (e.g., "best magnesium supplement")
        product_name: Product name to check (e.g., "XYZ Magnesium")
    
    Returns:
        Dictionary with analysis results
    """
    endpoint = f"{BASE_URL}/analyze"
    
    payload = {
        "query": query,
        "product_name": product_name
    }
    
    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to API. Make sure the server is running.")
        print(f"   Run: python main.py")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        print(f"   Response: {e.response.text}")
        return None


def health_check() -> bool:
    """Check if API is running"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        response.raise_for_status()
        return True
    except:
        return False


def print_results(result: dict) -> None:
    """Pretty print the analysis results"""
    if not result:
        return
    
    print("\n" + "="*70)
    print("📊 AI PRODUCT VISIBILITY ANALYSIS")
    print("="*70)
    
    print(f"\n💬 AI Response:\n{'-'*70}")
    print(result['ai_response'][:500] + "..." if len(result['ai_response']) > 500 else result['ai_response'])
    
    print(f"\n\n📦 Extracted Products:")
    for idx, product in enumerate(result['extracted_products'], 1):
        print(f"   {idx}. {product}")
    
    print(f"\n\n📍 Your Product Analysis:")
    print(f"   Found: {'✅ Yes' if result['product_found'] else '❌ No'}")
    if result['product_position']:
        print(f"   Position: #{result['product_position']}")
    print(f"   Visibility Score: {result['visibility_score']:.1f}%")
    
    print(f"\n📢 Message: {result['message']}")
    print("="*70 + "\n")


def run_examples():
    """Run example queries"""
    
    print("🚀 AI Product Visibility Analyzer - Example Usage\n")
    
    # Check if API is running
    print("Checking API connection...", end=" ")
    if not health_check():
        print("❌ FAILED")
        print("\n⚠️  API is not running!")
        print("Start it with: python main.py")
        return
    
    print("✅ Connected!\n")
    
    # Example queries
    examples = [
        {
            "query": "best magnesium supplement for seniors",
            "product": "XYZ Magnesium"
        },
        {
            "query": "best energy drink for workouts",
            "product": "PowerBoost Energy"
        },
        {
            "query": "best laptop for programming",
            "product": "TechPro Laptop X1"
        },
        {
            "query": "best wireless headphones under 100",
            "product": "SoundMax Wireless"
        }
    ]
    
    for idx, example in enumerate(examples, 1):
        print(f"\n📝 Example {idx}/{len(examples)}")
        print(f"   Query: {example['query']}")
        print(f"   Product: {example['product']}")
        print("   Analyzing...", end=" ", flush=True)
        
        result = analyze_product(example['query'], example['product'])
        
        if result:
            print("✅ Done!")
            print_results(result)
        else:
            print("❌ Failed!")
        
        if idx < len(examples):
            input("Press Enter to continue to next example...")


def interactive_mode():
    """Interactive mode for custom queries"""
    
    print("\n" + "="*70)
    print("🔍 INTERACTIVE MODE")
    print("="*70)
    print("Enter your own queries to analyze your products.\n")
    
    while True:
        try:
            query = input("Enter search query (or 'exit' to quit):\n> ").strip()
            
            if query.lower() in ['exit', 'quit', 'q']:
                print("\nGoodbye! 👋")
                break
            
            if not query:
                print("Please enter a query.\n")
                continue
            
            product = input("Enter your product name:\n> ").strip()
            
            if not product:
                print("Please enter a product name.\n")
                continue
            
            print("\nAnalyzing...", end=" ", flush=True)
            result = analyze_product(query, product)
            
            if result:
                print("✅ Done!")
                print_results(result)
            else:
                print("❌ Failed!")
            
            print("\n")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        interactive_mode()
    else:
        print("Usage:")
        print("  python examples.py              - Run example queries")
        print("  python examples.py interactive  - Interactive mode\n")
        run_examples()
