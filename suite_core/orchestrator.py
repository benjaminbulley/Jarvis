from .app_spec import AppSpecification
from .project_state import ProjectState
from agents.base_agent import AgentOutput # Assuming 'agents' is a top-level directory accessible via PYTHONPATH
import uuid

def handle_app_request(app_spec: AppSpecification) -> ProjectState:
    """
    Handles an application request, initializes project state, and simulates initial agent interaction.
    """
    print(f"Orchestrator: Received app request: {app_spec.request_id} for '{app_spec.user_prompt[:50]}...'")

    project_state = ProjectState(
        request_id=app_spec.request_id,
        current_status="received",
        app_spec=app_spec,
        generated_files=[],
        agent_history=[],
        error_log=[]
    )
    print("Orchestrator: Initializing project state...")

    print("Orchestrator: Passing to first agent (placeholder)...")

    # Simulate an initial agent interaction
    dummy_agent_output = AgentOutput(
        status="success",
        output_data={"plan": "Initial plan details (simulated)"},
        message="PlannerAgent: Initial plan created (simulated)",
        next_agent_hint="CodeGeneratorAgent"
    )
    
    project_state.agent_history.append({
        "agent_name": "PlannerAgent (simulated)",
        "output": dummy_agent_output.dict(),
        "timestamp": "YYYY-MM-DDTHH:MM:SSZ" # Placeholder timestamp
    })
    project_state.current_status = "planning_complete_simulated"

    print(f"Orchestrator: Processing finished for {app_spec.request_id}. Current state: {project_state.current_status}")
    return project_state
