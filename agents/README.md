# Agents

Agents are the core workers in the Autonomous App Suite. They are specialized Python classes responsible for performing specific tasks in the app generation lifecycle.

## Base Agent (`base_agent.py`)

All agents must inherit from the `BaseAgent` abstract base class defined in `agents/base_agent.py`. This class defines the common interface for all agents:

*   `async process_request(self, app_spec: AppSpecification, project_state: ProjectState) -> AgentOutput:`:
    This method is typically called when an agent needs to perform a more general task based on the overall `AppSpecification`, or it might be the entry point for the first agent in a sequence. Its role can be to initialize a process or to delegate to a more specific task via `execute_task`.
*   `async execute_task(self, task_name: str, task_details: Any, project_state: ProjectState) -> AgentOutput:`:
    This is the primary method for performing a specific, well-defined task.
    -   `task_name` (str): Identifies the specific task the agent should perform (e.g., "generate_code_from_plan").
    -   `task_details` (Any): Contains the input data required for the task. This data should conform to the Pydantic schema defined in the `TaskInputSpec` for the corresponding `task_name` in `get_capabilities()`.
*   `get_capabilities(self) -> Dict[str, TaskDefinition]:`:
    Returns a dictionary where keys are task names (strings) and values are `TaskDefinition` objects. This method advertises the agent's capabilities to the orchestrator.
    *   **`TaskDefinition`**: A Pydantic model that describes a specific task. It includes:
        *   `task_name` (str): The unique identifier for the task.
        *   `description` (str): A human-readable description of the task.
        *   `input_spec` (`TaskInputSpec`): Defines the expected input for the task.
        *   `output_spec` (`TaskOutputSpec`): Defines the expected output of the task.
    *   **`TaskInputSpec`**: A Pydantic model describing the input requirements.
        *   `description` (str): Describes the input data.
        *   `schema` (Type[BaseModel]): A reference to a Pydantic model that defines the structure of `task_details` expected by `execute_task`.
    *   **`TaskOutputSpec`**: A Pydantic model describing the output structure.
        *   `description` (str): Describes the output data.
        *   `schema` (Type[BaseModel]): A reference to a Pydantic model that defines the structure of the `output_data` field within the `AgentOutput` returned by `execute_task`.

The `AgentOutput` Pydantic model is used as the return type for both `process_request` and `execute_task`. It includes:
*   `status` (str): "success", "failure", "pending", etc.
*   `output_data` (Optional[Dict]): A dictionary containing the results of the task. For tasks defined in `get_capabilities`, this dictionary should conform to the `schema` specified in the `TaskOutputSpec`.
*   `message` (Optional[str]): A human-readable message about the outcome.
*   `next_agent_hint` (Optional[str]): A suggestion for the next agent to handle the workflow.
*   `request_clarification` (Optional[str]): If the agent needs more information.

## Creating a New Agent

1.  **Define Task-Specific Pydantic Models:**
    Before creating the agent, define Pydantic models for the inputs and outputs of the tasks your agent will perform. These models will be referenced in `TaskInputSpec` and `TaskOutputSpec`.

    ```python
    # In your_agent_file.py or a shared models file
    from pydantic import BaseModel
    from typing import List

    class MyTaskInput(BaseModel):
        item_id: int
        description: str

    class MyTaskOutput(BaseModel):
        processed_item_id: int
        status_message: str
        generated_artifacts: List[str]
    ```

2.  **Define the Agent Class:**
    Create a new Python file in the `agents/` directory (e.g., `my_new_agent.py`).
    Define your class, inheriting from `BaseAgent` and the new task specification models from `agents.base_agent`.

    ```python
    # In agents/my_new_agent.py
    import logging
    from typing import Any, Dict, Union # Union for task_details type hint
    from pydantic import BaseModel # For task I/O models if defined in the same file

    from .base_agent import BaseAgent, AgentOutput, TaskDefinition, TaskInputSpec, TaskOutputSpec
    # If MyTaskInput/MyTaskOutput are in a different file, import them:
    # from .my_agent_models import MyTaskInput, MyTaskOutput 
    from suite_core.app_spec import AppSpecification
    from suite_core.project_state import ProjectState

    logger = logging.getLogger(__name__)

    # Example Pydantic models for task I/O (can be in a separate file)
    class MyTaskInput(BaseModel):
        item_id: int
        instruction: str

    class MyTaskOutput(BaseModel):
        item_id: int
        result: str
        is_complete: bool

    class MyNewAgent(BaseAgent):
        async def process_request(self, app_spec: AppSpecification, project_state: ProjectState) -> AgentOutput:
            logger.info("MyNewAgent: process_request called, can delegate to a specific task.")
            # Example: Delegate to 'my_specific_task_1' if certain conditions are met
            # task_input = MyTaskInput(item_id=123, instruction="Process this item based on app_spec")
            # return await self.execute_task("my_specific_task_1", task_input, project_state)
            return AgentOutput(status="pending", message="MyNewAgent ready for specific task.")

        async def execute_task(self, task_name: str, task_details: Union[MyTaskInput, Dict[str, Any]], project_state: ProjectState) -> AgentOutput:
            logger.info(f"MyNewAgent: Executing task '{task_name}'")
            
            parsed_task_details: MyTaskInput # Or a Union if multiple tasks with different inputs
            
            if task_name == "my_specific_task_1":
                try:
                    if isinstance(task_details, dict):
                        parsed_task_details = MyTaskInput(**task_details)
                    elif isinstance(task_details, MyTaskInput):
                        parsed_task_details = task_details
                    else:
                        return AgentOutput(status="failure", message="Invalid task_details type for my_specific_task_1")
                except Exception as e:
                    logger.error(f"Error parsing task_details for my_specific_task_1: {e}")
                    return AgentOutput(status="failure", message=f"Invalid input for my_specific_task_1: {e}")

                # --- Your agent's logic for 'my_specific_task_1' here ---
                logger.info(f"Processing item: {parsed_task_details.item_id} with instruction: {parsed_task_details.instruction}")
                # ... actual processing ...
                
                output_content = MyTaskOutput(
                    item_id=parsed_task_details.item_id,
                    result="Successfully processed item.",
                    is_complete=True
                )
                return AgentOutput(
                    status="success", 
                    message=f"Task {task_name} executed by MyNewAgent for item {parsed_task_details.item_id}",
                    output_data=output_content.dict() # Return Pydantic model as dict
                )
            else:
                return AgentOutput(status="failure", message=f"Unknown task: {task_name}")

        def get_capabilities(self) -> Dict[str, TaskDefinition]:
            return {
                "my_specific_task_1": TaskDefinition(
                    task_name="my_specific_task_1",
                    description="Processes a specific item based on an ID and instruction.",
                    input_spec=TaskInputSpec(
                        description="Requires an item ID and a processing instruction.",
                        schema=MyTaskInput # Reference the Pydantic model for input
                    ),
                    output_spec=TaskOutputSpec(
                        description="Returns the processing result and completion status.",
                        schema=MyTaskOutput # Reference the Pydantic model for output
                    )
                )
                # Add other tasks here if MyNewAgent can perform more.
            }
    ```

3.  **Implement Agent Logic in `execute_task`:**
    *   Use the `task_name` to switch between different task logics.
    *   **Crucially, parse and validate `task_details`**. If `task_details` is passed as a dictionary (e.g., from JSON), convert it to your defined Pydantic input model (e.g., `MyTaskInput(**task_details)`). This provides data validation.
    *   Perform the task.
    *   Return an `AgentOutput` where the `output_data` field is a dictionary representation of your Pydantic output model (e.g., `my_task_output_instance.dict()`).

4.  **Register the Agent (Conceptual):**
    *   Add your new agent to `agents/__init__.py` to make it easily importable:
        ```python
        # In agents/__init__.py
        from .my_new_agent import MyNewAgent
        # ... other agents
        ```
    *   Add its configuration to `config/agent_config.yaml` (if the orchestrator uses it for discovery). This step depends on the orchestrator's design.

## Agent Protocol Benefits

The new agent protocol, centered around `TaskDefinition` and Pydantic model schemas, offers several advantages:

*   **Clear Contracts:** Agents explicitly define their tasks and the expected data structures for inputs and outputs. This makes it easier to understand what an agent does and how to use it.
*   **Interoperability:** Standardized task definitions and data formats improve how agents can work together. An orchestrator can reliably pass data from one agent's output to another agent's input if their schemas are compatible.
*   **Discoverability:** The `get_capabilities` method allows an orchestrator (or other tools) to dynamically discover what tasks an agent can perform and the specific data requirements for each task.
*   **Automatic Validation:** By using Pydantic models for `task_details` (input) and `output_data` (output), data is automatically validated against the defined schemas. This helps catch errors early and ensures data integrity.
*   **Improved Tooling:** Structured task definitions can be leveraged to automatically generate documentation, user interfaces for interacting with agents, or even client libraries.
*   **Maintainability:** Clearer interfaces and data structures make the agents easier to maintain and update.

## Orchestrator Interaction with the New Protocol

The new agent protocol significantly enhances how an orchestrator can manage and interact with agents. Here's a conceptual overview:

1.  **Task Discovery & Cataloging:**
    *   The orchestrator can iterate through all registered/available agents.
    *   For each agent, it calls `get_capabilities()` to retrieve the dictionary of `TaskDefinition`s.
    *   This allows the orchestrator to build a comprehensive catalog of all tasks available across the entire agent pool, understanding what each task does, what input it expects (`input_spec.schema`), and what output it produces (`output_spec.schema`).

2.  **Intelligent Task Assignment & Input Validation:**
    *   When a specific task needs to be performed (e.g., "generate_code_from_plan"), the orchestrator can find an agent that lists this task in its capabilities.
    *   Before calling `agent.execute_task(task_name="generate_code_from_plan", task_details=some_data, ...)`, the orchestrator can retrieve the `TaskDefinition` for "generate_code_from_plan".
    *   It can then use the `input_spec.schema` (which is a Pydantic model) from this definition to validate `some_data`. This ensures that `task_details` will conform to the agent's expected input structure, potentially even parsing and transforming `some_data` into the correct Pydantic model instance. This preempts runtime errors within the agent due to mismatched data.

3.  **Structured Output Handling & Validation:**
    *   Upon receiving an `AgentOutput` from `execute_task`, the orchestrator can again use the `TaskDefinition` for the executed task.
    *   The `output_spec.schema` (another Pydantic model) from the `TaskDefinition` tells the orchestrator the expected structure of `AgentOutput.output_data`.
    *   The orchestrator can use this schema to validate the received `output_data`, ensuring it matches the agent's declared output format. This helps in debugging and ensures data consistency.

4.  **Reliable Agent Chaining & Workflow Automation:**
    *   With explicit input and output schemas for each task, the orchestrator can more reliably chain sequences of agent tasks.
    *   For example, if `AgentA`'s "task1" has an `output_spec.schema` of `ModelX`, and `AgentB`'s "task2" has an `input_spec.schema` of `ModelX`, the orchestrator can confidently pass the output of `AgentA.task1` as the input to `AgentB.task2`.
    *   This allows for more dynamic and robust workflow construction, as the orchestrator can programmatically determine compatible tasks and manage the data flow between them. It can even facilitate data transformation if schemas are not directly compatible but can be mapped.

This structured approach moves towards a more predictable and manageable multi-agent system, where the orchestrator acts as an intelligent coordinator, leveraging the self-described capabilities of each agent.

## Example Agents

*   **`PlannerAgent`:** Validates the initial `AppSpecification` and prepares data for code generation. Its `validate_app_specification` task uses `AppSpecification` as input and `ValidatedSpecData` as output.
*   **`CodeGenAgent`:** Generates or refactors code. Its `generate_code_from_plan` task takes `GenerateCodeInput` (which includes `ValidatedSpecData`) and produces `GeneratedCodeOutput`.
*   **`TestAgent`:** Generates and runs tests. Its `generate_tests` task takes `GenerateTestsInput` and produces `GeneratedTestsOutput`, while `run_tests` takes `RunTestsInput` and produces `TestRunOutput`.

These examples (see their respective files in `agents/`) demonstrate the implementation of the new protocol and provide a practical starting point for developing more sophisticated agents.
