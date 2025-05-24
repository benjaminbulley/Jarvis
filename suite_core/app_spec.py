from typing import Optional, List
from pydantic import BaseModel

class AppSpecification(BaseModel):
    request_id: str
    user_prompt: str
    app_type: str
    target_languages_frameworks: Optional[List[str]] = None
    desired_features: Optional[List[str]] = None
    template_to_use: Optional[str] = None
    output_path: str
