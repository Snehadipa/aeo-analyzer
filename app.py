import streamlit as st
import json
import os
from openai import OpenAI

st.set_page_config(page_title="AI Product Analyzer", layout="wide")

st.title("🔍 AI Product Visibility Analyzer")
st.markdown("Check if your product appears in AI-generated recommendations")

if not get_api_key():
    st.warning("Set OPENAI_API_KEY in Streamlit secrets to enable analysis.")

def get_api_key() -> str | None:
    return os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")


def analyze_with_structure(query: str, product_name: str) -> dict:
    prompt = f"""You are an AI shopping assistant. For the given query, provide detailed recommendations with specific branded product names.

Query: {query}

INSTRUCTIONS:
1. Answer the query with 2-3 sentences of recommendations
2. Mention AT LEAST 5-7 specific branded products (include model numbers when relevant)
3. Format your recommendations as a natural paragraph
4. After your answer, list all products mentioned, one per line, after "PRODUCTS:"

Example format:
For budget headphones, I recommend JBL Tune 500BT for comfort, Anker Soundcore Q20 for value, Sony WH-CH720N for noise cancelling, Beats Studio Pro for brand trust, Sennheiser Momentum 3 for quality, and Audio-Technica ATH-M50x for professionals.

PRODUCTS:
JBL Tune 500BT
Anker Soundcore Q20
Sony WH-CH720N
Beats Studio Pro
Sennheiser Momentum 3
Audio-Technica ATH-M50x"""

    api_key = get_api_key()
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set in Streamlit secrets")

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500,
    )

    content = response.choices[0].message.content
    if not content:
        raise ValueError("OpenAI returned empty response")

    parts = content.split("PRODUCTS:")
    ai_response = parts[0].strip() if parts else content

    products = []
    if len(parts) > 1:
        product_lines = parts[1].strip().split("\n")
        for line in product_lines:
            line = line.strip()
            if line and len(line) > 2:
                products.append(line)

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
        "extracted_products": products,
        "product_found": product_found,
        "product_position": product_position,
    }


def calculate_visibility_score(
    product_found: bool,
    position: int | None,
    total_products: int,
) -> float:
    if not product_found or position is None:
        return 0.0

    if total_products == 0:
        return 100.0

    return max(0, 100 - (position - 1) * 10)

# Create two columns for inputs
col1, col2 = st.columns(2)

with col1:
    query = st.text_input(
        "Search Query",
        placeholder="e.g. best headphones under 100",
        help="What question would you ask an AI?"
    )

with col2:
    product = st.text_input(
        "Your Product",
        placeholder="e.g. SoundMax Wireless",
        help="Which product should we search for?"
    )

# Analyze button
if st.button("🔍 Analyze", use_container_width=True):
    if not query or not product:
        st.warning("⚠️ Please fill both fields")
    else:
        with st.spinner("Analyzing... This may take a few seconds"):
            try:
                data = analyze_with_structure(query.strip(), product.strip())

                # AI Response
                st.subheader("💬 AI Response")
                st.write(data["ai_response"])

                # Products Found
                st.subheader("📦 Products Found")
                if data["extracted_products"]:
                    for idx, prod in enumerate(data["extracted_products"], 1):
                        st.write(f"{idx}. **{prod}**")
                else:
                    st.info("No specific products mentioned")

                # Result Analysis
                st.subheader("📊 Visibility Analysis")
                col1, col2, col3 = st.columns(3)

                with col1:
                    if data["product_found"]:
                        st.metric("Status", "✅ Found", f"Position #{data['product_position']}")
                    else:
                        st.metric("Status", "❌ Not Found", "-")

                visibility_score = calculate_visibility_score(
                    data["product_found"],
                    data["product_position"],
                    len(data["extracted_products"]),
                )

                with col2:
                    st.metric("Visibility Score", f"{visibility_score:.0f}%")

                with col3:
                    st.metric("Total Products", len(data["extracted_products"]))

                if data["product_found"]:
                    message = (
                        f"✅ Product '{product}' found at position {data['product_position']} "
                        f"out of {len(data['extracted_products'])} products mentioned."
                    )
                    st.success(message)
                else:
                    message = (
                        f"❌ Product '{product}' not found in AI response. "
                        f"{len(data['extracted_products'])} other products were mentioned."
                    )
                    st.warning(message)

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Sidebar info
with st.sidebar:
    st.markdown("## 📋 Instructions")
     st.markdown("""
     1. **Enter a search query** - What would you ask AI?

     2. **Enter your product name** - Which product to search for?

     3. **Click Analyze** - Get instant results!

     ### 📊 What it shows:
     - AI's response to your query
     - All products it mentioned
     - Whether your product was found
     - Position ranking & visibility score
     """)
    
    st.divider()
    st.markdown("### ⚙️ Settings")
    st.markdown("""
    - Model: GPT-4o Mini
    - Response Format: Text + Product list
    """)

