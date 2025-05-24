from typing import Optional, List, Dict
from pydantic import BaseModel
from suite_core.app_spec import AppSpecification

class ProjectState(BaseModel):
    request_id: str
    current_status: str
    app_spec: AppSpecification
    generated_files: List[str] = []
    test_results: Optional[Dict] = None
    deployment_info: Optional[Dict] = None
    agent_history: List[Dict] = [] # Example: [{"agent_name": "PlannerAgent", "output": {...}, "timestamp": "..."}]
    error_log: List[str] = []
