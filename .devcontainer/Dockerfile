FROM mcr.microsoft.com/devcontainers/python:3.11

# Optional: install any OS packages you need here
RUN apt-get update \
    && apt-get -y install --no-install-recommends \
       curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Ensure pip is up to date
RUN pip install --no-cache-dir --upgrade pip

# Default workdir (the repo will be mounted here by the devcontainer)
WORKDIR /workspaces/ai-tools

