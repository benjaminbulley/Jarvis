# Agents

Agents are the core workers in the Autonomous App Suite. They are specialized Python classes responsible for performing specific tasks in the app generation lifecycle.

## Base Agent (`base_agent.py`)

All agents must inherit from the `BaseAgent` abstract base class. This class defines the common interface for all agents:

*   `async process_request(self, app_spec: AppSpecification, project_state: ProjectState) -> AgentOutput:`:
    Typically called for the first agent in a chain, or when an agent needs to primarily work from the overall `AppSpecification`. It should process the request and can delegate to its own `execute_task` or suggest the next agent.
*   `async execute_task(self, task_details: Any, project_state: ProjectState) -> AgentOutput:`:
    Called when an agent needs to perform a specific, well-defined task, often based on the output of a previous agent. The `task_details` will vary depending on the agent and task.
*   `get_capabilities(self) -> dict:`:
    Returns a dictionary describing the agent's name, purpose, and the tasks it can perform. This can be used by the orchestrator for agent selection.

The `AgentOutput` Pydantic model is used as the return type for `process_request` and `execute_task`. It includes status, messages, output data, and hints for the next agent.

## Creating a New Agent

1.  **Define the Agent Class:**
    Create a new Python file in the `agents/` directory (e.g., `my_new_agent.py`).
    Define your class, inheriting from `BaseAgent`:
    ```python
    from .base_agent import BaseAgent, AgentOutput
    from suite_core.app_spec import AppSpecification # If needed
    from suite_core.project_state import ProjectState # If needed
    from typing import Any

    class MyNewAgent(BaseAgent):
        async def process_request(self, app_spec: AppSpecification, project_state: ProjectState) -> AgentOutput:
            # Logic for processing the initial request
            # ...
            return AgentOutput(status="success", message="Processed by MyNewAgent")

        async def execute_task(self, task_details: Any, project_state: ProjectState) -> AgentOutput:
            # Logic for executing a specific task
            # ...
            return AgentOutput(status="success", message=f"Task {task_details} executed by MyNewAgent")

        def get_capabilities(self) -> dict:
            return {
                "name": "MyNewAgent",
                "description": "Description of what MyNewAgent does.",
                "tasks": ["my_specific_task_1", "my_specific_task_2"]
            }
    ```

2.  **Implement Agent Logic:**
    Fill in the logic for `process_request` and/or `execute_task`. Agents can interact with the `ProjectState` to get context or update it with their results (e.g., adding generated file paths, test results).

3.  **Register the Agent (Conceptual):**
    *   Add your new agent to `agents/__init__.py` to make it easily importable.
    *   Add its configuration to `config/agent_config.yaml`. This allows the orchestrator (once fully developed) to discover and use your agent.

## Example Agents

*   **`PlannerAgent`:** (Simulated) Takes an `AppSpecification` and creates a high-level plan.
*   **`CodeGenAgent`:** (Simulated) Generates code based on instructions.
*   **`TestAgent`:** (Simulated) Runs tests on generated code.

These examples provide a starting point for developing more sophisticated agents.
