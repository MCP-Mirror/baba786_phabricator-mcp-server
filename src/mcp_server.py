import asyncio
import json
from typing import Dict, Any

from mcp.server import (
    ServerSession,
    stdio_server,
    Tool,
    Request,
    Response,
    Error
)

from tools import PHABRICATOR_TOOLS

class PhabricatorMCPServer:
    def __init__(self):
        self.tools = PHABRICATOR_TOOLS

    async def handle_request(self, request: Request) -> Response | Error:
        if request.method == "list_tools":
            return Response(result=self.tools)
        
        # Handle tool requests
        if request.method == "invoke_tool":
            tool_name = request.params.get("name")
            tool_params = request.params.get("parameters", {})
            
            # Add your Phabricator API handling logic here
            # For now, return mock responses
            if tool_name == "get-task":
                return Response(result={
                    "id": tool_params["task_id"],
                    "title": "Mock Task",
                    "description": "This is a mock task response"
                })
                
            elif tool_name == "create-task":
                return Response(result={
                    "id": "T123",
                    "title": tool_params["title"],
                    "description": tool_params["description"]
                })
                
            elif tool_name == "update-task":
                return Response(result={
                    "id": tool_params["task_id"],
                    "status": "updated"
                })
                
            return Error(code=404, message=f"Unknown tool: {tool_name}")
            
        return Error(code=404, message=f"Unknown method: {request.method}")

async def main():
    server = PhabricatorMCPServer()
    
    async def handler(request: Request) -> Response | Error:
        return await server.handle_request(request)
    
    async with stdio_server(handler) as _:
        await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())