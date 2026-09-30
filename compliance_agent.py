from anthropic import Anthropic
from state import CaseState

client = Anthropic()

CONFIDENCE_THRESHOLD = 70  # below this, always force FLAG_FOR_REVIEW regardless of the label

def compliance_agent(state: CaseState) -> CaseState:
    permit = state["permit_record"]

    prompt = f"""You are a municipal compliance agent. You are given a description of a detected change on a parcel of land, and the permit record on file.

Detected change: {state['change_description']}
Change severity: {state['change_severity']}

Permit record:
- Parcel ID: {permit.get('parcel_id')}
- Permit type: {permit.get('permit_type')}
- Permit status: {permit.get('permit_status')}
- Issue date: {permit.get('issue_date')}
- Approved use: {permit.get('approved_use')}

Decide ONE action using these rules:
- AUTO_CLEAR: the change matches an approved permit covering this type of construction.
- FLAG_FOR_REVIEW: a permit application is on file (even if pending), or the change is minor. Not urgent.
- ESCALATE: no permit on file at all, or the change is large-scale/high-severity unauthorized construction. Urgent.

Also give a confidence score from 0-100 for how certain you are in this decision.

Respond in this exact format:
DECISION: <one of the three>
CONFIDENCE: <0-100>
REASON: <one sentence>
"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.content[0].text
    decision, confidence, reason = "", 0, ""
    for line in text.splitlines():
        if line.startswith("DECISION:"):
            decision = line.replace("DECISION:", "").strip()
        if line.startswith("CONFIDENCE:"):
            confidence = int("".join(filter(str.isdigit, line)))
        if line.startswith("REASON:"):
            reason = line.replace("REASON:", "").strip()

    state["raw_decision"] = decision
    state["confidence"] = confidence
    state["decision_reason"] = reason

    # deterministic safety rule — no LLM call needed for this part
    if confidence < CONFIDENCE_THRESHOLD:
        state["final_decision"] = "FLAG_FOR_REVIEW"
    else:
        state["final_decision"] = decision

    return state
