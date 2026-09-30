from anthropic import Anthropic
from utils import encode_image
from state import CaseState

client = Anthropic()

def perception_agent(state: CaseState) -> CaseState:
    before_b64 = encode_image(state["before_path"])
    after_b64 = encode_image(state["after_path"])

    prompt = """You are a computer vision analyst reviewing two satellite images of the same parcel of land: "before" and "after."

Describe what physically changed between the two images, focused on construction/structures.
Then rate the severity of the change as one of: minor, moderate, major
(minor = small addition/extension, moderate = one new building, major = large-scale new development).

Respond in this exact format:
CHANGE: <one or two sentences describing what changed>
SEVERITY: <minor, moderate, or major>
"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=250,
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

    # simple parsing: pull out the two labeled lines
    change_line = ""
    severity_line = ""
    for line in text.splitlines():
        if line.startswith("CHANGE:"):
            change_line = line.replace("CHANGE:", "").strip()
        if line.startswith("SEVERITY:"):
            severity_line = line.replace("SEVERITY:", "").strip().lower()

    state["change_description"] = change_line
    state["change_severity"] = severity_line
    return state
