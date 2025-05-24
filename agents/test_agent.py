from typing import Any
from .base_agent import BaseAgent, AgentOutput
from suite_core.app_spec import AppSpecification
from suite_core.project_state import ProjectState

class TestAgent(BaseAgent):
    async def process_request(self, app_spec: AppSpecification, project_state: ProjectState) -> AgentOutput:
        print("TestAgent: Process request called. Typically expects a specific task via execute_task.")
        return AgentOutput(status="pending", message="Ready for testing task.")

    async def execute_task(self, task_details: Any, project_state: ProjectState) -> AgentOutput:
        print(f"TestAgent: Executing task: {task_details}. Simulating running tests for {project_state.app_spec.output_path}.")
        # Simulate test results
        test_results = {"passed": 5, "failed": 0, "coverage": "70%"}
        
        project_state.test_results = test_results
        
        return AgentOutput(
            status="success",
            message="Tests simulated. All passed.",
            output_data={"test_summary": test_results},
            next_agent_hint="DeployAgent" # DeployAgent not created in this step
        )

    def get_capabilities(self) -> dict:
        return {
            "name": "TestAgent",
            "description": "Generates and runs tests for code.",
            "tasks": ["generate_tests", "run_tests"]
        }
