import sys, numpy as np
from PIL import Image
w_path, b_path, out_path, height = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
W = np.asarray(Image.open(w_path).convert('RGB'), dtype=np.float64)
B = np.asarray(Image.open(b_path).convert('RGB'), dtype=np.float64)
bw = W[5, 5].copy(); bb = B[5, 5].copy()          # los dos fondos lisos
span = (bw - bb)                                    # 238 por canal
alpha = 1 - ((W - B) / span).mean(axis=2)
alpha = np.clip(alpha, 0, 1)
a3 = alpha[..., None]
F = np.where(a3 > 1e-4, (B - (1 - a3) * bb) / np.maximum(a3, 1e-4), 0)
F = np.clip(F, 0, 255)
rgba = np.dstack([F, alpha * 255]).astype(np.uint8)
im = Image.fromarray(rgba, 'RGBA')
# recorte al teléfono con su sombra
ys, xs = np.where(alpha > 0.004)
box = (max(xs.min() - 8, 0), max(ys.min() - 8, 0), min(xs.max() + 8, im.width), min(ys.max() + 8, im.height))
im = im.crop(box)
im = im.resize((round(im.width * height / im.height), height), Image.LANCZOS)
im.save(out_path, 'WEBP', quality=86, method=6, alpha_quality=90)
print(out_path, im.size, 'caja', box)
