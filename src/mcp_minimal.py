from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types
from phabricator import Phabricator
import os
from typing import List

def load_env():
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

class MinimalMCPServer:
    def __init__(self):
        self.server = Server("minimal-phab-mcp")
        self.phab = Phabricator(
            host='https://phabricator.wikimedia.org/api/',
            token=os.getenv('PHABRICATOR_TOKEN')
        )
        self.phab.update_interfaces()
        self.setup_handlers()
    
    def setup_handlers(self):
        @self.server.list_tools()
        async def handle_list_tools() -> List[types.Tool]:
            return [
                types.Tool(
                    name="get-task",
                    description="Get details of a Phabricator task",
                    inputSchema=types.ObjectSchema(
                        type="object",
                        properties={
                            "task_id": types.StringSchema(
                                type="string",
                                description="Task ID (without 'T' prefix)"
                            )
                        },
                        required=["task_id"]
                    )
                )
            ]

        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict) -> List[types.TextContent]:
            try:
                if name == "get-task":
                    # Get task details
                    task = self.phab.maniphest.search(
                        constraints={'ids': [int(arguments["task_id"])]}
                    ).data[0]
                    
                    # Format response
                    response = f"""Task T{task['id']}: {task['fields']['name']}
Status: {task['fields']['status']['name']}
Priority: {task['fields']['priority']['name']}

Description:
{task['fields']['description']['raw']}"""
                    
                    return [types.TextContent(
                        type="text",
                        text=response
                    )]
                else:
                    raise ValueError(f"Unknown tool: {name}")
                    
            except Exception as e:
                return [types.TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )]

    async def run(self):
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="minimal-phab-mcp",
                    server_version="0.1.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    )
                )
            )

if __name__ == "__main__":
    load_env()
    if not os.getenv('PHABRICATOR_TOKEN'):
        print('Error: PHABRICATOR_TOKEN not set')
        exit(1)
    
    server = MinimalMCPServer()
    import asyncio
    asyncio.run(server.run())
