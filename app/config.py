"""
Configuration module for Census RAG application.
Handles environment variables and API key management.
"""
import os
from dotenv import load_dotenv

def load_config():
    """
    Load environment variables from .env file.
    
    Returns:
        bool: True if .env file was loaded successfully, False otherwise
    """
    return load_dotenv()

def get_groq_api():
    """
    Retrieve Groq API key from environment variables.
    
    Returns:
        str: Groq API key or None if not found
    """
    return os.getenv('GROQ_API_KEY')

def get_config_value(key, default=None):
    """
    Get configuration value from environment variables.
    
    Args:
        key (str): Environment variable name
        default: Default value if key not found
        
    Returns:
        Configuration value or default
    """
    return os.getenv(key, default)