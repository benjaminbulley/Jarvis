from typing import Optional, List, Dict
from pydantic import BaseModel

class AppTemplateManifest(BaseModel):
    template_id: str
    template_name: str
    description: str
    supported_app_types: List[str]
    supported_languages_frameworks: List[str]
    placeholder_definitions: Optional[Dict[str, str]] = None # Example: {"{{APP_NAME}}": "The name of the application"}
    entry_point_script: Optional[str] = None
