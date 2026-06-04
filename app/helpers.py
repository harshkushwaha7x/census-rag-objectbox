"""
Helper utility functions for the Census RAG application.
"""

import os
import time
from functools import wraps
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


def timer_decorator(func):
    """
    Decorator to measure function execution time.
    
    Args:
        func: Function to be timed
        
    Returns:
        Wrapped function that logs execution time
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"{func.__name__} executed in {execution_time:.2f} seconds")
        return result
    return wrapper


def validate_pdf_directory(directory_path: str) -> bool:
    """
    Validate if the PDF directory exists and contains PDF files.
    
    Args:
        directory_path: Path to the PDF directory
        
    Returns:
        bool: True if directory is valid and contains PDFs
    """
    if not os.path.exists(directory_path):
        logger.error(f"Directory does not exist: {directory_path}")
        return False
    
    pdf_files = [f for f in os.listdir(directory_path) if f.endswith('.pdf')]
    
    if not pdf_files:
        logger.warning(f"No PDF files found in: {directory_path}")
        return False
    
    logger.info(f"Found {len(pdf_files)} PDF files in {directory_path}")
    return True


def validate_env_variable(var_name: str) -> bool:
    """
    Check if an environment variable is set.
    
    Args:
        var_name: Name of the environment variable
        
    Returns:
        bool: True if variable exists and is not empty
    """
    value = os.getenv(var_name)
    if not value:
        logger.error(f"Environment variable {var_name} is not set")
        return False
    return True


def format_response_time(seconds: float) -> str:
    """
    Format response time in a human-readable way.
    
    Args:
        seconds: Time in seconds
        
    Returns:
        str: Formatted time string
    """
    if seconds < 1:
        return f"{seconds * 1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    else:
        minutes = int(seconds // 60)
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds:.0f}s"


def chunk_documents_info(documents: List[Any]) -> Dict[str, Any]:
    """
    Get statistics about document chunks.
    
    Args:
        documents: List of document chunks
        
    Returns:
        dict: Statistics about the chunks
    """
    if not documents:
        return {
            "total_chunks": 0,
            "avg_chunk_length": 0,
            "total_characters": 0
        }
    
    total_chars = sum(len(doc.page_content) for doc in documents)
    avg_length = total_chars / len(documents)
    
    return {
        "total_chunks": len(documents),
        "avg_chunk_length": int(avg_length),
        "total_characters": total_chars,
        "min_chunk_length": min(len(doc.page_content) for doc in documents),
        "max_chunk_length": max(len(doc.page_content) for doc in documents)
    }


def sanitize_input(text: str, max_length: int = 500) -> str:
    """
    Sanitize user input to prevent injection attacks.
    
    Args:
        text: User input text
        max_length: Maximum allowed length
        
    Returns:
        str: Sanitized text
    """
    # Remove potential dangerous characters
    sanitized = text.strip()
    
    # Limit length
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
        logger.warning(f"Input truncated to {max_length} characters")
    
    return sanitized


def get_db_size(db_directory: str) -> str:
    """
    Calculate the size of the ObjectBox database directory.
    
    Args:
        db_directory: Path to the database directory
        
    Returns:
        str: Human-readable size
    """
    if not os.path.exists(db_directory):
        return "0 MB"
    
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(db_directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.exists(filepath):
                total_size += os.path.getsize(filepath)
    
    # Convert to MB
    size_mb = total_size / (1024 * 1024)
    
    if size_mb < 1:
        return f"{total_size / 1024:.2f} KB"
    elif size_mb < 1024:
        return f"{size_mb:.2f} MB"
    else:
        return f"{size_mb / 1024:.2f} GB"


def format_context_snippets(contexts: List[Any], max_snippets: int = 3) -> List[str]:
    """
    Format retrieved context snippets for display.
    
    Args:
        contexts: List of retrieved context documents
        max_snippets: Maximum number of snippets to return
        
    Returns:
        list: Formatted context snippets
    """
    snippets = []
    for i, doc in enumerate(contexts[:max_snippets]):
        content = doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
        snippets.append(f"[{i+1}] {content}")
    
    return snippets
