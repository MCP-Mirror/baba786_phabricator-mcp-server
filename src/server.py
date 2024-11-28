from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types
from phab_client import PhabricatorClient
import os
from typing import List, Dict

class PhabricatorMCPServer:
    def __init__(self):
        self.server = Server("phabricator-wmf-mcp")
        self.phab_client = PhabricatorClient(
            token=os.environ["PHABRICATOR_TOKEN"]
        )
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

    def _format_task_details(self, task: Dict, comments: List[Dict]) -> str:
        """Format task details for display."""
        return f"""
Task T{task['id']}: {task['fields']['name']}
Status: {task['fields']['status']['name']}
Priority: {task['fields']['priority']['name']}

Description:
{task['fields']['description']['raw']}

Comments:
{self._format_comments(comments)}
        """.strip()

    def _format_comments(self, comments: List[Dict]) -> str:
        """Format task comments for display."""
        if not comments:
            return "No comments"
        return "\n\n".join([
            f"- {comment['comments']}"
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
    # Check for required environment variables
    if "PHABRICATOR_TOKEN" not in os.environ:
        raise ValueError("PHABRICATOR_TOKEN environment variable is required")
    
    server = PhabricatorMCPServer()
    import asyncio
    asyncio.run(server.run())
