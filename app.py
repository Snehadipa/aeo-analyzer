import streamlit as st
import requests
import json
import os

st.set_page_config(page_title="AI Product Analyzer", layout="wide")

st.title("🔍 AI Product Visibility Analyzer")
st.markdown("Check if your product appears in AI-generated recommendations")

# Backend URL - uses environment variable or defaults to localhost
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

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
                res = requests.post(
                    f"{BACKEND_URL}/analyze",
                    json={"query": query, "product_name": product},
                    timeout=30
                )
                
                if res.status_code == 200:
                    data = res.json()
                    
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
                    
                    with col2:
                        st.metric("Visibility Score", f"{data['visibility_score']:.0f}%")
                    
                    with col3:
                        st.metric("Total Products", len(data["extracted_products"]))
                    
                    # Message
                    if data["product_found"]:
                        st.success(f"✅ {data['message']}")
                    else:
                        st.warning(f"⚠️ {data['message']}")
                
                else:
                    st.error(f"API Error: {res.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error(f"❌ Cannot connect to API at {BACKEND_URL}. Check if backend is running.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Sidebar info
with st.sidebar:
    st.markdown("## 📋 Instructions")
    st.markdown("""
    1. **Start the backend** (in another terminal):
       ```bash
       python main.py
       ```
    
    2. **Enter a search query** - What would you ask AI?
    
    3. **Enter your product name** - Which product to search for?
    
    4. **Click Analyze** - Get instant results!
    
    ### 📊 What it shows:
    - AI's response to your query
    - All products it mentioned
    - Whether your product was found
    - Position ranking & visibility score
    """)
    
    st.divider()
    st.markdown("### ⚙️ Settings")
    st.markdown(f"""
    - Backend: {BACKEND_URL}
    - Model: GPT-4o Mini
    - Response Format: Structured JSON
    """)

