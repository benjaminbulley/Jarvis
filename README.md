# Autonomous App Suite Template

This project is a template for building an "Autonomous App Suite" – a system where autonomous agents can create various software applications (feature apps) based on user specifications.

## Overview

The suite is designed around a core orchestrator that manages a team of specialized agents (e.g., Planner, CodeGen, TestAgent). Users provide an "App Specification," and the agents collaborate to generate, test, and potentially deploy the desired application.

## Core Concepts

*   **App Specification (`suite_core/app_spec.py`):** Defines the user's request for a new application. See `example_app_spec.yaml` for an example.
*   **Agents (`agents/`):** Specialized Python classes inheriting from `BaseAgent`. Each agent performs specific tasks (e.g., planning, code generation, testing). See `agents/README.md`.
*   **Orchestrator (`suite_core/orchestrator.py`):** Manages the overall workflow, passing tasks between agents based on the project state and agent capabilities.
*   **App Blueprints/Templates (`templates/`):** Reusable starting points or structures for common application types. See `templates/README.md`.
*   **Project State (`suite_core/project_state.py`):** A data structure that tracks the progress and artifacts of an app generation request.
*   **Configuration (`config/agent_config.yaml`):** Configuration for agents and the suite itself.

## Getting Started

1.  **Prerequisites:** Python 3.8+
2.  **Installation:**
    ```bash
    # It's recommended to use a virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```
3.  **Run the Demo:**
    This template includes a basic demonstration that processes an example app specification (`example_app_spec.yaml`):
    ```bash
    python run.py
    ```
    This will simulate the workflow using the boilerplate agents and an example script template.

## Project Structure

```
autonomous-app-suite/
├── apps/                # Generated feature apps (e.g., my_generated_greeting_app/)
├── agents/              # Agent definitions (base_agent.py, planner_agent.py, etc.)
├── suite_core/          # Core logic (orchestrator.py, app_spec.py, etc.)
├── templates/           # App blueprints (simple_script_template/, etc.)
├── config/              # Configuration (agent_config.yaml)
├── example_app_spec.yaml # Example input for creating an app
├── requirements.txt     # Project dependencies
├── run.py               # Main entry point for the demo
└── README.md            # This file
```

## Extending the Template

*   **Adding New Agents:** See `agents/README.md`.
*   **Creating New App Templates:** See `templates/README.md`.
*   **Developing the Orchestrator:** Enhance `suite_core/orchestrator.py` to dynamically load and sequence agents based on `agent_config.yaml` and `ProjectState`.
*   **Building a UI:** Replace or enhance `suite_core/ui_interface.py` and `run.py` with a more interactive UI (e.g., web interface, advanced CLI).

## Advanced Concepts (Future Development)

*   **Agent Collaboration:** Implement more sophisticated communication and task hand-off between agents. This could involve a shared blackboard system or direct messaging.
*   **Tool Usage:** Equip agents with tools (e.g., file system access, shell command execution, API callers) for more complex tasks.
*   **App Deployment:** Develop `DeployAgent`s capable of deploying generated applications to various platforms (e.g., Docker, serverless functions, web servers).
*   **Testing and Validation:** Enhance `TestAgent` to generate comprehensive tests and integrate with linters/static analysis tools.

This template provides the foundational structure. Building a fully autonomous app suite is a significant endeavor.
