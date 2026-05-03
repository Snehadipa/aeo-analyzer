"""
Configuration and constants for AI Product Visibility Analyzer
Easily customize these settings
"""

# OpenAI Configuration
OPENAI_MODEL = "gpt-3.5-turbo"  # Can use "gpt-4" for better results (costs more)
OPENAI_TEMPERATURE = 0.7  # Range: 0-1 (lower = more deterministic, higher = more creative)
OPENAI_MAX_TOKENS = 1000  # Maximum response length

# API Configuration
DEFAULT_PORT = 8000
HOST = "0.0.0.0"  # 0.0.0.0 for all interfaces, 127.0.0.1 for localhost only

# Product Extraction Configuration
MAX_PRODUCTS_TO_EXTRACT = 10  # Maximum number of products to extract from response
MIN_PRODUCT_NAME_LENGTH = 2  # Minimum characters for a valid product name
MAX_PRODUCT_NAME_LENGTH = 150  # Maximum characters for a valid product name

# Visibility Score Configuration
# Adjust these to customize how visibility score is calculated
VISIBILITY_SCORE_FIRST_POSITION = 100  # Score for first position (%)
VISIBILITY_SCORE_POSITION_DECREMENT = 25  # How much to decrease for each position

# CORS Configuration
CORS_ORIGINS = ["*"]  # Allow all origins. Change to specific domains for production: ["https://yourdomain.com"]
CORS_CREDENTIALS = True
CORS_METHODS = ["*"]
CORS_HEADERS = ["*"]

# System Prompt for OpenAI
SYSTEM_PROMPT = """You are a helpful product recommendation assistant. 
Provide a concise, informative response about the user's query. 
Include specific product names and brands in your recommendations."""

# Error Messages
ERROR_EMPTY_QUERY = "Query cannot be empty"
ERROR_EMPTY_PRODUCT = "Product name cannot be empty"
ERROR_API_FAILURE = "Failed to get response from OpenAI API"

# Logging
ENABLE_LOGGING = True
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
