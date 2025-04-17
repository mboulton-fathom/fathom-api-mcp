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

## Docker

To build the Docker image:

```bash
docker build -t fathom-api-mcp .
```

To run the Docker image:

```bash
docker run --rm --name fathom-api-mcp -e FATHOM_CLIENT_ID=your_client_id -e FATHOM_CLIENT_SECRET=your_client_secret fathom-api-mcp
```

Note: Replace `your_client_id` and `your_client_secret` with your actual Fathom client ID and secret.
