from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
import os

async def main():
    # Create server parameters
    server_params = StdioServerParameters(
        command="/opt/homebrew/bin/python3.11",
        args=["mcp_minimal.py"],
        env={"PYTHONPATH": os.getenv("PYTHONPATH", "")}
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print("\nAvailable tools:")
            for tool in tools:
                print(f"- {tool.name}: {tool.description}")

            # Get a task
            task_id = input("\nEnter task ID (without 'T' prefix): ")
            result = await session.call_tool("get-task", {"task_id": task_id})
            print("\nTask details:")
            print(result[0].text)

if __name__ == "__main__":
    asyncio.run(main())
