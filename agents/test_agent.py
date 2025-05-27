from typing import Any, Dict, List, Optional, Union # Added Dict, List, Optional, Union
import logging # Added logging
import os # Added os for path manipulation in simulation

from pydantic import BaseModel
from .base_agent import BaseAgent, AgentOutput, TaskDefinition, TaskInputSpec, TaskOutputSpec
from suite_core.app_spec import AppSpecification # Keep for process_request type hint
from suite_core.project_state import ProjectState

logger = logging.getLogger(__name__)

# --- Pydantic Models for Task I/O ---

class GenerateTestsInput(BaseModel):
    """Input for the 'generate_tests' task."""
    files_to_test: List[str]
    test_strategy: Optional[str] = None

class GeneratedTestsOutput(BaseModel):
    """Output for the 'generate_tests' task."""
    generated_test_files: List[str]

class RunTestsInput(BaseModel):
    """Input for the 'run_tests' task."""
    test_files: List[str]
    code_files_under_test: List[str] # Added as per instruction

class TestRunOutput(BaseModel):
    """Output for the 'run_tests' task."""
    test_summary: Dict[str, Any] # e.g., {"passed": 5, "failed": 0, "coverage": "70%"}

class TestAgent(BaseAgent):
    async def process_request(self, app_spec: AppSpecification, project_state: ProjectState) -> AgentOutput:
        # This method might be deprecated or used for more general, non-task-specific interactions.
        logger.info("TestAgent: Process request called. Typically expects a specific task via execute_task.")
        return AgentOutput(status="pending", message="Ready for a specific testing task.")

    async def execute_task(self, task_name: str, task_details: Union[GenerateTestsInput, RunTestsInput, Dict[str, Any]], project_state: ProjectState) -> AgentOutput:
        logger.info(f"TestAgent: Executing task '{task_name}' with details: {task_details}")

        parsed_task_details: Union[GenerateTestsInput, RunTestsInput, None] = None

        if task_name == "generate_tests":
            if isinstance(task_details, GenerateTestsInput):
                parsed_task_details = task_details
            elif isinstance(task_details, dict):
                try:
                    parsed_task_details = GenerateTestsInput(**task_details)
                except Exception as e:
                    logger.error(f"Error parsing task_details for generate_tests: {e}")
                    return AgentOutput(status="failure", message=f"Invalid task_details for generate_tests: {e}")
            else:
                return AgentOutput(status="failure", message="Invalid task_details type for generate_tests.")

            logger.info(f"Simulating test generation for files: {parsed_task_details.files_to_test} with strategy: {parsed_task_details.test_strategy or 'default'}")
            
            generated_test_files = []
            for file_to_test in parsed_task_details.files_to_test:
                # Simulate creating a test file based on the original file name
                base, ext = os.path.splitext(file_to_test)
                # Assuming files might be in a directory like 'app/src/module.py'
                # We want to place tests in a similar structure, e.g., 'app/tests/test_module.py'
                # This is a simplified simulation for path handling.
                file_name = os.path.basename(base)
                # Try to place it in a 'tests' subdirectory relative to the app's output path.
                # project_state.app_spec.output_path could be like 'apps/my_generated_app'
                test_file_path = os.path.join(project_state.app_spec.output_path, "tests", f"test_{file_name}{ext if ext else '.py'}")
                generated_test_files.append(test_file_path)
            
            logger.info(f"Simulated generated test files: {generated_test_files}")
            
            # Update project_state if needed (e.g., if it tracks all generated files)
            if project_state.generated_files is None:
                project_state.generated_files = []
            project_state.generated_files.extend(generated_test_files) # Add new test files

            output_data = GeneratedTestsOutput(generated_test_files=generated_test_files)
            return AgentOutput(
                status="success",
                message=f"Test generation simulated. Generated files: {', '.join(generated_test_files)}",
                output_data=output_data.dict(),
                next_agent_hint="TestAgent" # Or CodeGenAgent if tests need to be written to disk by it
            )

        elif task_name == "run_tests":
            if isinstance(task_details, RunTestsInput):
                parsed_task_details = task_details
            elif isinstance(task_details, dict):
                try:
                    parsed_task_details = RunTestsInput(**task_details)
                except Exception as e:
                    logger.error(f"Error parsing task_details for run_tests: {e}")
                    return AgentOutput(status="failure", message=f"Invalid task_details for run_tests: {e}")
            else:
                return AgentOutput(status="failure", message="Invalid task_details type for run_tests.")

            logger.info(f"Simulating running tests for files: {parsed_task_details.test_files} against code: {parsed_task_details.code_files_under_test}")
            # Simulate test results
            simulated_test_results = {"passed": len(parsed_task_details.test_files) * 2, "failed": 0, "coverage": "85%"}
            
            project_state.test_results = simulated_test_results # Update project_state
            
            output_data = TestRunOutput(test_summary=simulated_test_results)
            return AgentOutput(
                status="success",
                message="Tests simulated. All passed (simulated).",
                output_data=output_data.dict(),
                next_agent_hint=None # Or DeployAgent if tests pass
            )
        else:
            logger.warning(f"TestAgent: Unknown task_name '{task_name}'")
            return AgentOutput(status="failure", message=f"Unknown task_name: {task_name}")

    def get_capabilities(self) -> Dict[str, TaskDefinition]:
        return {
            "generate_tests": TaskDefinition(
                task_name="generate_tests",
                description="Generates test files for specified source code files.",
                input_spec=TaskInputSpec(
                    description="Files to generate tests for and an optional testing strategy.",
                    schema=GenerateTestsInput
                ),
                output_spec=TaskOutputSpec(
                    description="List of paths to the generated test files.",
                    schema=GeneratedTestsOutput
                )
            ),
            "run_tests": TaskDefinition(
                task_name="run_tests",
                description="Runs specified test files against corresponding code files and reports results.",
                input_spec=TaskInputSpec(
                    description="Test files and the code files they are intended to test.",
                    schema=RunTestsInput
                ),
                output_spec=TaskOutputSpec(
                    description="A summary of the test execution results, including pass/fail counts and coverage.",
                    schema=TestRunOutput
                )
            )
        }
