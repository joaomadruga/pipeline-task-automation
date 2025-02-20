from langchain_openai import ChatOpenAI
import getpass
import os
from dotenv import load_dotenv

from typing import Literal

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from langgraph.graph import MessagesState, END
from langgraph.types import Command
from tools import shell_execution_tool, documentation_tool, plan_and_solve_tool, database_tool

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")


def make_system_prompt(suffix: str) -> str:
    return (
        "You are a helpful AI assistant, collaborating with other assistants."
        " Use the provided tools to progress towards answering the question."
        " If you are unable to fully answer, that's OK, another assistant with different tools "
        " will help where you left off. Execute what you can to make progress."
        " If you or any of the other assistants have the final answer or deliverable,"
        " prefix your response with FINAL ANSWER so the team knows to stop."
        f"\n{suffix}"
    )


llm = ChatOpenAI(model="gpt-4o-mini")


def get_next_node(last_message: BaseMessage, goto: str):
    if "FINAL ANSWER" in last_message.content:
        # Any agent decided the work is done
        return END
    return goto


product_owner_agent = create_react_agent(
    llm,
    tools=[plan_and_solve_tool],
    state_modifier=make_system_prompt(
        """
            You are the initial task processor. Your role is to:
            1. Understand the user's request clearly
            2. Format it in a structured way
            3. Extract key requirements and constraints
            Output format should be JSON with 'task_description', 'requirements', and 'constraints' fields.
        """
    ),
)

describe_success_criteria_agent = create_react_agent(
    llm,
    tools=[shell_execution_tool],
    state_modifier=make_system_prompt(
        """
            You are responsible for describing the success criteria. Your role is to:
            1. Understand the user's request
            2. Define clear success criteria
            3. Ensure criteria are measurable and achievable
            4. Use the plan_and_solve_tool to assist in planning and solving tasks
        """
    ),
)

developer_agent = create_react_agent(
    llm,
    tools=[shell_execution_tool, documentation_tool],
    state_modifier=make_system_prompt(
        """
        You are a developer who writes and tests code. Your role is to:
            1. Implement the solution based on requirements
            2. Follow best practices and patterns
            3. Document your code
            4. Use the shell_execution_tool for running commands
            5. Use the documentation_tool for documentation
            6. Handle edge cases
            Consider the success criteria in your implementation.
        """
    ),
)

rag_with_docs_agent = create_react_agent(
    llm,
    tools=[documentation_tool],
    state_modifier=make_system_prompt(
        """
            You are responsible for reviewing and generating documentation. Your role is to:
            1. Review the developer's work
            2. Generate necessary documentation
            3. Ensure documentation is clear and comprehensive
        """
    ),
)

tester_unit_agent = create_react_agent(
    llm,
    tools=[shell_execution_tool, documentation_tool],
    state_modifier=make_system_prompt(
        """
            You are responsible for unit testing. Your role is to:
            1. Write and execute unit tests
            2. Verify code quality and functionality
            3. Ensure all edge cases are tested
            4. Use the shell_execution_tool to run tests
            5. Use the documentation_tool for documentation
        """
    ),
)

db_analyst_agent = create_react_agent(
    llm,
    tools=[database_tool],
    state_modifier=make_system_prompt(
        """
            You are responsible for database analysis. Your role is to:
            1. Analyze database requirements
            2. Ensure database design meets the needs
            3. Optimize database performance
        """
    ),
)

reviewer_agent = create_react_agent(
    llm,
    tools=[plan_and_solve_tool],
    state_modifier=make_system_prompt(
        """
            You are responsible for reviewing the final solution. Your role is to:
            1. Review the entire solution
            2. Ensure it meets all success criteria
            3. Provide final approval or feedback
            4. If the success criteria are not met, provide structured feedback and send it back to describe_success_criteria
        """
    ),
)


def po_node(
    state: MessagesState,
) -> Command[Literal["developer", END]]:
    result = product_owner_agent.invoke(state)
    goto = get_next_node(result["messages"][-1], "developer")
    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content, name="product_owner"
    )
    return Command(
        update={
            "messages": result["messages"],
        },
        goto=goto,
    )


def developer_node(
    state: MessagesState,
) -> Command[Literal["tester_unit", END]]:
    result = developer_agent.invoke(state)
    goto = get_next_node(result["messages"][-1], "tester_unit")
    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content, name="developer"
    )
    return Command(
        update={
            "messages": result["messages"],
        },
        goto=goto,
    )


def describe_success_criteria_node(
    state: MessagesState,
) -> Command[Literal["developer", END]]:
    result = describe_success_criteria_agent.invoke(state)
    goto = get_next_node(result["messages"][-1], "developer")
    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content, name="describe_success_criteria"
    )
    return Command(
        update={
            "messages": result["messages"],
        },
        goto=goto,
    )

def rag_with_docs_node(
    state: MessagesState,
) -> Command[Literal["tester_unit", END]]:
    result = rag_with_docs_agent.invoke(state)
    goto = get_next_node(result["messages"][-1], "tester_unit")
    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content, name="rag_with_docs"
    )
    return Command(
        update={
            "messages": result["messages"],
        },
        goto=goto,
    )

def tester_unit_node(
    state: MessagesState,
) -> Command[Literal["reviewer", END]]:
    result = tester_unit_agent.invoke(state)
    goto = get_next_node(result["messages"][-1], "reviewer")
    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content, name="tester_unit"
    )
    return Command(
        update={
            "messages": result["messages"],
        },
        goto=goto,
    )

def db_analyst_node(
    state: MessagesState,
) -> Command[Literal["developer", END]]:
    result = db_analyst_agent.invoke(state)
    goto = get_next_node(result["messages"][-1], "developer")
    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content, name="db_analyst"
    )
    return Command(
        update={
            "messages": result["messages"],
        },
        goto=goto,
    )

def reviewer_node(
    state: MessagesState,
) -> Command[Literal["describe_success_criteria", END]]:
    result = reviewer_agent.invoke(state)
    if "criteria not met" in result["messages"][-1].content:
        goto = "describe_success_criteria"
    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content, name="reviewer"
    )
    return Command(
        update={
            "messages": result["messages"],
        },
        goto=goto,
    )
