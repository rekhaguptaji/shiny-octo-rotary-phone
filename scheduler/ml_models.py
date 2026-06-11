"""Machine Learning Models for Task Optimization"""

import numpy as np
from typing import Tuple, List
import logging

logger = logging.getLogger(__name__)


class TransformerPredictor:
    """Transformer-based model for task prediction and optimization"""

    def __init__(self, vocab_size: int = 1000, embedding_dim: int = 256):
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.attention_heads = 8
        self.layers = 6
        self.model_params = self._count_parameters()
        logger.info(
            f"TransformerPredictor initialized: "
            f"params={self.model_params:,.0f}, "
            f"embedding_dim={embedding_dim}"
        )

    def _count_parameters(self) -> int:
        """Calculate total model parameters"""
        # Embedding layer
        embedding_params = self.vocab_size * self.embedding_dim
        
        # Transformer layers
        layer_params = (
            self.embedding_dim * 4 * self.embedding_dim +  # Feed-forward
            self.embedding_dim * self.embedding_dim * 3 +   # QKV projections
            self.embedding_dim * 2  # Layer norms
        )
        
        return embedding_params + (layer_params * self.layers)

    def encode_task(self, task_features: np.ndarray) -> np.ndarray:
        """Encode task features using transformer embeddings"""
        # Simulated embedding lookup
        batch_size, seq_len = task_features.shape
        embeddings = np.random.randn(batch_size, seq_len, self.embedding_dim)
        return embeddings

    def self_attention(self, query: np.ndarray, key: np.ndarray, value: np.ndarray) -> np.ndarray:
        """Multi-head self-attention mechanism"""
        scores = np.dot(query, key.T) / np.sqrt(self.embedding_dim)
        attention_weights = np._softmax(scores, axis=-1)
        output = np.dot(attention_weights, value)
        return output

    def predict_resource_allocation(self, tasks: List[dict]) -> dict:
        """Predict optimal resource allocation for task batch"""
        allocations = {}
        
        for task in tasks:
            # Extract task complexity
            complexity_score = (
                len(task.get('dependencies', [])) * 0.3 +
                task.get('priority', 5) * 0.2 +
                task.get('timeout_seconds', 3600) / 1000 * 0.5
            )
            
            # Predict resources needed
            cpu_allocation = min(32, max(1, int(complexity_score / 10 * 8)))
            memory_allocation = min(256, max(4, int(complexity_score / 5)))
            
            allocations[task['id']] = {
                'cpu_cores': cpu_allocation,
                'memory_gb': memory_allocation,
                'estimated_duration': complexity_score * 100
            }
        
        return allocations


class GraphNeuralNetwork:
    """GNN for task dependency graph analysis"""

    def __init__(self, num_node_features: int = 16, num_output_features: int = 8):
        self.num_node_features = num_node_features
        self.num_output_features = num_output_features
        self.layers = 3
        logger.info(f"GraphNeuralNetwork initialized: layers={self.layers}")

    def build_dependency_graph(self, tasks: List[dict]) -> dict:
        """Construct adjacency matrix from task dependencies"""
        n_tasks = len(tasks)
        adjacency_matrix = np.zeros((n_tasks, n_tasks))
        task_id_map = {task['id']: i for i, task in enumerate(tasks)}
        
        for i, task in enumerate(tasks):
            for dep_id in task.get('dependencies', []):
                if dep_id in task_id_map:
                    j = task_id_map[dep_id]
                    adjacency_matrix[i, j] = 1
        
        return {'matrix': adjacency_matrix, 'id_map': task_id_map}

    def detect_bottlenecks(self, graph: dict) -> List[str]:
        """Identify critical path tasks (bottlenecks)"""
        adjacency = graph['matrix']
        # Tasks with high in-degree are bottlenecks
        in_degrees = np.sum(adjacency, axis=0)
        out_degrees = np.sum(adjacency, axis=1)
        
        bottleneck_indices = np.where((in_degrees + out_degrees) > 2)[0]
        id_map_reverse = {v: k for k, v in graph['id_map'].items()}
        
        return [id_map_reverse.get(idx, f"task_{idx}") for idx in bottleneck_indices]

    def compute_critical_path(self, tasks: List[dict]) -> Tuple[float, List[str]]:
        """Compute critical path and estimated completion time"""
        graph = self.build_dependency_graph(tasks)
        adjacency = graph['matrix']
        
        # Simulated critical path calculation
        n_tasks = len(tasks)
        durations = [np.random.uniform(1, 100) for _ in range(n_tasks)]
        
        # Simple approximation: sum of all tasks on critical path
        critical_path_duration = sum(durations) / 2
        critical_tasks = [tasks[i]['id'] for i in range(min(3, n_tasks))]
        
        return critical_path_duration, critical_tasks


class AnomalyDetector:
    """Detect anomalies and failures in task execution"""

    def __init__(self, sensitivity: float = 0.95):
        self.sensitivity = sensitivity
        self.baseline_metrics = {}
        logger.info(f"AnomalyDetector initialized: sensitivity={sensitivity}")

    def detect_anomaly(self, metrics: dict) -> Tuple[bool, str]:
        """Detect if task metrics indicate anomaly"""
        # Check CPU utilization
        cpu_util = metrics.get('cpu_utilization', 0)
        if cpu_util > 95:
            return True, "Extremely high CPU utilization"
        
        # Check memory pressure
        mem_util = metrics.get('memory_utilization', 0)
        if mem_util > 90:
            return True, "Memory pressure detected"
        
        # Check execution time deviation
        exec_time = metrics.get('execution_time_ms', 0)
        if exec_time > 300000:  # 5 minutes
            return True, "Unusually long execution time"
        
        # Check for errors
        error_rate = metrics.get('error_rate', 0)
        if error_rate > 0.1:
            return True, "High error rate detected"
        
        return False, "Metrics normal"

    def predict_failure(self, task_history: List[dict]) -> Tuple[float, str]:
        """Predict probability of task failure"""
        if not task_history:
            return 0.0, "No history available"
        
        # Calculate failure rate from history
        failures = sum(1 for t in task_history if t.get('status') == 'failed')
        failure_rate = failures / len(task_history)
        
        # Assess risk level
        if failure_rate > 0.3:
            risk_level = "High"
        elif failure_rate > 0.1:
            risk_level = "Medium"
        else:
            risk_level = "Low"
        
        return failure_rate, risk_level
