import os
import asyncio
from typing import List, Dict, Any
from dotenv import load_dotenv
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types
from phab_client import PhabricatorClient

# Load environment variables from .env file
load_dotenv()

class PhabricatorMCPServer:
    def __init__(self):
        self.server = Server("phabricator-wmf-mcp")
        token = os.getenv("PHABRICATOR_TOKEN")
        if not token:
            raise ValueError("PHABRICATOR_TOKEN environment variable is required")
        self.phab_client = PhabricatorClient(token=token)
        self.setup_handlers()
    
    def setup_handlers(self):
        @self.server.list_tools()
        async def handle_list_tools() -> List[types.Tool]:
            return [
                types.Tool(
                    name="get-task",
                    description="Get details of a Phabricator task",
                    arguments=[
                        types.ToolArgument(
                            name="task_id",
                            description="Task ID (without 'T' prefix)",
                            required=True
                        )
                    ]
                )
            ]

        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict) -> List[types.TextContent]:
            try:
                if name == "get-task":
                    task = await self.phab_client.get_task(arguments["task_id"])
                    comments = await self.phab_client.get_task_comments(arguments["task_id"])
                    
                    return [types.TextContent(
                        type="text",
                        text=self._format_task_details(task, comments)
                    )]
                else:
                    raise ValueError(f"Unknown tool: {name}")
                    
            except Exception as e:
                return [types.TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )]

    def _format_task_details(self, task: Dict[str, Any], comments: List[Dict[str, Any]]) -> str:
        """Format task details for display."""
        try:
            return f"""
Task T{task['id']}: {task['fields']['name']}
Status: {task['fields']['status']['name']}
Priority: {task['fields']['priority']['name']}

Description:
{task['fields']['description']['raw']}

Comments:
{self._format_comments(comments)}
            """.strip()
        except KeyError as e:
            return f"Error formatting task details: Missing field {str(e)}"

    def _format_comments(self, comments: List[Dict[str, Any]]) -> str:
        """Format task comments for display."""
        if not comments:
            return "No comments"
        return "\n\n".join([
            f"- {comment.get('comments', 'No comment content')}"
            for comment in comments
        ])

    async def run(self):
        """Run the MCP server."""
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="phabricator-wmf-mcp",
                    server_version="0.1.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    )
                )
            )

if __name__ == "__main__":
    try:
        server = PhabricatorMCPServer()
        asyncio.run(server.run())
    except Exception as e:
        print(f"Error starting server: {str(e)}")
        raise