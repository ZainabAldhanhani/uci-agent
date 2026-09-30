from anthropic import Anthropic
from utils import encode_image
from state import CaseState

client = Anthropic()

def environmental_agent(state: CaseState) -> CaseState:
    before_b64 = encode_image(state["before_path"])
    after_b64 = encode_image(state["after_path"])

    prompt = """You are an environmental analyst reviewing two satellite images of the same parcel: "before" and "after."

Give a brief, qualitative assessment of environmental impact — specifically:
- Was vegetation/tree cover visibly lost?
- Was natural/undeveloped land converted to hardened surface (buildings, roads, pavement)?

Also rate the environmental impact severity as one of: low, moderate, high

Keep the notes to 1-2 sentences. Be honest that this is a rough visual estimate, not a precise measurement.

Respond in this exact format:
ENVIRONMENTAL_NOTES: <1-2 sentence assessment>
ENVIRONMENTAL_SEVERITY: <low, moderate, or high>
"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": "BEFORE image:"},
                {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": before_b64}},
                {"type": "text", "text": "AFTER image:"},
                {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": after_b64}},
                {"type": "text", "text": prompt},
            ]
        }]
    )

    text = response.content[0].text
    notes = ""
    severity = ""
    for line in text.splitlines():
        if line.startswith("ENVIRONMENTAL_NOTES:"):
            notes = line.replace("ENVIRONMENTAL_NOTES:", "").strip()
        if line.startswith("ENVIRONMENTAL_SEVERITY:"):
            severity = line.replace("ENVIRONMENTAL_SEVERITY:", "").strip().lower()

    state["environmental_notes"] = notes
    state["environmental_severity"] = severity
    return state

