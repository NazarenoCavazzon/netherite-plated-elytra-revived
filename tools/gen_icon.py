#!/usr/bin/env python3
"""Genera iconos (1024x1024) para la ficha del mod a partir de la textura del elytra."""
import os, random
from PIL import Image, ImageDraw, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ART = os.path.join(ROOT, "art")
TEX = os.path.join(ROOT, "src", "main", "resources", "assets", "netheriteelytra",
                   "textures", "item", "netherite_plated_elytra.png")

S = 1024
GOLD = (200, 161, 75)
GOLD_L = (237, 196, 114)
GOLD_D = (122, 92, 38)


def radial(size, center_color, edge_color):
    g = Image.radial_gradient("L").resize((size, size), Image.BICUBIC)
    return ImageOps.colorize(g, black=center_color, white=edge_color).convert("RGBA")


def noise_layer(size, amount=3000, color=(255, 255, 255), alpha=(4, 16)):
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    px = layer.load()
    rnd = random.Random(7)
    for _ in range(amount):
        px[rnd.randrange(size), rnd.randrange(size)] = (*color, rnd.randrange(*alpha))
    return layer


def elytra_scaled(scale):
    im = Image.open(TEX).convert("RGBA")
    return im.resize((im.width * scale, im.height * scale), Image.NEAREST)


def with_gold_outline(item, grow=4):
    """Devuelve (item, outline) con un borde dorado alrededor del pixel art."""
    a = item.split()[3]
    big = a.filter(ImageFilter.MaxFilter(grow * 2 + 1))
    outline = Image.new("RGBA", item.size, (0, 0, 0, 0))
    outline.putalpha(big)
    # sacar el relleno interior
    inner = a.filter(ImageFilter.MaxFilter(1))  # 1 queda igual
    outline = Image.composite(Image.new("RGBA", item.size, (0, 0, 0, 0)), outline, inner)
    gold = Image.new("RGBA", item.size, (*GOLD, 255))
    gold.putalpha(outline.split()[3])
    return gold


def centered(canvas, img, cy=None, cx=None):
    x = (canvas.width - img.width) // 2 if cx is None else cx
    y = (canvas.height - img.height) // 2 if cy is None else cy
    canvas.alpha_composite(img, (x, y))
    return x, y


def variant_a():
    bg = radial(S, "#3b3440", "#0a0a0c")
    bg.alpha_composite(noise_layer(S))
    glow = Image.radial_gradient("L").resize((S, S), Image.BICUBIC)
    glow = ImageOps.invert(glow).point(lambda v: int(v * 0.35))
    g = Image.new("RGBA", (S, S), (*GOLD, 255)); g.putalpha(glow)
    bg.alpha_composite(g)
    item = elytra_scaled(40)
    outline = with_gold_outline(item, 4)
    cx = (S - item.width) // 2
    cy = (S - item.height) // 2
    # sombra
    sh = Image.new("RGBA", item.size, (0, 0, 0, 0)); sh.putalpha(item.split()[3])
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    bg.alpha_composite(sh, (cx + 14, cy + 22))
    bg.alpha_composite(outline, (cx, cy))
    bg.alpha_composite(item, (cx, cy))
    border(bg, 14)
    return bg


def variant_b():
    bg = radial(S, "#2a2530", "#101013")
    # gradiente diagonal
    diag = Image.new("L", (S, S)); d = diag.load()
    for y in range(S):
        for x in range(S):
            d[x, y] = int(60 + (x + y) * 100 / (2 * S))
    tint = Image.new("RGBA", (S, S), (70, 60, 90, 0)); tint.putalpha(diag.point(lambda v: v // 6))
    bg.alpha_composite(tint)
    bg.alpha_composite(noise_layer(S, 4000))
    item = elytra_scaled(46)
    outline = with_gold_outline(item, 5)
    cx = (S - item.width) // 2; cy = (S - item.height) // 2
    sh = Image.new("RGBA", item.size, (0, 0, 0, 0)); sh.putalpha(item.split()[3])
    sh = sh.filter(ImageFilter.GaussianBlur(22))
    bg.alpha_composite(sh, (cx + 10, cy + 20))
    bg.alpha_composite(outline, (cx, cy))
    bg.alpha_composite(item, (cx, cy))
    return bg


def variant_c():
    bg = radial(S, "#33303a", "#0b0b0d")
    bg.alpha_composite(noise_layer(S, 2500))
    # badge redondeado
    pad = 90
    badge = Image.new("RGBA", (S - 2 * pad, S - 2 * pad), (24, 22, 28, 255))
    bd = ImageDraw.Draw(badge)
    bd.rounded_rectangle([0, 0, badge.width - 1, badge.height - 1], radius=90,
                         fill=(26, 24, 30, 255), outline=GOLD, width=8)
    bg.alpha_composite(badge, (pad, pad))
    glow = Image.radial_gradient("L").resize((S, S), Image.BICUBIC)
    glow = ImageOps.invert(glow).point(lambda v: int(v * 0.30))
    g = Image.new("RGBA", (S, S), (*GOLD, 255)); g.putalpha(glow)
    bg.alpha_composite(g)
    item = elytra_scaled(40)
    outline = with_gold_outline(item, 4)
    cx = (S - item.width) // 2; cy = (S - item.height) // 2
    bg.alpha_composite(outline, (cx, cy))
    bg.alpha_composite(item, (cx, cy))
    return bg


def border(canvas, w, color=GOLD):
    d = ImageDraw.Draw(canvas)
    d.rectangle([0, 0, canvas.width - 1, canvas.height - 1], outline=color, width=w)



def vanilla_tex(name):
    import zipfile, io
    jar = os.path.expanduser("~/.gradle/caches/fabric-loom/26.2/minecraft-client.jar")
    with zipfile.ZipFile(jar) as z:
        with z.open("assets/minecraft/textures/item/" + name) as f:
            return Image.open(f).convert("RGBA")


def variant_d():
    """Elytra netherita + lingote de netherita (concepto 'upgrade')."""
    bg = radial(S, "#38313e", "#0a0a0c")
    bg.alpha_composite(noise_layer(S, 3500))
    glow = Image.radial_gradient("L").resize((S, S), Image.BICUBIC)
    glow = ImageOps.invert(glow).point(lambda v: int(v * 0.32))
    g = Image.new("RGBA", (S, S), (*GOLD, 255)); g.putalpha(glow)
    bg.alpha_composite(g)

    item = elytra_scaled(38)
    outline = with_gold_outline(item, 4)
    ingot = vanilla_tex("netherite_ingot.png")
    ingot = ingot.resize((ingot.width * 20, ingot.height * 20), Image.NEAREST)
    ingot_out = with_gold_outline(ingot, 4)

    ex = (S - item.width) // 2 - 55
    ey = (S - item.height) // 2 - 65
    ix = S - ingot.width - 78
    iy = S - ingot.height - 78

    sh = Image.new("RGBA", item.size, (0, 0, 0, 0)); sh.putalpha(item.split()[3])
    sh = sh.filter(ImageFilter.GaussianBlur(20))
    bg.alpha_composite(sh, (ex + 12, ey + 18))
    bg.alpha_composite(outline, (ex, ey))
    bg.alpha_composite(item, (ex, ey))

    sh2 = Image.new("RGBA", ingot.size, (0, 0, 0, 0)); sh2.putalpha(ingot.split()[3])
    sh2 = sh2.filter(ImageFilter.GaussianBlur(12))
    bg.alpha_composite(sh2, (ix + 8, iy + 12))
    bg.alpha_composite(ingot_out, (ix, iy))
    bg.alpha_composite(ingot, (ix, iy))
    border(bg, 14)
    return bg


def diagonal_mask(size, cx, cy, slope=0.0):
    m = Image.new("L", size, 0)
    px = m.load()
    for y in range(size[1]):
        edge = cx + (y - cy) * slope
        for x in range(size[0]):
            px[x, y] = 255 if x < edge else 0
    return m


def variant_e():
    """Antes/despues: ala izquierda vanilla, ala derecha netherita."""
    bg = radial(S, "#332e3a", "#0a0a0c")
    bg.alpha_composite(noise_layer(S, 3000))
    glow = Image.radial_gradient("L").resize((S, S), Image.BICUBIC)
    glow = ImageOps.invert(glow).point(lambda v: int(v * 0.28))
    g = Image.new("RGBA", (S, S), (*GOLD, 255)); g.putalpha(glow)
    bg.alpha_composite(g)

    scale = 44
    nether = elytra_scaled(scale)
    van = vanilla_tex("elytra.png").resize((16 * scale, 16 * scale), Image.NEAREST)
    w = nether.width
    cx = w * 8 // 16 + 10
    cy = nether.height // 2
    mask = diagonal_mask(nether.size, cx, cy, slope=0.0)
    split = Image.composite(van, nether, mask)  # izquierda vanilla, derecha netherita

    outline = with_gold_outline(split, 4)
    # costura dorada en el corte
    seam = Image.new("RGBA", split.size, (0, 0, 0, 0))
    ImageDraw.Draw(seam).rectangle([cx - 3, 0, cx + 3, split.height], fill=(*GOLD, 235))
    seam.putalpha(Image.composite(seam.split()[3], Image.new("L", split.size, 0), split.split()[3]))
    x = (S - w) // 2
    y = (S - split.height) // 2
    sh = Image.new("RGBA", split.size, (0, 0, 0, 0)); sh.putalpha(split.split()[3])
    sh = sh.filter(ImageFilter.GaussianBlur(20))
    bg.alpha_composite(sh, (x + 12, y + 20))
    bg.alpha_composite(outline, (x, y))
    bg.alpha_composite(split, (x, y))
    bg.alpha_composite(seam, (x, y))
    border(bg, 14)
    return bg


def main():
    os.makedirs(ART, exist_ok=True)
    for name, fn in [("icon_a", variant_a), ("icon_b", variant_b), ("icon_c", variant_c), ("icon_d", variant_d), ("icon_e", variant_e)]:
        img = fn()
        img.convert("RGB").save(os.path.join(ART, f"{name}_1024.png"))
        img.convert("RGB").resize((256, 256), Image.LANCZOS).save(os.path.join(ART, f"{name}_256.png"))
        print("OK", name)


if __name__ == "__main__":
    main()
