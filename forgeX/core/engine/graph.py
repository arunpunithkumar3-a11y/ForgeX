from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import tools_condition

from forgeX.core.engine.nodes import coder, planner, scanner, tool_node
from forgeX.core.engine.state import AgentState

graph = StateGraph(AgentState)
graph.add_node("scanner", scanner)
graph.add_node("planner", planner)
graph.add_node("coder", coder)
graph.add_node("tool_node", tool_node)


graph.add_edge(START, "scanner")
graph.add_edge("scanner", "planner")
graph.add_edge("planner", "coder")
graph.add_conditional_edges(
    "coder", tools_condition, {"tools": "tool_node", "__end__": END}
)
graph.add_edge("tool_node", "coder")
builder = graph.compile()
