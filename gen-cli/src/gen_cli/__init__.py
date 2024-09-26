"""
gen_cli

A command-line interface for interacting with the GenSphere platform.

This package provides tools to build, deploy, and manage Docker images
for GenSphere pods.

Modules:
    main: Contains the main CLI entry point.
    build: Handles building and pushing Docker images.
    deploy: Manages local deployment of containers.
    list: Provides commands to list repositories and tags.
    setup: Handles initial setup of the CLI.
    utils: Contains utility functions used across the CLI.

The CLI supports the following main commands:
    setup: Configure the registry address.
    build: Build and push a Docker image.
    list-repositories: List all repositories in the registry.
    list-tags: List tags for a specific repository.
    deploy: Deploy a container locally.
"""

from .main import cli

__all__ = ['cli']
