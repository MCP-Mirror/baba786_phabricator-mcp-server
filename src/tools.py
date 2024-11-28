from typing import Dict, Any, List
from pydantic import BaseModel

class GetTaskInput(BaseModel):
    task_id: str

class CreateTaskInput(BaseModel):
    title: str
    description: str
    project_ids: List[str] = []

class UpdateTaskInput(BaseModel):
    task_id: str
    title: str = None
    description: str = None
    status: str = None

PHABRICATOR_TOOLS = [
    {
        "name": "get-task",
        "description": "Get details of a Phabricator task",
        "inputSchema": GetTaskInput.model_json_schema(),
        "required": ["task_id"]
    },
    {
        "name": "create-task",
        "description": "Create a new Phabricator task",
        "inputSchema": CreateTaskInput.model_json_schema(),
        "required": ["title", "description"]
    },
    {
        "name": "update-task",
        "description": "Update an existing Phabricator task",
        "inputSchema": UpdateTaskInput.model_json_schema(),
        "required": ["task_id"]
    }
]