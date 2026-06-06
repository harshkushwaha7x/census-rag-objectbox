"""
Unit tests for performance monitoring module.
"""

import os
import sys
import pytest
import json
import tempfile

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from performance import PerformanceMonitor, QueryMetrics


class TestPerformanceMonitor:
    """Test cases for PerformanceMonitor class."""
    
    def test_initialization(self):
        """Test monitor initialization."""
        monitor = PerformanceMonitor()
        assert len(monitor.metrics) == 0
        assert monitor.start_time > 0
    
    def test_record_query_success(self):
        """Test recording a successful query."""
        monitor = PerformanceMonitor()
        monitor.record_query(
            query="What is the population?",
            retrieval_time=0.5,
            generation_time=1.2,
            num_chunks=3,
            success=True
        )
        
        assert len(monitor.metrics) == 1
        assert monitor.metrics[0].query == "What is the population?"
        assert monitor.metrics[0].retrieval_time == 0.5
        assert monitor.metrics[0].generation_time == 1.2
        assert monitor.metrics[0].total_time == 1.7
        assert monitor.metrics[0].num_chunks_retrieved == 3
        assert monitor.metrics[0].success is True
    
    def test_record_query_failure(self):
        """Test recording a failed query."""
        monitor = PerformanceMonitor()
        monitor.record_query(
            query="Invalid query",
            retrieval_time=0.1,
            generation_time=0.0,
            num_chunks=0,
            success=False,
            error="API Error"
        )
        
        assert len(monitor.metrics) == 1
        assert monitor.metrics[0].success is False
        assert monitor.metrics[0].error_message == "API Error"
    
    def test_get_statistics_empty(self):
        """Test getting statistics with no queries."""
        monitor = PerformanceMonitor()
        stats = monitor.get_statistics()
        
        assert stats['total_queries'] == 0
        assert stats['avg_response_time'] == 0
        assert stats['success_rate'] == 0
    
    def test_get_statistics_with_queries(self):
        """Test getting statistics with recorded queries."""
        monitor = PerformanceMonitor()
        
        # Record successful queries
        monitor.record_query("Query 1", 0.5, 1.0, 3, success=True)
        monitor.record_query("Query 2", 0.6, 1.2, 4, success=True)
        monitor.record_query("Query 3", 0.4, 0.8, 2, success=False)
        
        stats = monitor.get_statistics()
        
        assert stats['total_queries'] == 3
        assert stats['successful_queries'] == 2
        assert stats['failed_queries'] == 1
        assert stats['success_rate'] == pytest.approx(66.67, rel=0.01)
        assert stats['avg_response_time'] > 0
        assert stats['avg_chunks_retrieved'] == 3.5
    
    def test_get_recent_queries(self):
        """Test getting recent queries."""
        monitor = PerformanceMonitor()
        
        for i in range(15):
            monitor.record_query(f"Query {i}", 0.5, 1.0, 3, success=True)
        
        recent = monitor.get_recent_queries(limit=5)
        
        assert len(recent) == 5
        assert recent[-1]['query'].startswith("Query 14")
    
    def test_export_metrics(self):
        """Test exporting metrics to file."""
        monitor = PerformanceMonitor()
        monitor.record_query("Test query", 0.5, 1.0, 3, success=True)
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            filepath = f.name
        
        try:
            monitor.export_metrics(filepath)
            
            # Verify file exists and contains data
            assert os.path.exists(filepath)
            
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            assert 'statistics' in data
            assert 'queries' in data
            assert len(data['queries']) == 1
        finally:
            if os.path.exists(filepath):
                os.unlink(filepath)
    
    def test_reset_metrics(self):
        """Test resetting metrics."""
        monitor = PerformanceMonitor()
        monitor.record_query("Query", 0.5, 1.0, 3, success=True)
        
        assert len(monitor.metrics) == 1
        
        monitor.reset_metrics()
        
        assert len(monitor.metrics) == 0


class TestQueryMetrics:
    """Test cases for QueryMetrics dataclass."""
    
    def test_query_metrics_creation(self):
        """Test creating QueryMetrics instance."""
        metric = QueryMetrics(
            query="Test query",
            timestamp="2024-01-01T00:00:00",
            retrieval_time=0.5,
            generation_time=1.0,
            total_time=1.5,
            num_chunks_retrieved=3,
            success=True
        )
        
        assert metric.query == "Test query"
        assert metric.retrieval_time == 0.5
        assert metric.generation_time == 1.0
        assert metric.total_time == 1.5
        assert metric.num_chunks_retrieved == 3
        assert metric.success is True
        assert metric.error_message is None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
