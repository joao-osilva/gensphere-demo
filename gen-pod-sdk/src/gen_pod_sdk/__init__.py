"""
gen_pod_sdk

A SDK to wrap an AI agent project into a GenSphere pod app.

This package provides tools to easily convert CrewAI projects into
GenSphere compatible pods with FastAPI endpoints.

Modules:
    pod_generator: Contains the main function to generate and run the pod app.
    crewai_wrapper: Provides the CrewAIPodWrapper class for handling CrewAI projects.

Functions:
    generate_pod_app: The main function to generate and run the pod app.
"""

from .pod_generator import generate_pod_app

__all__ = ['generate_pod_app']
