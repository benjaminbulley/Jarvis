from typing import Any
from .base_agent import BaseAgent, AgentOutput
from suite_core.app_spec import AppSpecification
from suite_core.project_state import ProjectState

class PlannerAgent(BaseAgent):
    async def process_request(self, app_spec: AppSpecification, project_state: ProjectState) -> AgentOutput:
        print(f"PlannerAgent: Processing request {app_spec.request_id} - '{app_spec.user_prompt[:50]}...'")
        # Simulate planning
        plan = "1. Generate code. 2. Run tests. 3. Deploy (simulated)."
        return AgentOutput(
            status="success",
            message="Initial plan created.",
            output_data={"plan": plan},
            next_agent_hint="CodeGenAgent"
        )

    async def execute_task(self, task_details: Any, project_state: ProjectState) -> AgentOutput:
        print("PlannerAgent: Execute task called (not typically used for this agent, using process_request instead).")
        return AgentOutput(status="success", message="No specific task executed by planner via execute_task.")

    def get_capabilities(self) -> dict:
        return {
            "name": "PlannerAgent",
            "description": "Takes an app specification and creates a high-level plan.",
            "tasks": ["create_plan_from_spec"]
        }
