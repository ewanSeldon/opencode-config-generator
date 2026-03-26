"""Generator for pre-commit hooks."""

from pathlib import Path
from ..types import ProjectConfig, Language


class PreCommitGenerator:
    """Generates pre-commit configuration."""
    
    def generate(self, config: ProjectConfig) -> dict[str, str]:
        """Generate pre-commit config files."""
        
        files = {}
        
        # Main .pre-commit-config.yaml
        files[".pre-commit-config.yaml"] = self._generate_config(config)
        
        return files
    
    def _generate_config(self, config: ProjectConfig) -> str:
        """Generate .pre-commit-config.yaml based on language."""
        
        repos = self._get_repos(config)
        
        content = """# Pre-commit hooks configuration
# Install: pip install pre-commit && pre-commit install
# Run manually: pre-commit run --all-files

repos:
"""
        
        for repo in repos:
            content += f"""  - repo: {repo['repo']}
    rev: {repo['rev']}
    hooks:
"""
            for hook in repo['hooks']:
                content += f"""      - id: {hook['id']}
"""
                if 'args' in hook:
                    content += f"""        args: [{', '.join(hook['args'])}]
"""
                if 'files' in hook:
                    content += f"""        files: {hook['files']}
"""
        
        content += """
# Skip certain files
exclude: '^\.git/|^dist/|^build/|^__pycache__/'
"""
        
        return content
    
    def _get_repos(self, config: ProjectConfig) -> list[dict]:
        """Get repositories based on language."""
        
        repos = [
            {
                "repo": "https://github.com/pre-commit/pre-commit-hooks",
                "rev": "v4.6.0",
                "hooks": [
                    {"id": "trailing-whitespace"},
                    {"id": "end-of-file-fixer"},
                    {"id": "check-yaml"},
                    {"id": "check-added-large-files", "args": ["--maxkb=1000"]},
                    {"id": "check-json"},
                    {"id": "check-toml"},
                    {"id": "check-merge-conflict"},
                ],
            },
        ]
        
        # Language-specific hooks
        if config.language == Language.PYTHON:
            repos.extend([
                {
                    "repo": "https://github.com/astral-sh/ruff-pre-commit",
                    "rev": "v0.8.0",
                    "hooks": [
                        {"id": "ruff", "args": ["--fix"]},
                        {"id": "ruff-format"},
                    ],
                },
                {
                    "repo": "https://github.com/pycqa/isort",
                    "rev": "5.13.2",
                    "hooks": [
                        {"id": "isort", "files": r"\.py$"},
                    ],
                },
            ])
        
        elif config.language in (Language.TYPESCRIPT, Language.JAVASCRIPT):
            repos.extend([
                {
                    "repo": "https://github.com/pre-commit/mirrors-prettier",
                    "rev": "v3.0.0-alpha.9-for-vscode",
                    "hooks": [
                        {"id": "prettier", "files": r"\.(js|jsx|ts|tsx|json|css|md|yaml)$"},
                    ],
                },
                {
                    "repo": "https://github.com/eslint/eslint",
                    "rev": "v9.17.0",
                    "hooks": [
                        {"id": "eslint", "args": ["--fix"], "types": ["javascript", "typescript"]},
                    ],
                },
            ])
        
        elif config.language == Language.GO:
            repos.append({
                "repo": "https://github.com/dnephin/pre-commit-golang",
                "rev": "v0.5.1",
                "hooks": [
                    {"id": "go-fmt"},
                    {"id": "go-vet"},
                ],
            })
        
        elif config.language == Language.RUST:
            repos.append({
                "repo": "https://github.com/doublify/pre-commit-rust",
                "rev": "v1.0",
                "hooks": [
                    {"id": "cargo-check"},
                    {"id": "cargo-clippy", "args": ["--fix"]},
                ],
            })
        
        return repos
    
    def generate_install_script(self, config: ProjectConfig) -> str:
        """Generate a script to install pre-commit hooks."""
        
        return """#!/bin/bash
# Install pre-commit hooks for this project

# Install pre-commit if not present
if ! command -v pre-commit &> /dev/null; then
    echo "Installing pre-commit..."
    pip install pre-commit
fi

# Install hooks
echo "Installing pre-commit hooks..."
pre-commit install

# Run on all files initially
echo "Running pre-commit on all files (first time)..."
pre-commit run --all-files

echo "Done! Pre-commit hooks are now active."
"""
