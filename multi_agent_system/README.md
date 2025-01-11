# Multi-Agent System for Development Pipelines

## Overview

This system is designed to automate minor impact tasks in development pipelines using a multi-agent approach. Each agent in the system is responsible for a specific task, and they communicate with each other to complete the pipeline.

## Agents

- **HumanTaskAgent**: Responsible for defining success criteria.
- **DeveloperAgent**: Generates code based on success criteria.
- **PlanAndSolveAgent**: Plans and solves tasks based on the developer's output.
- Additional agents can be added as needed.

## Communication

Agents communicate by sending and receiving messages. This allows them to coordinate tasks and pass information along the pipeline.

## Development Choices

- **Modular Design**: Each agent is implemented as a separate class, allowing for easy extension and modification.
- **Simple Messaging Protocol**: A basic messaging system is used for communication between agents, which can be extended for more complex interactions.
- **Integration with Existing Tools**: The system can be integrated with existing development tools and APIs to perform tasks like code generation and testing.

## Future Work

- Implement additional agents for tasks like testing and documentation.
- Enhance the messaging protocol for more complex interactions.
- Integrate with external APIs for automated code generation and testing.
