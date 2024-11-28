import asyncio
from mcp.client import ClientSession, stdio_client

async def main():
    server_params = {
        "capabilities": ["list_tools", "invoke_tool"]
    }
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            try:
                # List available tools
                tools = await session.list_tools()
                print("Available tools:")
                for tool in tools:
                    print(f"- {tool['name']}: {tool['description']}")
                
                # Example: Get task details
                result = await session.invoke_tool(
                    "get-task",
                    {"task_id": "T123"}
                )
                print("\nGet task result:", result)
                
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())