FROM python:3.12-slim-bookworm

WORKDIR /app

# Install uv
RUN pip install uv

# Copy only the pyproject.toml to leverage caching
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen

# Copy the rest of the application code
COPY hello.py ./

# Expose the port if necessary (if your MCP server listens on a specific port)
# EXPOSE 8000

# Set the entrypoint to run the MCP server
ENTRYPOINT ["uvx", "mcpo", "--port", "8000", "--", "uv", "run", "hello.py", "--transport", "stdio"]
