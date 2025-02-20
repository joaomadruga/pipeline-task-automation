from langgraph.graph import StateGraph, START
from langgraph.graph import MessagesState, END
from multi_agents import po_node, developer_node, describe_success_criteria_node, rag_with_docs_node, tester_unit_node, db_analyst_node, reviewer_node

workflow = StateGraph(MessagesState)
workflow.add_node("human_task", po_node)
workflow.add_node("describe_success_criteria", describe_success_criteria_node)
workflow.add_node("developer", developer_node)
workflow.add_node("rag_with_docs", rag_with_docs_node)
workflow.add_node("tester_unit", tester_unit_node)
workflow.add_node("db_analyst", db_analyst_node)
workflow.add_node("reviewer", reviewer_node)

workflow.add_edge(START, "human_task")
workflow.add_edge("human_task", "describe_success_criteria")
workflow.add_edge("describe_success_criteria", "developer")
workflow.add_edge("developer", "rag_with_docs")
workflow.add_edge("developer", "tester_unit")
workflow.add_edge("developer", "db_analyst")
workflow.add_edge("rag_with_docs", "tester_unit")
workflow.add_edge("tester_unit", "reviewer")
workflow.add_edge("reviewer", "describe_success_criteria")  # Connection for re-evaluation