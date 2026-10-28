# Contributing to SeeNOW

We welcome contributions to SeeNOW! Please read these guidelines before submitting code.

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/rhaffle87/seenow.git
   cd seenow
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install production and development dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. Run tests and static checks:
   ```bash
   pytest
   ruff check .
   mypy core gui main.py
   bandit -r core gui main.py -ll
   ```

## Pull Request Guidelines

- Ensure your code follows PEP 8 style via `ruff`.
- All tests must pass before submitting a PR.
- Add unit tests in `tests/` for any new logic or bugfixes.
- Never commit active API keys or credentials.
