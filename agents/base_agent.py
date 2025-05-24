import abc
from typing import Optional, List, Any, Dict
from pydantic import BaseModel
from suite_core.app_spec import AppSpecification
from suite_core.project_state import ProjectState

class AgentOutput(BaseModel):
    status: str
    output_data: Optional[Dict] = None
    message: Optional[str] = None
    next_agent_hint: Optional[str] = None
    request_clarification: Optional[str] = None

class BaseAgent(abc.ABC):
    @abc.abstractmethod
    async def process_request(self, app_spec: AppSpecification, project_state: ProjectState) -> AgentOutput:
        pass

    @abc.abstractmethod
    async def execute_task(self, task_details: Any, project_state: ProjectState) -> AgentOutput:
        pass

    @abc.abstractmethod
    def get_capabilities(self) -> dict:
        pass
