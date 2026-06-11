"""Main entry point for Distributed Task Scheduler"""

import asyncio
import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn

from scheduler.core import (
    DistributedScheduler,
    TaskDefinition,
    ResourceRequirements,
    TaskStatus,
    ConsensusType,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Distributed Task Scheduler API",
    description="Enterprise-grade distributed task orchestration system",
    version="1.0.0"
)

# Initialize scheduler
scheduler = DistributedScheduler(
    cluster_size=5,
    ml_model="transformer_v2",
    consensus_type=ConsensusType.PBFT
)


@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    logger.info("Scheduler service starting up")
    health = scheduler.get_cluster_health()
    logger.info(f"Cluster health: {health}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "cluster_health": scheduler.get_cluster_health()
    }


@app.post("/v1/tasks/schedule")
async def schedule_task(task_request: dict):
    """Schedule a new task"""
    try:
        task = TaskDefinition(
            id=task_request.get('id'),
            description=task_request['description'],
            priority=task_request.get('priority', 5),
            timeout_seconds=task_request.get('timeout_seconds', 3600),
            resource_requirements=ResourceRequirements(
                cpu_cores=task_request['resource_requirements'].get('cpu_cores', 1),
                memory_gb=task_request['resource_requirements'].get('memory_gb', 2),
                gpu_count=task_request['resource_requirements'].get('gpu_count', 0),
                gpu_memory_gb=task_request['resource_requirements'].get('gpu_memory_gb', 0),
            ),
            dependencies=task_request.get('dependencies', []),
            sla_guarantee=task_request.get('sla_guarantee', '95%'),
        )
        
        result = await scheduler.schedule_task(task)
        
        return {
            "task_id": result.task_id,
            "status": result.status.value,
            "worker_id": result.worker_id,
            "execution_time_ms": result.execution_time_ms,
        }
    except Exception as e:
        logger.error(f"Error scheduling task: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/v1/tasks/{task_id}/status")
async def get_task_status(task_id: str):
    """Get task execution status"""
    if task_id not in scheduler.task_results:
        raise HTTPException(status_code=404, detail="Task not found")
    
    result = scheduler.task_results[task_id]
    return {
        "task_id": result.task_id,
        "status": result.status.value,
        "execution_time_ms": result.execution_time_ms,
        "worker_id": result.worker_id,
        "output": result.output,
        "error": result.error,
        "metrics": result.metrics,
    }


@app.get("/v1/cluster/metrics")
async def get_cluster_metrics():
    """Get cluster-wide metrics"""
    return scheduler.get_cluster_health()


@app.get("/v1/cluster/status")
async def get_cluster_status():
    """Get detailed cluster status"""
    health = scheduler.get_cluster_health()
    return {
        "timestamp": __import__('datetime').datetime.now().isoformat(),
        "cluster_status": health,
        "consensus_type": "PBFT",
        "ml_model": "transformer_v2",
        "quorum_size": scheduler.consensus_engine.quorum_size,
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )


if __name__ == "__main__":
    logger.info("Starting Distributed Task Scheduler")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        workers=4,
        log_level="info"
    )
