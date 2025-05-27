from typing import Any, Dict, List, Union # Added Dict, List, Union
import logging # Added logging

from pydantic import BaseModel
from .base_agent import BaseAgent, AgentOutput, TaskDefinition, TaskInputSpec, TaskOutputSpec
from .planner_agent import ValidatedSpecData # Import from planner_agent
from suite_core.app_spec import AppSpecification # Keep for process_request type hint
from suite_core.project_state import ProjectState

logger = logging.getLogger(__name__)

# --- Pydantic Models for Task I/O ---

class GenerateCodeInput(BaseModel):
    """Input for the 'generate_code_from_plan' task."""
    plan_data: ValidatedSpecData  # Data from PlannerAgent
    output_path: str              # Base output path for generated files

class RefactorCodeInput(BaseModel):
    """Input for the 'refactor_code' task."""
    files_to_refactor: List[str]
    refactoring_instructions: str

class GeneratedCodeOutput(BaseModel):
    """Output for code generation and refactoring tasks."""
    generated_files: List[str]

class CodeGenAgent(BaseAgent):
    async def process_request(self, app_spec: AppSpecification, project_state: ProjectState) -> AgentOutput:
        # This method might be deprecated or used for more general, non-task-specific interactions.
        logger.info("CodeGenAgent: Process request called. Typically expects a specific task via execute_task.")
        return AgentOutput(status="pending", message="Ready for a specific code generation or refactoring task.")

    async def execute_task(self, task_name: str, task_details: Union[GenerateCodeInput, RefactorCodeInput, Dict[str, Any]], project_state: ProjectState) -> AgentOutput:
        logger.info(f"CodeGenAgent: Executing task '{task_name}' with details: {task_details}")

        parsed_task_details: Union[GenerateCodeInput, RefactorCodeInput, None] = None

        if task_name == "generate_code_from_plan":
            if isinstance(task_details, GenerateCodeInput):
                parsed_task_details = task_details
            elif isinstance(task_details, dict):
                try:
                    parsed_task_details = GenerateCodeInput(**task_details)
                except Exception as e:
                    logger.error(f"Error parsing task_details for generate_code_from_plan: {e}")
                    return AgentOutput(status="failure", message=f"Invalid task_details for generate_code_from_plan: {e}")
            else:
                return AgentOutput(status="failure", message="Invalid task_details type for generate_code_from_plan.")
            
            # Simulate creating a file using output_path from parsed_task_details
            # For the simulation, we'll use the project_state's app_spec output_path if task_details.output_path is not directly usable
            # or if we want to ensure it's rooted correctly. In a real scenario, task_details.output_path would be primary.
            output_dir = parsed_task_details.output_path # This should be the apps/my_generated_app
            generated_file_path = f"{output_dir}/generated_code_from_plan.py" # Example file
            logger.info(f"Simulating code generation for: {output_dir}. Output file: {generated_file_path}")

            # Ensure generated_files list exists and append
            if project_state.generated_files is None: # Check if None, not hasattr
                project_state.generated_files = []
            project_state.generated_files.append(generated_file_path)
            
            output_data = GeneratedCodeOutput(generated_files=[generated_file_path])
            return AgentOutput(
                status="success",
                message=f"Code generation simulated. Output in {generated_file_path}.",
                output_data=output_data.dict(), # Ensure Pydantic model is dict for AgentOutput
                next_agent_hint="TestAgent"
            )

        elif task_name == "refactor_code":
            if isinstance(task_details, RefactorCodeInput):
                parsed_task_details = task_details
            elif isinstance(task_details, dict):
                try:
                    parsed_task_details = RefactorCodeInput(**task_details)
                except Exception as e:
                    logger.error(f"Error parsing task_details for refactor_code: {e}")
                    return AgentOutput(status="failure", message=f"Invalid task_details for refactor_code: {e}")
            else:
                return AgentOutput(status="failure", message="Invalid task_details type for refactor_code.")

            logger.info(f"Simulating refactoring for files: {parsed_task_details.files_to_refactor} with instructions: '{parsed_task_details.refactoring_instructions}'")
            # Simulate modifying files - for now, just list them as "modified"
            modified_files = [f"refactored_{os.path.basename(f)}" for f in parsed_task_details.files_to_refactor] # Simulate new names
            
            if project_state.generated_files is None:
                project_state.generated_files = []
            project_state.generated_files.extend(modified_files) # Add all "refactored" files
            
            output_data = GeneratedCodeOutput(generated_files=modified_files)
            return AgentOutput(
                status="success",
                message=f"Refactoring simulated. Modified files: {', '.join(modified_files)}.",
                output_data=output_data.dict(),
                next_agent_hint="TestAgent" # Or perhaps back to Planner or a ReviewAgent
            )
        else:
            logger.warning(f"CodeGenAgent: Unknown task_name '{task_name}'")
            return AgentOutput(status="failure", message=f"Unknown task_name: {task_name}")

    def get_capabilities(self) -> Dict[str, TaskDefinition]:
        return {
            "generate_code_from_plan": TaskDefinition(
                task_name="generate_code_from_plan",
                description="Generates code based on planning data (e.g., validated specification, template details).",
                input_spec=TaskInputSpec(
                    description="Plan details (ValidatedSpecData from PlannerAgent) and the target output path for code generation.",
                    schema=GenerateCodeInput
                ),
                output_spec=TaskOutputSpec(
                    description="List of paths to the generated code files.",
                    schema=GeneratedCodeOutput
                )
            ),
            "refactor_code": TaskDefinition(
                task_name="refactor_code",
                description="Refactors existing code files based on specific instructions.",
                input_spec=TaskInputSpec(
                    description="A list of file paths to refactor and natural language instructions for the refactoring process.",
                    schema=RefactorCodeInput
                ),
                output_spec=TaskOutputSpec(
                    description="List of paths to the modified or newly generated files resulting from refactoring.",
                    schema=GeneratedCodeOutput
                )
            )
        }
import os # Added os for basename in refactor_code simulation
