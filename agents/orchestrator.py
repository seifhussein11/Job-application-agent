

from langgraph.graph import StateGraph, END
from agents.state import ApplicationState
from agents import research_agent
from agents.state import initial_state
from agents import tailoring_agent
from agents import scoring_agent
from agents import judge_agent

def should_continue(state: ApplicationState):
    
    if state.get("status") == "failed":
        return "end"
    
    if not state.get("tailored_cv"):
        return "tailor"
    
    if not state.get("tailored_match_score"):
        return "score"
    
    if not state.get("approved"):
        return "judge"
    
    return "end"
    
    



def build_graph() -> StateGraph:
    
    graph = StateGraph(ApplicationState)
    
    
    graph.add_node("research", research_agent.run)
    
    graph.add_node("tailor", tailoring_agent.run)
    
    graph.add_node("score", scoring_agent.run)
    
    graph.add_node("judge", judge_agent.run)
    
    graph.set_entry_point("research")
    
    graph.add_conditional_edges("research", should_continue, {"end": END, "tailor" : "tailor"},)
    
    graph.add_conditional_edges("tailor", should_continue,{"score":"score", "end": END})
    
    graph.add_conditional_edges("score", should_continue,{"judge":"judge", "end": END})
    
    
    graph.add_conditional_edges("judge", should_continue,{"tailor":"tailor", "end": END} )
    
    return graph.compile()


def run_pipeline(job_description : str, raw_cv: str):
    
    graph = build_graph()
    
    initial = initial_state(job_description, raw_cv)
    
    print("pipeline starting\n")
    
    final_state = graph.invoke(initial)
    
    print("pipeline complete\n")
    
    return final_state