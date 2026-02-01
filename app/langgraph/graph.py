from langgraph.graph import StateGraph
from app.langgraph.state import BIState
from app.agents import metadata_agent, rag_agent, sql_agent, impact_agent, execute_agent, bi_agent

graph = StateGraph(BIState)
graph.add_node("metadata", metadata_agent.run)
graph.add_node("rag", rag_agent.run)
graph.add_node("sql", sql_agent.run)
graph.add_node("impact", impact_agent.run)
graph.add_node("execute", execute_agent.run)
graph.add_node("bi", bi_agent.run)

graph.set_entry_point("metadata")
graph.add_edge("metadata", "rag")
graph.add_edge("rag", "sql")
graph.add_edge("sql", "impact")
graph.add_edge("impact", "execute")
graph.add_edge("execute", "bi")

bi_graph = graph.compile()
