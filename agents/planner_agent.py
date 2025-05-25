from typing import Any, Dict, Optional, List
import os
import json
import logging

from .base_agent import BaseAgent, AgentOutput
from suite_core.app_spec import AppSpecification
from suite_core.project_state import ProjectState

logger = logging.getLogger(__name__)

def is_safe_output_path(path: str) -> bool:
    """
    Checks if the provided path string is safe for use as an output directory name.
    A safe path is non-empty, relative, and does not attempt to traverse upwards (e.g., contain "..").

    Args:
        path (str): The path string to validate.

    Returns:
        bool: True if the path is considered safe, False otherwise.
    """
    if not path: return False
    # Disallow '..' and absolute paths
    if ".." in path or os.path.isabs(path):
        return False
    # Optionally, restrict characters or length if needed
    # For now, this basic check is aligned with CodeGenAgent's existing check
    return True

class PlannerAgent(BaseAgent):
    """
    The PlannerAgent is responsible for the initial validation of the AppSpecification.
    It ensures that the request is well-formed and consistent with available resources
    (like templates) and project constraints before proceeding to code generation.

    Key validation checks include:
    - Existence and validity of the specified template (directory and manifest file).
    - Safety and validity of the specified output path.
    - Consistency of provided placeholder values against those defined in the
      template's manifest (issues warnings for discrepancies).
    """
    async def process_request(self, app_spec: AppSpecification, project_state: ProjectState) -> AgentOutput:
        """
        Validates the incoming AppSpecification and prepares data for subsequent agents.

        Args:
            app_spec (AppSpecification): The application specification to validate.
            project_state (ProjectState): The current project state (not significantly modified by this agent,
                                          but passed for interface consistency).

        Returns:
            AgentOutput:
                - If validation is successful:
                    - `status`: "success"
                    - `message`: A summary of validation, including any warnings.
                    - `output_data`: A dictionary containing:
                        - `validated_template_id` (str): The ID of the validated template.
                        - `template_manifest_path` (str): Path to the template's manifest file.
                        - `template_manifest_content` (dict): The parsed content of the manifest.
                        - `warnings` (List[str]): A list of warnings generated during validation
                                                  (e.g., for missing optional placeholder values).
                    - `next_agent_hint`: "CodeGenAgent"
                - If critical validation fails:
                    - `status`: "failure"
                    - `message`: A description of the validation error.
                    - `output_data`: None
        """
        logger.info(f"PlannerAgent: Processing request {app_spec.request_id} for '{app_spec.user_prompt[:50]}...'")
        warnings: List[str] = []
        manifest_data: Optional[Dict[str, Any]] = None
        manifest_path: Optional[str] = None

        # 1. Validate template_to_use and manifest
        if not app_spec.template_to_use or not isinstance(app_spec.template_to_use, str):
            msg = "AppSpecification.template_to_use is missing or invalid."
            logger.error(msg)
            return AgentOutput(status="failure", message=msg)

        template_dir = os.path.join("templates", app_spec.template_to_use)
        if not os.path.isdir(template_dir):
            msg = f"Template directory not found: {template_dir}"
            logger.error(msg)
            return AgentOutput(status="failure", message=msg)

        manifest_path = os.path.join(template_dir, "template_manifest.json")
        if not os.path.isfile(manifest_path):
            msg = f"Template manifest not found: {manifest_path}"
            logger.error(msg)
            return AgentOutput(status="failure", message=msg)

        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest_data = json.load(f)
        except json.JSONDecodeError as e:
            msg = f"Error decoding JSON from manifest {manifest_path}: {e}"
            logger.exception(msg) # Use exception for stack trace
            return AgentOutput(status="failure", message=msg)
        except IOError as e:
            msg = f"IOError reading manifest file {manifest_path}: {e}"
            logger.exception(msg)
            return AgentOutput(status="failure", message=msg)
        except Exception as e:
            msg = f"Unexpected error loading manifest {manifest_path}: {e}"
            logger.exception(msg)
            return AgentOutput(status="failure", message=msg)
        
        if not manifest_data: # Should be caught by exceptions, but as a safeguard
            msg = f"Manifest data could not be loaded from {manifest_path}."
            logger.error(msg)
            return AgentOutput(status="failure", message=msg)

        # 2. Validate output_path
        if not app_spec.output_path or not isinstance(app_spec.output_path, str):
            msg = "AppSpecification.output_path is missing or invalid."
            logger.error(msg)
            return AgentOutput(status="failure", message=msg)
        
        if not is_safe_output_path(app_spec.output_path):
            msg = (f"AppSpecification.output_path '{app_spec.output_path}' is unsafe. "
                   "It must be a relative path and cannot contain '..'.")
            logger.error(msg)
            return AgentOutput(status="failure", message=msg)

        # 3. Validate placeholder_values (Conditional)
        placeholder_definitions: Dict[str, Any] = manifest_data.get("placeholder_definitions", {})
        
        if placeholder_definitions: # If the template defines placeholders
            if app_spec.placeholder_values is None:
                warning_msg = (f"Template '{app_spec.template_to_use}' defines placeholders, "
                               "but AppSpecification.placeholder_values is missing (None).")
                warnings.append(warning_msg)
                logger.warning(warning_msg)
            elif not isinstance(app_spec.placeholder_values, dict):
                # This case should ideally be caught by Pydantic, but as a safeguard:
                warning_msg = (f"Template '{app_spec.template_to_use}' defines placeholders, "
                               "but AppSpecification.placeholder_values is not a dictionary.")
                warnings.append(warning_msg)
                logger.warning(warning_msg)
            else: # placeholder_values is a dict
                for key in placeholder_definitions.keys():
                    if key not in app_spec.placeholder_values:
                        warning_msg = (f"Placeholder '{key}' defined in template manifest for '{app_spec.template_to_use}' "
                                       "is missing from AppSpecification.placeholder_values.")
                        warnings.append(warning_msg)
                        logger.warning(warning_msg)
        
        # 4. Handle Successful Validation
        success_message = "PlannerAgent: AppSpecification validated successfully."
        if warnings:
            success_message += " Warnings: " + "; ".join(warnings)
        
        output_data = {
            "validated_template_id": app_spec.template_to_use,
            "template_manifest_path": manifest_path, # Still useful for context/logging
            "template_manifest_content": manifest_data, # The actual parsed JSON content
            "warnings": warnings
            # Old simulated plan data removed.
        }
        
        logger.info(success_message)
        return AgentOutput(
            status="success",
            message=success_message,
            output_data=output_data,
            next_agent_hint="CodeGenAgent" # As it was previously
        )

    async def execute_task(self, task_details: Any, project_state: ProjectState) -> AgentOutput:
        logger.info("PlannerAgent: Execute task called (not typically used for this agent, using process_request instead).")
        return AgentOutput(status="success", message="No specific task executed by planner via execute_task.")

    def get_capabilities(self) -> dict:
        return {
            "name": "PlannerAgent",
            "description": "Takes an app specification and creates a high-level plan.",
            "tasks": ["create_plan_from_spec"]
        }
