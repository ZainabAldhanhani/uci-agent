from langgraph.graph import StateGraph, END
from state import CaseState
from perception_agent import perception_agent
from environmental_agent import environmental_agent
from compliance_agent import compliance_agent
from reporting_agent import generate_report
from permits import PERMITS

# --- Build the graph: perception -> environmental -> compliance -> END ---
graph = StateGraph(CaseState)
graph.add_node("perception", perception_agent)
graph.add_node("environmental", environmental_agent)
graph.add_node("compliance", compliance_agent)

graph.set_entry_point("perception")
graph.add_edge("perception", "environmental")
graph.add_edge("environmental", "compliance")
graph.add_edge("compliance", END)

app = graph.compile()

# --- Run the graph once per case ---
cases = [
    "test_2_0000_0000",
    "test_55_0256_0000",
    "test_102_0512_0000",
    "test_77_0512_0256",
    "test_2_0000_0512",
    "test_121_0768_0256",
]
all_results = []

for pair_id in cases:
    print(f"Running pipeline for {pair_id}...")
    initial_state = {
        "pair_id": pair_id,
        "before_path": f"STANet/samples/A/{pair_id}.png",
        "after_path": f"STANet/samples/B/{pair_id}.png",
        "permit_record": PERMITS[pair_id],
    }
    result = app.invoke(initial_state)
    all_results.append(result)
    print(f"  -> {result['final_decision']} ({result['confidence']}%)")

# --- Once all 3 cases are done, generate the report ---
generate_report(all_results)
