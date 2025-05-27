import abc
from typing import Optional, List, Any, Dict, Type # Added Type
from pydantic import BaseModel
from suite_core.app_spec import AppSpecification
from suite_core.project_state import ProjectState

# --- Task Specification Models ---

class TaskInputSpec(BaseModel):
    """
    Describes the expected input schema for an agent's task.
    The `schema` field itself refers to another Pydantic model
    that defines the structure of `task_details` for a specific task.
    """
    description: str  # Describes the input data
    schema: Type[BaseModel]  # The Pydantic model defining the structure of task_details

class TaskOutputSpec(BaseModel):
    """
    Describes the expected output schema for an agent's task.
    The `schema` field itself refers to another Pydantic model
    that defines the structure of `output_data` for a specific task.
    """
    description: str  # Describes the output data
    schema: Type[BaseModel]  # The Pydantic model defining the structure of output_data

class TaskDefinition(BaseModel):
    """
    Provides a structured definition for a task that an agent can perform.
    It includes the task's name, a human-readable description, and
    specifications for its input and output data structures.
    """
    task_name: str
    description: str
    input_spec: TaskInputSpec
    output_spec: TaskOutputSpec

# --- Agent Output Model ---

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
    def get_capabilities(self) -> Dict[str, TaskDefinition]: # Updated return type hint
        pass
