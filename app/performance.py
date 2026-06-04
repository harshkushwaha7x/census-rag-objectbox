"""
Performance monitoring and metrics tracking for Census RAG.
"""

import time
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json

logger = logging.getLogger(__name__)


@dataclass
class QueryMetrics:
    """Store metrics for a single query."""
    query: str
    timestamp: str
    retrieval_time: float
    generation_time: float
    total_time: float
    num_chunks_retrieved: int
    success: bool
    error_message: Optional[str] = None


class PerformanceMonitor:
    """Monitor and track application performance."""
    
    def __init__(self):
        self.metrics: List[QueryMetrics] = []
        self.start_time = time.time()
        logger.info("Performance monitor initialized")
    
    def record_query(
        self,
        query: str,
        retrieval_time: float,
        generation_time: float,
        num_chunks: int,
        success: bool = True,
        error: Optional[str] = None
    ) -> None:
        """
        Record metrics for a query.
        
        Args:
            query: The user query
            retrieval_time: Time taken for retrieval (seconds)
            generation_time: Time taken for answer generation (seconds)
            num_chunks: Number of document chunks retrieved
            success: Whether the query was successful
            error: Error message if query failed
        """
        metric = QueryMetrics(
            query=query,
            timestamp=datetime.now().isoformat(),
            retrieval_time=retrieval_time,
            generation_time=generation_time,
            total_time=retrieval_time + generation_time,
            num_chunks_retrieved=num_chunks,
            success=success,
            error_message=error
        )
        
        self.metrics.append(metric)
        logger.info(f"Query recorded: {query[:50]}... | Time: {metric.total_time:.2f}s")
    
    def get_statistics(self) -> Dict:
        """
        Get performance statistics.
        
        Returns:
            dict: Performance statistics
        """
        if not self.metrics:
            return {
                "total_queries": 0,
                "avg_response_time": 0,
                "avg_retrieval_time": 0,
                "avg_generation_time": 0,
                "success_rate": 0,
                "uptime_hours": 0
            }
        
        successful_queries = [m for m in self.metrics if m.success]
        
        stats = {
            "total_queries": len(self.metrics),
            "successful_queries": len(successful_queries),
            "failed_queries": len(self.metrics) - len(successful_queries),
            "success_rate": len(successful_queries) / len(self.metrics) * 100,
            "avg_response_time": sum(m.total_time for m in successful_queries) / len(successful_queries) if successful_queries else 0,
            "avg_retrieval_time": sum(m.retrieval_time for m in successful_queries) / len(successful_queries) if successful_queries else 0,
            "avg_generation_time": sum(m.generation_time for m in successful_queries) / len(successful_queries) if successful_queries else 0,
            "avg_chunks_retrieved": sum(m.num_chunks_retrieved for m in successful_queries) / len(successful_queries) if successful_queries else 0,
            "min_response_time": min(m.total_time for m in successful_queries) if successful_queries else 0,
            "max_response_time": max(m.total_time for m in successful_queries) if successful_queries else 0,
            "uptime_hours": (time.time() - self.start_time) / 3600
        }
        
        return stats
    
    def get_recent_queries(self, limit: int = 10) -> List[Dict]:
        """
        Get recent query metrics.
        
        Args:
            limit: Number of recent queries to return
            
        Returns:
            list: Recent query metrics
        """
        recent = self.metrics[-limit:]
        return [
            {
                "query": m.query[:100],
                "timestamp": m.timestamp,
                "total_time": f"{m.total_time:.2f}s",
                "success": m.success
            }
            for m in recent
        ]
    
    def export_metrics(self, filepath: str) -> None:
        """
        Export metrics to JSON file.
        
        Args:
            filepath: Path to save the metrics file
        """
        try:
            metrics_data = {
                "statistics": self.get_statistics(),
                "queries": [
                    {
                        "query": m.query,
                        "timestamp": m.timestamp,
                        "retrieval_time": m.retrieval_time,
                        "generation_time": m.generation_time,
                        "total_time": m.total_time,
                        "num_chunks": m.num_chunks_retrieved,
                        "success": m.success,
                        "error": m.error_message
                    }
                    for m in self.metrics
                ]
            }
            
            with open(filepath, 'w') as f:
                json.dump(metrics_data, f, indent=2)
            
            logger.info(f"Metrics exported to {filepath}")
        except Exception as e:
            logger.error(f"Failed to export metrics: {str(e)}")
    
    def reset_metrics(self) -> None:
        """Clear all recorded metrics."""
        self.metrics.clear()
        self.start_time = time.time()
        logger.info("Metrics reset")


# Global performance monitor instance
performance_monitor = PerformanceMonitor()
