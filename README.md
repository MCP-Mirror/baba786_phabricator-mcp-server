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
- Phabricator API token
- Access to a Phabricator instance

### Installation

1. Clone this repository:
```bash
git clone https://github.com/baba786/phabricator-mcp-server.git
cd phabricator-mcp-server
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Phabricator API token:
```bash
export PHABRICATOR_TOKEN="your-token-here"
```

## Development Status

🚧 This project is currently under development. Stay tuned for updates!