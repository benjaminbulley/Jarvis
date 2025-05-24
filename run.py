import yaml
from suite_core.app_spec import AppSpecification
from suite_core.orchestrator import handle_app_request
# from suite_core.project_state import ProjectState # Optional, if more detailed state printing is needed

def main():
    print("Autonomous App Suite: Demo Run Initializing...")

    spec_file_path = "example_app_spec.yaml"
    print(f"Loading app specification from: {spec_file_path}")

    try:
        with open(spec_file_path, 'r') as f:
            raw_spec_data = yaml.safe_load(f)
        
        if raw_spec_data is None:
            print(f"Error: Specification file {spec_file_path} is empty or not valid YAML.")
            return

        app_spec = AppSpecification(**raw_spec_data)
        print(f"Successfully loaded AppSpecification: {app_spec.request_id}")

    except FileNotFoundError:
        print(f"Error: Specification file not found at {spec_file_path}")
        print("Please ensure 'example_app_spec.yaml' exists in the root directory.")
        return
    except yaml.YAMLError as e:
        print(f"Error parsing YAML from {spec_file_path}: {e}")
        return
    except Exception as e: # Catch other Pydantic validation errors or unexpected issues
        print(f"Error loading or parsing specification file: {e}")
        return

    print(f"Passing specification to orchestrator...")
    project_state = handle_app_request(app_spec)

    print(f"Orchestration complete for request: {app_spec.request_id}")
    print("Final Project State (simulated):")
    # project_state.dict() provides a dictionary representation of the Pydantic model
    # Using exclude_none=True for cleaner output as in ui_interface.py
    print(project_state.dict(indent=2, exclude_none=True)) 

if __name__ == "__main__":
    main()
