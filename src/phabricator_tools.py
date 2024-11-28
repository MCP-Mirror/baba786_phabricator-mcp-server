from typing import List
from pydantic import BaseModel, Field
from mcp.tools import Tool, ToolError

class GetTaskInput(BaseModel):
    task_id: str = Field(..., description="The ID of the Phabricator task to retrieve")

class GetTaskOutput(BaseModel):
    title: str
    description: str
    status: str
    priority: str

async def get_task(input_data: GetTaskInput) -> GetTaskOutput:
    # Implementation will be added later
    raise NotImplementedError()

PHABRICATOR_TOOLS: List[Tool] = [
    Tool(
        name="get-task",
        description="Retrieve a Phabricator task by ID",
        input_schema=GetTaskInput,
        output_schema=GetTaskOutput,
        function=get_task
    )
]
