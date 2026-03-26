"""Generator for release automation."""

from pathlib import Path
from ..types import ProjectConfig, Language


class ReleaseGenerator:
    """Generates release automation workflows."""
    
    def generate(self, config: ProjectConfig) -> dict[str, str]:
        """Generate release files."""
        
        files = {}
        
        # Release workflow
        files[".github/workflows/release.yml"] = self._generate_release_workflow(config)
        
        # conventional-commits config
        files[".release-please-config.json"] = self._generate_release_config()
        
        return files
    
    def _generate_release_workflow(self, config: ProjectConfig) -> str:
        """Generate release workflow."""
        
        if config.language == Language.PYTHON:
            build_cmd = "python -m build"
            test_cmd = "pytest"
            publish = """- name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: \${{ secrets.PYPI_TOKEN }}"""
        elif config.language in (Language.TYPESCRIPT, Language.JAVASCRIPT):
            build_cmd = "npm publish"
            test_cmd = "npm test"
            publish = """- name: Publish to npm
        run: npm publish
        env:
          NODE_AUTH_TOKEN: \${{ secrets.NPM_TOKEN }}"""
        elif config.language == Language.GO:
            build_cmd = "go build"
            test_cmd = "go test ./..."
            publish = """- name: Release
        uses: goreleaser/goreleaser-action@v4
        with:
          args: release --rm-dist
        env:
          GITHUB_TOKEN: \${{ secrets.GITHUB_TOKEN }}"""
        else:
            build_cmd = "echo 'No build step'"
            test_cmd = "echo 'No tests'"
            publish = "# No publish configured for this language"
        
        return f"""name: Release

on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      version:
        description: 'Version (e.g., 1.0.0) or leave empty for auto'
        required: false
        type: string

permissions:
  contents: write

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"

      - name: Run tests
        run: {test_cmd}

      - name: Run lint
        run: ruff check src/

  release:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && startsWith(github.ref, 'refs/heads/main')
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          token: \${{ secrets.GITHUB_TOKEN }}

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install release-please-action

      - name: Release
        uses: google-github-actions/release-please-action@v3
        with:
          token: \${{ secrets.GITHUB_TOKEN }}
          release-type: python
          target-branch: main
          draft: false
          prerelease: false

  publish:
    needs: release
    runs-on: ubuntu-latest
    if: needs.release.outputs.releases_created
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install build

      - name: Build package
        run: {build_cmd}

      - name: {publish.replace('$', '\\$').split('\\n')[0] if publish.startswith('-') else 'Publish'}
        {publish.replace('$', '\\$')}
"""
    
    def _generate_release_config(self) -> str:
        """Generate release-please configuration."""
        
        return """{
  "packages": {
    ".": {
      "release-type": "python",
      "include-component-in-tag": false,
      "include-v-in-tag": true
    }
  },
  "plugins": [
    {
      "type": "linked-versions",
      "strategy": "bumpMinorPreMajor"
    }
  ]
}
"""
    
    def generate_changelog_template(self) -> str:
        """Generate changelog template."""
        
        return """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New feature (#[issue])

### Changed
- Change to existing functionality

### Deprecated
- Soon-to-be removed feature

### Removed
- Removed feature

### Fixed
- Bug fix (#[issue])

### Security
- Security improvement

## [1.0.0] - YYYY-MM-DD

### Added
- Initial release
"""
    
    def generate_version_bump_script(self, config: ProjectConfig) -> str:
        """Generate version bump script."""
        
        if config.language == Language.PYTHON:
            return """#!/bin/bash
# Bump version for Python project

VERSION_TYPE="${1:-patch}"  # major, minor, patch

# Read current version from pyproject.toml
CURRENT_VERSION=$(grep '^version = ' pyproject.toml | sed 's/version = "\\(.*\\)"/\\1/')

echo "Current version: $CURRENT_VERSION"

# Split version
IFS='.' read -ra VERSION_PARTS <<< "$CURRENT_VERSION"
MAJOR="${VERSION_PARTS[0]}"
MINOR="${VERSION_PARTS[1]}"
PATCH="${VERSION_PARTS[2]}"

# Bump version
case "$VERSION_TYPE" in
    major)
        MAJOR=$((MAJOR + 1))
        MINOR=0
        PATCH=0
        ;;
    minor)
        MINOR=$((MINOR + 1))
        PATCH=0
        ;;
    patch)
        PATCH=$((PATCH + 1))
        ;;
esac

NEW_VERSION="$MAJOR.$MINOR.$PATCH"
echo "New version: $NEW_VERSION"

# Update pyproject.toml
sed -i "s/version = \\"[0-9.]*\\"/version = \\"$NEW_VERSION\\"/" pyproject.toml

# Create git tag
git add pyproject.toml
git commit -m "chore: bump version to $NEW_VERSION"
git tag "v$NEW_VERSION"

echo "Version bumped to $NEW_VERSION"
"""
        
        elif config.language in (Language.TYPESCRIPT, Language.JAVASCRIPT):
            return """#!/bin/bash
# Bump version for Node.js project

VERSION_TYPE="${1:-patch}"  # major, minor, patch

CURRENT_VERSION=$(node -p "require('./package.json').version")
echo "Current version: $CURRENT_VERSION"

npm version $VERSION_TYPE --no-git-tag-version

git add package.json package-lock.json
git commit -m "chore: bump version to $NEW_VERSION"
"""
        
        else:
            return "# Version bump not implemented for this language"
