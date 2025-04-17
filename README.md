# MCP Flood Data Server

This project is an MCP server that uses the fathom global client SDK to fetch flood data via an LLM.

## Setup

Use uv to setup the project. (`uv venv`, `uv lock`, `uv sync`, ...)

## Use

To use in [continue](https://docs.continue.dev/customize/deep-dives/mcp) (Must be running 1.1.24 or later - at the time of writing this is the pre-release version):

```
mcpServers:
  - name: Fathom API MCP server
    command: uv
    transport:
      type: stdio
    env:
     FATHOM_CLIENT_ID: my-client-id
     FATHOM_CLIENT_SECRET: my-client-secret
    args:
    - --quiet
    - --directory
    - /path/to/fathom-api-mcp/
    - run
    - hello.py
```
