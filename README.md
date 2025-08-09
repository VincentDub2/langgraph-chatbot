# LangGraph Chatbot (CLI)

## Setup

1. Create virtualenv and install dependencies:



2. Configure environment variables:



## Run



Type  to exit.

## Files
- `app.py`: CLI chat loop using the compiled LangGraph.
- `graph.py`: Defines the LangGraph state and model node.
- `prompt_manager.py`: Load versioned Markdown prompts from the `prompts/` directory.
- `pyproject.toml`: Python dependencies.
- `uv.lock`: Lockfile for dependencies.
- `tools/`: Additional tool functions used by the graph.
- `prompts/`: Example prompt files (e.g. `chatbot_v1.md`).
