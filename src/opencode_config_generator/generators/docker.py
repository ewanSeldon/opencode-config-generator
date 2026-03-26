"""Generator for Dockerfile and docker-compose."""

from pathlib import Path
from ..types import ProjectConfig, Language


class DockerGenerator:
    """Generates Docker files."""
    
    def generate(self, config: ProjectConfig) -> dict[str, str]:
        """Generate Docker files."""
        
        files = {}
        
        files["Dockerfile"] = self._generate_dockerfile(config)
        
        if config.language in (Language.TYPESCRIPT, Language.JAVASCRIPT):
            files[".dockerignore"] = self._generate_dockerignore_js()
        elif config.language == Language.PYTHON:
            files[".dockerignore"] = self._generate_dockerignore_py()
        
        return files
    
    def _generate_dockerfile(self, config: ProjectConfig) -> str:
        """Generate Dockerfile based on language."""
        
        if config.language == Language.PYTHON:
            return self._generate_python_dockerfile(config)
        elif config.language in (Language.TYPESCRIPT, Language.JAVASCRIPT):
            return self._generate_js_dockerfile(config)
        elif config.language == Language.GO:
            return self._generate_go_dockerfile(config)
        elif config.language == Language.RUST:
            return self._generate_rust_dockerfile(config)
        else:
            return "# Unsupported language"
    
    def _generate_python_dockerfile(self, config: ProjectConfig) -> str:
        """Generate Dockerfile for Python."""
        
        return f"""FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    git \\
    && rm -rf /var/lib/apt/lists/*

# Install uv for faster package management
RUN pip install uv

# Copy requirements
COPY pyproject.toml ./

# Install dependencies
RUN uv pip install --system -e .

# Copy source code
COPY src/ ./src/

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Default command
CMD ["python", "-m", "opencode_config_generator", "--help"]
"""
    
    def _generate_js_dockerfile(self, config: ProjectConfig) -> str:
        """Generate Dockerfile for JavaScript/TypeScript."""
        
        base_image = "node:20-alpine"
        
        return f"""FROM {base_image}

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy source code
COPY src/ ./src/

# Set environment variables
ENV NODE_ENV=development

# Default command
CMD ["npm", "run", "start"]
"""
    
    def _generate_go_dockerfile(self, config: ProjectConfig) -> str:
        """Generate Dockerfile for Go."""
        
        return """FROM golang:1.21-alpine AS builder

WORKDIR /app

# Install dependencies
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Build
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

# Final image
FROM alpine:3.18

WORKDIR /app
COPY --from=builder /app/main .

CMD ["./main"]
"""
    
    def _generate_rust_dockerfile(self, config: ProjectConfig) -> str:
        """Generate Dockerfile for Rust."""
        
        return """FROM rust:1.75-alpine AS builder

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache musl-dev

# Copy source
COPY . .

# Build
RUN cargo build --release

# Final image
FROM alpine:3.18

WORKDIR /app
COPY --from=builder /app/target/release/appname ./app

CMD ["./app"]
"""
    
    def _generate_dockerignore_js(self) -> str:
        """Generate .dockerignore for JavaScript."""
        
        return """node_modules
npm-debug.log
dist
build
.env
.env.local
.vscode
.git
.gitignore
README.md
*.md
"""
    
    def _generate_dockerignore_py(self) -> str:
        """Generate .dockerignore for Python."""
        
        return """__pycache__
*.py[cod]
*$py.class
.venv
venv
.env
.vscode
.git
.gitignore
README.md
*.md
.pytest_cache
.coverage
htmlcov
"""
