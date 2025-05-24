from typing import Any
from .base_agent import BaseAgent, AgentOutput
from suite_core.app_spec import AppSpecification
from suite_core.project_state import ProjectState

class CodeGenAgent(BaseAgent):
    async def process_request(self, app_spec: AppSpecification, project_state: ProjectState) -> AgentOutput:
        print("CodeGenAgent: Process request called. Typically expects a specific task via execute_task.")
        return AgentOutput(status="pending", message="Ready for code generation task.")

    async def execute_task(self, task_details: Any, project_state: ProjectState) -> AgentOutput:
        print(f"CodeGenAgent: Executing task: {task_details}. Simulating code generation for {project_state.app_spec.output_path}.")
        # Simulate creating a file
        generated_file_path = f"{project_state.app_spec.output_path}/generated_code.py"
        
        # Ensure generated_files list exists and append
        if not hasattr(project_state, 'generated_files') or project_state.generated_files is None:
            project_state.generated_files = []
        project_state.generated_files.append(generated_file_path)
        
        return AgentOutput(
            status="success",
            message=f"Code generation simulated. Output in {generated_file_path}.",
            output_data={"generated_files": [generated_file_path]},
            next_agent_hint="TestAgent"
        )

    def get_capabilities(self) -> dict:
        return {
            "name": "CodeGenAgent",
            "description": "Generates code based on specifications or plans.",
            "tasks": ["generate_code_from_plan", "refactor_code"]
        }
