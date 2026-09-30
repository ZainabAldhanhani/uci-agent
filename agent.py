import base64
from anthropic import Anthropic
from permits import PERMITS

client = Anthropic()

def encode_image(path):
    with open(path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")

def check_change(pair_id):
    permit = PERMITS[pair_id]

    before_b64 = encode_image(f"STANet/samples/A/{pair_id}.png")
    after_b64 = encode_image(f"STANet/samples/B/{pair_id}.png")

    prompt_text = f"""You are a municipal building-compliance agent. You are shown two satellite images of the same parcel of land: the first is "before," the second is "after."

Permit record on file for this parcel:
- Parcel ID: {permit['parcel_id']}
- Permit type: {permit['permit_type']}
- Permit status: {permit['permit_status']}
- Issue date: {permit['issue_date']}
- Approved use: {permit['approved_use']}

Look at the two images, describe briefly what changed, then decide ONE action using these rules:
- AUTO_CLEAR: the change matches an approved permit covering this type of construction.
- FLAG_FOR_REVIEW: a permit application is on file (even if pending), or the change is minor. Not urgent.
- ESCALATE: no permit on file at all, or large-scale/high-severity unauthorized construction. Urgent.

Respond in this exact format:
CHANGE: <one sentence describing what you see changed>
DECISION: <one of the three>
REASON: <one sentence>
"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": "BEFORE image:"},
                {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": before_b64}},
                {"type": "text", "text": "AFTER image:"},
                {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": after_b64}},
                {"type": "text", "text": prompt_text},
            ]
        }]
    )

    return response.content[0].text


if __name__ == "__main__":
    for label, pair_id in [
        ("Case 1: no permit on file", "test_2_0000_0000"),
        ("Case 2: approved permit on file", "test_55_0256_0000"),
        ("Case 3: pending permit, matching use", "test_102_0512_0000"),
    ]:
        print(f"=== {label} ===")
        print(check_change(pair_id))
        print()