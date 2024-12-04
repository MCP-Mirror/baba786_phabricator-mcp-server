# Phabricator MCP Server

A Model Context Protocol (MCP) server implementation for interacting with Phabricator API. This server allows LLMs to interact with Phabricator through a standardized interface.

## Overview

This project provides an MCP server that exposes Phabricator functionality through:
- Task management (viewing, creating, updating tasks)
- Project information
- User details

## Getting Started

### Prerequisites

- Python 3.8+
- Phabricator API token (from your Phabricator instance)
- Access to a Phabricator instance

### Installation

1. Clone this repository:
```bash
git clone https://github.com/baba786/phabricator-mcp-server.git
cd phabricator-mcp-server
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Unix/MacOS
# or
.\venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your environment:
```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your Phabricator token
# Replace 'your-token-here' with your actual Phabricator API token
echo "PHABRICATOR_TOKEN=your-token-here" > .env
```

5. Run the server:
```bash
cd src
python server.py
```

## Usage

Currently supported commands:
- `get-task`: Retrieve details of a specific Phabricator task

Example usage through the client:
```python
from src.mcp_minimal_client import Client

client = Client()
response = client.get_task(task_id="123")  # Replace with actual task ID
print(response)
```

## Development Status

🚧 This project is currently under development. Stay tuned for updates!