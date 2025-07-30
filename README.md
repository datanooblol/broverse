# broverse
This is a lib for data pipeline, agentic workflows or any flow with less dependencies

## Development Setup

For development, install all dependencies:

```bash
uv sync --extra dev
```

For development, install the package in editable mode:

```bash
uv pip install -e .
```

This allows you to:
- Import `broverse` from anywhere in your project
- Run examples from `examples/` subdirectories
- See changes immediately without reinstalling

*Note: in development phase, pytorch is triggy if you're using windows or older operating systems, consult google/stackoverflow but don't worry broverse doesn't contain it*