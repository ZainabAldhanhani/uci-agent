from typing import TypedDict, Optional

class CaseState(TypedDict):
    # input
    pair_id: str
    before_path: str
    after_path: str
    permit_record: dict

    # filled in by Perception Agent
    change_description: Optional[str]
    change_severity: Optional[str]   # e.g. "minor" / "moderate" / "major"

    # filled in by Environmental Impact Agent
    environmental_notes: Optional[str]
    environmental_severity: Optional[str]  # low / moderate / high

    # filled in by Compliance Agent
    raw_decision: Optional[str]      # AUTO_CLEAR / FLAG_FOR_REVIEW / ESCALATE
    confidence: Optional[int]        # 0-100
    decision_reason: Optional[str]
    final_decision: Optional[str]    # after confidence threshold rule is applied
