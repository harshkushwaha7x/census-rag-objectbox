"""
Logging configuration for Census RAG application.
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime


def setup_logging(log_level: str = "INFO", log_dir: str = "logs") -> None:
    """
    Configure application-wide logging.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory to store log files
    """
    # Create logs directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Convert string log level to logging constant
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(simple_formatter)
    
    # File handler - rotating log files
    log_filename = os.path.join(log_dir, f'census_rag_{datetime.now().strftime("%Y%m%d")}.log')
    file_handler = RotatingFileHandler(
        log_filename,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5
    )
    file_handler.setLevel(numeric_level)
    file_handler.setFormatter(detailed_formatter)
    
    # Error file handler - separate file for errors
    error_log_filename = os.path.join(log_dir, 'errors.log')
    error_handler = RotatingFileHandler(
        error_log_filename,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    
    # Remove existing handlers
    root_logger.handlers.clear()
    
    # Add handlers
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_handler)
    
    # Log startup message
    root_logger.info("=" * 80)
    root_logger.info("Census RAG Application Started")
    root_logger.info(f"Log Level: {log_level}")
    root_logger.info(f"Log Directory: {log_dir}")
    root_logger.info("=" * 80)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Name of the module (typically __name__)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    return logging.getLogger(name)


# Environment-based configuration
def configure_from_env() -> None:
    """Configure logging based on environment variables."""
    log_level = os.getenv("LOG_LEVEL", "INFO")
    log_dir = os.getenv("LOG_DIR", "logs")
    setup_logging(log_level=log_level, log_dir=log_dir)
