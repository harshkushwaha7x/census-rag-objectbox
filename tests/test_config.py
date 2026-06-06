"""
Unit tests for config module.
"""

import os
import pytest
from unittest.mock import patch
import sys

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from config import load_config, get_groq_api, get_config_value


class TestConfig:
    """Test cases for configuration functions."""
    
    def test_load_config_success(self):
        """Test successful loading of configuration."""
        # This will return True if .env exists, False otherwise
        result = load_config()
        assert isinstance(result, bool)
    
    @patch.dict(os.environ, {'GROQ_API_KEY': 'test_api_key_123'})
    def test_get_groq_api_success(self):
        """Test retrieving Groq API key when it exists."""
        api_key = get_groq_api()
        assert api_key == 'test_api_key_123'
    
    @patch.dict(os.environ, {}, clear=True)
    def test_get_groq_api_missing(self):
        """Test retrieving Groq API key when it doesn't exist."""
        api_key = get_groq_api()
        assert api_key is None
    
    @patch.dict(os.environ, {'TEST_VAR': 'test_value'})
    def test_get_config_value_exists(self):
        """Test retrieving existing config value."""
        value = get_config_value('TEST_VAR')
        assert value == 'test_value'
    
    @patch.dict(os.environ, {}, clear=True)
    def test_get_config_value_default(self):
        """Test retrieving config value with default."""
        value = get_config_value('NONEXISTENT_VAR', 'default_value')
        assert value == 'default_value'
    
    @patch.dict(os.environ, {}, clear=True)
    def test_get_config_value_none(self):
        """Test retrieving config value that doesn't exist."""
        value = get_config_value('NONEXISTENT_VAR')
        assert value is None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
