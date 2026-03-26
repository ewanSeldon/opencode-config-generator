"""Stack detection for automatic project detection."""

import os
from pathlib import Path
from typing import Optional


class StackDetector:
    """Detects project stack from files and directories."""

    def __init__(self, directory: str = "."):
        self.directory = Path(directory)
        self.detected = {}

    def detect(self) -> dict:
        """Run all detection methods."""
        self.detected["language"] = self._detect_language()
        self.detected["framework"] = self._detect_framework()
        self.detected["package_manager"] = self._detect_package_manager()
        self.detected["testing"] = self._detect_testing()
        self.detected["formatter"] = self._detect_formatter()
        self.detected["linter"] = self._detect_linter()
        self.detected["project_type"] = self._detect_project_type()

        # Remove None values
        return {k: v for k, v in self.detected.items() if v is not None}

    def _detect_language(self) -> Optional[str]:
        """Detect programming language."""
        
        # Check file extensions
        extensions = {
            ".ts": "TypeScript",
            ".tsx": "TypeScript",
            ".js": "JavaScript",
            ".jsx": "JavaScript",
            ".py": "Python",
            ".go": "Go",
            ".rs": "Rust",
            ".java": "Java",
            ".php": "PHP",
            ".rb": "Ruby",
            ".swift": "Swift",
            ".kt": "Kotlin",
            ".cs": "C#",
        }

        files_by_ext = {}
        for ext, lang in extensions.items():
            files_by_ext[ext] = lang

        # Count files by extension
        ext_counts = {}
        for root, _, files in os.walk(self.directory):
            # Skip common non-source directories
            skip_dirs = {".git", "node_modules", "__pycache__", ".venv", "dist", "build", ".next"}
            if any(skip in root for skip in skip_dirs):
                continue
                
            for file in files:
                ext = Path(file).suffix
                if ext in ext_counts:
                    ext_counts[ext] = ext_counts.get(ext, 0) + 1

        # Find most common language
        if ext_counts:
            most_common = max(ext_counts.items(), key=lambda x: x[1])
            return files_by_ext.get(most_common[0])

        return None

    def _detect_framework(self) -> Optional[str]:
        """Detect framework."""
        
        # Check for specific files
        framework_indicators = {
            "next.config": "Next.js",
            "nuxt.config": "Nuxt.js",
            "svelte.config": "Svelte",
            "vite.config": "Vite",
            "webpack.config": "Webpack",
            "angular.json": "Angular",
            "nest-cli.json": "NestJS",
            "fastapi": "FastAPI",
            "manage.py": "Django",
            "app.py": "Flask",
            "main.go": "Go",
            "Cargo.toml": "Rust",
            "pom.xml": "Maven (Java)",
            "build.gradle": "Gradle",
            "composer.json": "Laravel/PHP",
            "Gemfile": "Ruby on Rails",
        }

        for root, _, files in os.walk(self.directory):
            if ".git" in root or "node_modules" in root:
                continue
                
            for file in files:
                if file in framework_indicators:
                    return framework_indicators[file]

        # Check package.json for React/Vue
        pkg_json = self.directory / "package.json"
        if pkg_json.exists():
            try:
                import json
                with open(pkg_json) as f:
                    data = json.load(f)
                    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                    
                    if "next" in deps:
                        return "Next.js"
                    elif "nuxt" in deps:
                        return "Nuxt.js"
                    elif "react" in deps:
                        return "React"
                    elif "vue" in deps:
                        return "Vue.js"
                    elif "@nestjs/core" in deps:
                        return "NestJS"
                    elif "express" in deps:
                        return "Express"
                    elif "svelte" in deps:
                        return "Svelte"
            except:
                pass

        return None

    def _detect_package_manager(self) -> Optional[str]:
        """Detect package manager."""
        
        indicators = {
            "pnpm-lock.yaml": "pnpm",
            "yarn.lock": "yarn",
            "package-lock.json": "npm",
            "poetry.lock": "Poetry",
            "Pipfile.lock": "pipenv",
            "go.mod": "Go modules",
            "Cargo.lock": "Cargo",
            "Gemfile.lock": "Bundler",
            "composer.lock": "Composer",
        }

        for indicator in indicators:
            if (self.directory / indicator).exists():
                return indicators[indicator]

        return None

    def _detect_testing(self) -> Optional[str]:
        """Detect testing framework."""
        
        # Check package.json or pyproject.toml
        files_to_check = [
            "package.json",
            "pyproject.toml",
            "Cargo.toml",
        ]

        for file in files_to_check:
            path = self.directory / file
            if path.exists():
                try:
                    if file == "package.json":
                        import json
                        with open(path) as f:
                            data = json.load(f)
                            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                            
                            if "jest" in deps:
                                return "Jest"
                            elif "vitest" in deps:
                                return "Vitest"
                            elif "mocha" in deps:
                                return "Mocha"
                            elif "playwright" in deps:
                                return "Playwright"
                            elif "cypress" in deps:
                                return "Cypress"
                            
                    elif file == "pyproject.toml":
                        with open(path) as f:
                            content = f.read()
                            if "pytest" in content:
                                return "pytest"
                            elif "unittest" in content:
                                return "unittest"
                                
                    elif file == "Cargo.toml":
                        with open(path) as f:
                            content = f.read()
                            if "#[test]" in content or "[[test]]" in content:
                                return "Rust tests"
                except:
                    pass

        return None

    def _detect_formatter(self) -> Optional[str]:
        """Detect code formatter."""
        
        # Check for config files
        formatters = {
            "pyproject.toml": "Black + isort",
            ".prettierrc": "Prettier",
            ".prettierrc.json": "Prettier",
            "prettier.config.js": "Prettier",
            ".rustfmt.toml": "rustfmt",
            "go fmt": "gofmt",
        }

        for root, _, files in os.walk(self.directory):
            if ".git" in root:
                continue
            for file in files:
                if file in formatters:
                    return formatters[file]

        return None

    def _detect_linter(self) -> Optional[str]:
        """Detect linter."""
        
        files_to_check = [
            "package.json",
            "pyproject.toml",
            ".eslintrc",
            ".eslintrc.js",
            ".eslintrc.json",
            "tsconfig.json",
        ]

        for file in files_to_check:
            path = self.directory / file
            if path.exists():
                try:
                    if file == "package.json":
                        import json
                        with open(path) as f:
                            data = json.load(f)
                            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                            
                            if "eslint" in deps:
                                return "ESLint"
                            elif "tslint" in deps:
                                return "TSLint"
                                
                    elif file == "pyproject.toml":
                        with open(path) as f:
                            content = f.read()
                            if "ruff" in content:
                                return "Ruff"
                            elif "flake8" in content:
                                return "Flake8"
                            elif "mypy" in content:
                                return "MyPy"
                                
                except:
                    pass

        return None

    def _detect_project_type(self) -> Optional[str]:
        """Detect project type."""
        
        # Check for indicators
        indicators = {
            "api": ["routes", "endpoints", "views.py", "controllers"],
            "web": ["pages", "components", "public", "templates"],
            "cli": ["bin", "cli", "main.py"],
            "library": ["src", "package.json"],
            "monorepo": ["packages", "apps", "workspaces"],
        }

        for root, dirs, files in os.walk(self.directory):
            if ".git" in root:
                continue
                
            for ptype, ind in indicators.items():
                if any(i in root.split(os.sep) or i in files for i in ind):
                    return ptype

        return None
