"""Generator for GitHub Actions workflows."""

import json
from pathlib import Path
from ..types import ProjectConfig, Language


class GitHubActionsGenerator:
    """Generates GitHub Actions workflows."""
    
    def generate(self, config: ProjectConfig) -> dict[str, str]:
        """Generate GitHub Actions workflows."""
        
        workflows = {}
        
        # CI workflow
        workflows[".github/workflows/ci.yml"] = self._generate_ci_workflow(config)
        
        # Test coverage workflow
        if config.language in (Language.PYTHON, Language.TYPESCRIPT, Language.JAVASCRIPT):
            workflows[".github/workflows/coverage.yml"] = self._generate_coverage_workflow(config)
        
        return workflows
    
    def _generate_ci_workflow(self, config: ProjectConfig) -> str:
        """Generate CI workflow."""
        
        python_versions = ["3.9", "3.10", "3.11", "3.12"]
        
        if config.language == Language.PYTHON:
            test_cmd = "pytest"
            install_cmd = "pip install -e ."
        elif config.language in (Language.TYPESCRIPT, Language.JAVASCRIPT):
            test_cmd = "npm test"
            install_cmd = "npm install"
        elif config.language == Language.GO:
            test_cmd = "go test ./..."
            install_cmd = "go mod download"
        elif config.language == Language.RUST:
            test_cmd = "cargo test"
            install_cmd = "cargo fetch"
        else:
            test_cmd = "echo 'No tests configured'"
            install_cmd = "echo 'No dependencies'"
        
        workflow = f"""name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: {install_cmd.replace('"', '').split()[0]} install dependencies
        run: |
          python -m pip install --upgrade pip
          {install_cmd}

      - name: Run tests
        run: {test_cmd}

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install ruff

      - name: Run ruff
        run: ruff check src/
"""
        return workflow
    
    def _generate_coverage_workflow(self, config: ProjectConfig) -> str:
        """Generate coverage workflow."""
        
        if config.language == Language.PYTHON:
            run_cmd = "pytest --cov=src --cov-report=xml"
            action = "codecov/codecov-action@v4"
        else:
            run_cmd = "npm test -- --coverage"
            action = "codecov/codecov-action@v4"
        
        workflow = f"""name: Coverage

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  coverage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -e ".[dev]"

      - name: Generate coverage
        run: {run_cmd}

      - name: Upload to Codecov
        uses: {action}
        with:
          file: ./coverage.xml
          fail_ci_if_error: false
"""
        return workflow
