# Multi-Agent System for Development Pipelines

## Overview

This system is designed to automate minor impact tasks in development pipelines using a multi-agent approach. Each agent in the system is responsible for a specific task, and they communicate with each other to complete the pipeline.

## Agents

- **HumanTaskAgent**: Responsible for defining success criteria.
- **DeveloperAgent**: Generates code based on success criteria.
- **PlanAndSolveAgent**: Plans and solves tasks based on the developer's output.
- Additional agents can be added as needed.

## Pipeline

The pipeline is defined as a series of tasks that each agent performs in sequence. The tasks are passed through the agents according to the specified graph connections.

## Development Choices

- **Langchain Integration**: Each agent is implemented using Langchain, allowing for flexible and scalable task management.
- **Graph-Based Pipeline**: The pipeline is defined using a graph structure, enabling complex task flows and dependencies.
- **Extensible Design**: Additional agents and tasks can be easily added to the system to extend its functionality.

## Future Work

- Enhance the pipeline with more complex task flows and dependencies.
- Integrate with external APIs for automated code generation, testing, and documentation.
- Implement advanced error handling and recovery mechanisms.
