from abc import ABC, abstractmethod
from typing import Dict, List
from models.orchestrator import OrchestrationPlan, CommunicationStructure
from models.agent_execution_step import AgentExecutionStep, AgentExecuted

class ExecutionStrategy(ABC):
    """Abstract base class for different execution strategies"""
    @abstractmethod
    def execute(self, agent_execution_plan: List[AgentExecutionStep]) -> List[AgentExecuted]:
        pass

class LayeredExecution(ExecutionStrategy):
    """Implements layered hierarchical execution where each agent depends on previous layer"""
    def execute(self, agent_execution_plan: List[AgentExecutionStep]) -> List[AgentExecuted]:
        last_answer = ""
        layer_results: Dict[int, str] = {}
        executed_agents: List[AgentExecuted] = []

        # Group agents by their layer
        for step in agent_execution_plan:
            layer = getattr(step, 'layer', 0)  # Default to layer 0 if not specified
            context = f"""
            Previous layer results: {layer_results}
            Last answer: {last_answer}
            """
            result = step.agent.run(context)
            layer_results[layer] = result.content
            last_answer = result.content

            executed_agents.append(AgentExecuted(agent=step.agent.agent_name, action_description=step.action_description, result=result.content))

            print(f"Layer {layer} - Agent: {step.agent.agent_name}")
            print(f"Action: {step.action_description}")
            print(f"Result: {result.content}\n")

        return executed_agents

class DecentralizedExecution(ExecutionStrategy):
    """Implements peer-to-peer execution where agents communicate directly"""
    def execute(self, agent_execution_plan: List[AgentExecutionStep]) -> List[AgentExecuted]:
        last_answer = ""
        agent_messages: Dict[str, List[str]] = {}
        executed_agents: List[AgentExecuted] = []

        for step in agent_execution_plan:
            # Collect relevant messages from other agents
            peer_messages = [
                msg for agent, msgs in agent_messages.items()
                if agent != step.agent.agent_name
                for msg in msgs
            ]

            context = f"""
            Peer messages: {peer_messages}
            Last answer: {last_answer}
            """
            result = step.agent.run(context)

            # Store this agent's message
            if step.agent.agent_name not in agent_messages:
                agent_messages[step.agent.agent_name] = []
            agent_messages[step.agent.agent_name].append(result.content)

            last_answer = result.content
            executed_agents.append(AgentExecuted(agent=step.agent.agent_name, action_description=step.action_description, result=result.content))

            print(f"Agent: {step.agent.agent_name}")
            print(f"Action: {step.action_description}")
            print(f"Result: {result.content}\n")

        return executed_agents

class CentralizedExecution(ExecutionStrategy):
    """Implements hub-and-spoke execution with a central coordinator"""
    def execute(self, agent_execution_plan: List[AgentExecutionStep]) -> List[AgentExecuted]:
        last_answer = ""
        central_agent = next(
            (step.agent for step in agent_execution_plan if step.agent.is_central_authority),
            None
        )

        if not central_agent:
            raise ValueError("Centralized execution requires a central authority agent")

        executed_agents: List[AgentExecuted] = []

        for step in agent_execution_plan:
            if step.agent.is_central_authority:
                context = f"Coordinating execution. Last answer: {last_answer}"
            else:
                context = f"""
                Central authority instruction: {last_answer}
                Agent role: {step.action_description}
                """

            result = step.agent.run(context)
            last_answer = result.content

            executed_agents.append(AgentExecuted(agent=step.agent.agent_name, action_description=step.action_description, result=result.content))

            print(f"Agent: {step.agent.agent_name}")
            print(f"Action: {step.action_description}")
            print(f"Result: {result.content}\n")

        return executed_agents

class SharedPoolExecution(ExecutionStrategy):
    """Implements shared message pool where all agents can read/write messages"""
    def execute(self, agent_execution_plan: List[AgentExecutionStep]) -> List[AgentExecuted]:
        last_answer = ""
        message_pool: List[Dict] = []
        executed_agents: List[AgentExecuted] = []

        for step in agent_execution_plan:
            context = f"""
            Message pool: {message_pool}
            Last answer: {last_answer}
            Your role: {step.action_description}
            """

            result = step.agent.run(context)

            # Add message to pool with metadata
            message_pool.append({
                'agent': step.agent.agent_name,
                'action': step.action_description,
                'message': result.content,
                'timestamp': len(message_pool)  # Simple timestamp using message order
            })

            last_answer = result.content
            executed_agents.append(AgentExecuted(agent=step.agent.agent_name, action_description=step.action_description, result=result.content))

            print(f"Agent: {step.agent.agent_name}")
            print(f"Action: {step.action_description}")
            print(f"Result: {result.content}\n")

        return executed_agents

class AgentCompiler:
    """Manages agent execution according to different communication structures"""
    def __init__(self, orchestration_plan: OrchestrationPlan):
        self.orchestration_plan = orchestration_plan
        self._strategy_map = {
            CommunicationStructure.LAYERED: LayeredExecution(),
            CommunicationStructure.DECENTRALIZED: DecentralizedExecution(),
            CommunicationStructure.CENTRALIZED: CentralizedExecution(),
            CommunicationStructure.SHARED_MESSAGE_POOL: SharedPoolExecution()
        }

    def execute_agents(self) -> List[AgentExecuted]:
        """Execute agents according to the specified communication structure"""
        strategy = self._strategy_map.get(self.orchestration_plan.communication_structure)
        if not strategy:
            return self.orchestration_plan

        return strategy.execute(self.orchestration_plan.agent_execution_plan)
