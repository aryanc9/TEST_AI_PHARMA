from langgraph.graph import StateGraph, END
from backend.app.graph.state import PharmacyState

from backend.app.agents.memory_agent import memory_agent
from backend.app.agents.conversation_agent import conversation_agent
from backend.app.agents.safety_agent import safety_agent
from backend.app.agents.action_agent import action_agent
from backend.app.agents.predictive_refill_agent import predictive_refill_agent


def build_pharmacy_graph():
    graph = StateGraph(PharmacyState)

    # ✅ Each node explicitly declares what it writes
    print("STATE TYPES:", {k: type(v) for k, v in state.items()})

    graph.add_node(
        "memory_agent",
        memory_agent,
        outputs=["meta", "decision_trace"]
    )
    
    graph.add_node(
        "conversation_agent",
        conversation_agent,
        outputs=["extraction", "reasoning", "decision_trace"]
    )

    graph.add_node(
        "safety_agent",
        safety_agent,
        outputs=["safety", "decision_trace"]
    )

    graph.add_node(
        "action_agent",
        action_agent,
        outputs=["execution", "decision_trace"]
    )

    graph.add_node(
        "predictive_refill_agent",
        predictive_refill_agent,
        outputs=["meta", "decision_trace"]
    )

    # Flow
    graph.set_entry_point("memory_agent")
    graph.add_edge("memory_agent", "conversation_agent")
    graph.add_edge("conversation_agent", "safety_agent")
    graph.add_edge("safety_agent", "action_agent")
    graph.add_edge("action_agent", "predictive_refill_agent")
    graph.add_edge("predictive_refill_agent", END)

    return graph.compile()
