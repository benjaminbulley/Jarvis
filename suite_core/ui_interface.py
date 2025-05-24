from .app_spec import AppSpecification
from .orchestrator import handle_app_request
import uuid # For generating unique request_ids if needed, or use hardcoded

def get_app_specification_from_cli() -> AppSpecification:
    """
    Returns a hardcoded AppSpecification object for demonstration purposes.
    """
    print("UI: Using hardcoded app specification for demonstration.")
    spec = AppSpecification(
        request_id=str(uuid.uuid4()), # Generate a unique ID for each run
        user_prompt="Create a simple Python script that prints 'Hello, World!' and saves it as hello.py",
        app_type="script",
        target_languages_frameworks=["python"],
        desired_features=["Prints 'Hello, World!' to console", "Saves output to a file named 'hello.py'"],
        output_path="generated_apps/hello_world_app"
    )
    return spec

def run_demo():
    """
    Runs a demonstration of the app request and orchestration process.
    """
    print("UI: Starting demo run...")
    app_spec = get_app_specification_from_cli()
    print(f"UI: App Specification created: {app_spec.request_id}")
    
    project_state = handle_app_request(app_spec)
    
    print(f"UI: Demo run complete for request {app_spec.request_id}.")
    print(f"UI: Final project state: {project_state.dict(exclude_none=True)}")

if __name__ == "__main__":
    run_demo()
