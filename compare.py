from PIL import Image, ImageDraw

pair_id = "test_102_0512_0000"
img_size = 256
pad = 20
title_h = 40

labels = ["Before", "After", "Ground Truth", "Model Output"]
folders = ["A", "B", "label", "output"]

imgs = []
for folder in folders:
    path = f"STANet/samples/{folder}/{pair_id}.png"
    im = Image.open(path).convert("RGB").resize((img_size, img_size))
    imgs.append(im)

canvas_w = img_size * 4 + pad * 5
canvas_h = img_size + title_h + pad * 2
canvas = Image.new("RGB", (canvas_w, canvas_h), "white")
draw = ImageDraw.Draw(canvas)

x = pad
for im, label in zip(imgs, labels):
    canvas.paste(im, (x, title_h + pad))
    draw.text((x, 12), label, fill="black")
    x += img_size + pad

out_name = f"comparison_{pair_id}.png"
canvas.save(out_name)
print(f"Saved {out_name}")
