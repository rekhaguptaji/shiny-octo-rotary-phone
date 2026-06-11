# Contributing to DistributedTaskScheduler

We welcome contributions! This document provides guidelines for contributing.

## Development Setup

```bash
git clone https://github.com/rekhaguptaji/shiny-octo-rotary-phone.git
cd shiny-octo-rotary-phone
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Running Tests

```bash
pytest tests/ -v --cov=scheduler
```

## Code Style

- Follow PEP 8
- Use Black for formatting: `black scheduler/`
- Use Flake8 for linting: `flake8 scheduler/`
- Use MyPy for type checking: `mypy scheduler/`

## Submitting Changes

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes and commit: `git commit -am 'Add feature'`
3. Push to branch: `git push origin feature/your-feature`
4. Submit a pull request

## Reporting Issues

Use GitHub Issues with:
- Clear title
- Detailed description
- Steps to reproduce
- Expected vs actual behavior

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.
