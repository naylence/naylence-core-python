# Naylence Fame Core

**Fame Core** is the low-level messaging backbone for the [Naylence](https://github.com/naylence) platform, providing the essential types, protocols, and interfaces for high-performance, addressable, and semantically routable message passing between AI agents and services.

> Part of the Naylence stack. See the full platform [here](https://github.com/naylence).

## Development & Publishing

This project uses Poetry for dependency management and GitHub Actions for automated testing and publishing.

### Local Development

```bash
# Install dependencies
poetry install

# Run tests
poetry run pytest

# Run linting
poetry run ruff check .
poetry run black --check .

# Build package
poetry build
```

### Publishing

- **Automatic**: Create a GitHub release to automatically publish to PyPI
- **Manual**: Use the "Publish to PyPI" workflow dispatch to publish to TestPyPI or PyPI
- **Local**: Use `poetry publish -r testpypi` or `poetry publish` for local testing
