import base64

def encode_image(path):
    with open(path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")

