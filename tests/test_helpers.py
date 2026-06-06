"""
Unit tests for helper utility functions.
"""

import os
import sys
import pytest
import tempfile
from unittest.mock import Mock

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from helpers import (
    validate_pdf_directory,
    validate_env_variable,
    format_response_time,
    chunk_documents_info,
    sanitize_input,
    get_db_size,
    format_context_snippets
)


class TestHelpers:
    """Test cases for helper functions."""
    
    def test_validate_pdf_directory_nonexistent(self):
        """Test validation of non-existent directory."""
        result = validate_pdf_directory('/nonexistent/path')
        assert result is False
    
    def test_validate_pdf_directory_empty(self):
        """Test validation of empty directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = validate_pdf_directory(tmpdir)
            assert result is False
    
    def test_validate_pdf_directory_with_pdfs(self):
        """Test validation of directory with PDF files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a fake PDF file
            pdf_path = os.path.join(tmpdir, 'test.pdf')
            with open(pdf_path, 'w') as f:
                f.write('fake pdf content')
            
            result = validate_pdf_directory(tmpdir)
            assert result is True
    
    def test_validate_env_variable_exists(self, monkeypatch):
        """Test validation of existing environment variable."""
        monkeypatch.setenv('TEST_VAR', 'test_value')
        result = validate_env_variable('TEST_VAR')
        assert result is True
    
    def test_validate_env_variable_missing(self, monkeypatch):
        """Test validation of missing environment variable."""
        monkeypatch.delenv('TEST_VAR', raising=False)
        result = validate_env_variable('TEST_VAR')
        assert result is False
    
    def test_format_response_time_milliseconds(self):
        """Test formatting response time in milliseconds."""
        result = format_response_time(0.5)
        assert result == "500ms"
    
    def test_format_response_time_seconds(self):
        """Test formatting response time in seconds."""
        result = format_response_time(5.25)
        assert result == "5.25s"
    
    def test_format_response_time_minutes(self):
        """Test formatting response time in minutes."""
        result = format_response_time(125)
        assert result == "2m 5s"
    
    def test_chunk_documents_info_empty(self):
        """Test chunk info for empty document list."""
        result = chunk_documents_info([])
        assert result['total_chunks'] == 0
        assert result['avg_chunk_length'] == 0
    
    def test_chunk_documents_info_with_documents(self):
        """Test chunk info with actual documents."""
        mock_docs = [
            Mock(page_content="A" * 100),
            Mock(page_content="B" * 200),
            Mock(page_content="C" * 150)
        ]
        
        result = chunk_documents_info(mock_docs)
        assert result['total_chunks'] == 3
        assert result['total_characters'] == 450
        assert result['avg_chunk_length'] == 150
        assert result['min_chunk_length'] == 100
        assert result['max_chunk_length'] == 200
    
    def test_sanitize_input_normal(self):
        """Test sanitizing normal input."""
        result = sanitize_input("  Hello World  ")
        assert result == "Hello World"
    
    def test_sanitize_input_max_length(self):
        """Test sanitizing input exceeding max length."""
        long_input = "A" * 1000
        result = sanitize_input(long_input, max_length=100)
        assert len(result) == 100
    
    def test_get_db_size_nonexistent(self):
        """Test getting size of non-existent directory."""
        result = get_db_size('/nonexistent/db')
        assert result == "0 MB"
    
    def test_get_db_size_empty(self):
        """Test getting size of empty directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = get_db_size(tmpdir)
            assert "KB" in result or "MB" in result
    
    def test_format_context_snippets(self):
        """Test formatting context snippets."""
        mock_contexts = [
            Mock(page_content="This is a test document with some content"),
            Mock(page_content="Another test document"),
            Mock(page_content="A" * 300)  # Long content
        ]
        
        result = format_context_snippets(mock_contexts, max_snippets=2)
        assert len(result) == 2
        assert result[0].startswith("[1]")
        assert result[1].startswith("[2]")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
