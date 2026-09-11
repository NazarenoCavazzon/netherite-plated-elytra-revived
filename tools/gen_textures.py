#!/usr/bin/env python3
"""Genera las texturas netherita del mod a partir de las texturas vanilla del elytra.

Se toman las texturas originales del cliente de MC 26.2 (jar cacheado por Loom) y se
recolorean con una paleta netherita (grises muy oscuros + detalles dorados), sin tocar
la forma ni la transparencia.

Uso:  python3 tools/gen_textures.py
"""
import os
import sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "src", "main", "resources", "assets", "netheriteelytra", "textures")

HOME = os.path.expanduser("~")
CANDIDATES = [
    os.path.join(HOME, ".gradle/caches/fabric-loom/26.2/minecraft-client.jar"),
    "/tmp/mcextract",
]


def find_vanilla():
    """Devuelve (getter) que abre assets/minecraft/<ruta> desde el jar o carpeta."""
    import zipfile
    jar = CANDIDATES[0]
    if os.path.isfile(jar):
        z = zipfile.ZipFile(jar)

        def load(rel):
            with z.open("assets/minecraft/" + rel) as f:
                return Image.open(f).convert("RGBA")
        return load
    folder = CANDIDATES[1]
    if os.path.isdir(folder):
        def load(rel):
            return Image.open(os.path.join(folder, "assets/minecraft", rel)).convert("RGBA")
        return load
    sys.exit("No se encontraron las texturas vanilla (jar de Loom ni /tmp/mcextract).")


def item_map(r, g, b, a):
    """Wing del item: membrana oscura con filo dorado."""
    if a == 0:
        return (0, 0, 0, 0)
    lum = (r + g + b) / 3
    purple = b - r
    if purple >= 20:                      # membrana (violeta en vanilla)
        if lum < 120:
            return (0x2C, 0x27, 0x33, a)
        if lum < 135:
            return (0x39, 0x33, 0x42, a)
        return (0x46, 0x3E, 0x50, a)
    if lum < 64:                          # marco / contorno
        return (0x14, 0x14, 0x16, a)
    if lum < 85:
        return (0x22, 0x22, 0x26, a)
    if lum < 110:
        return (0x30, 0x30, 0x37, a)
    if lum < 125:
        return (0x4A, 0x4A, 0x53, a)
    if lum < 138:                         # brillos -> oro
        return (0xB8, 0x92, 0x3F, a)
    return (0xE0, 0xBA, 0x66, a)


def wings_map(r, g, b, a):
    """Alas sobre el jugador: base oscura con punta dorada."""
    if a == 0:
        return (0, 0, 0, 0)
    lum = r * 0.3 + g * 0.59 + b * 0.11
    if lum < 85:
        return (0x1B, 0x1B, 0x1F, a)
    if lum < 100:
        return (0x2A, 0x2A, 0x30, a)
    if lum < 115:
        return (0x38, 0x38, 0x3F, a)
    if lum < 128:
        return (0x46, 0x46, 0x4F, a)
    if lum < 136:
        return (0x6B, 0x5A, 0x38, a)
    return (0xC8, 0xA1, 0x4B, a)


def recolor(img, fn):
    out = Image.new("RGBA", img.size)
    out.putdata([fn(*p) for p in list(img.getdata())])
    return out


def main():
    load = find_vanilla()

    jobs = [
        ("textures/item/elytra.png", "item/netherite_plated_elytra.png", item_map),
        ("textures/item/elytra_broken.png", "item/netherite_plated_elytra_broken.png", item_map),
        ("textures/entity/equipment/wings/elytra.png",
         "entity/equipment/wings/netherite_plated_elytra.png", wings_map),
    ]
    for src, dst, fn in jobs:
        img = load(src)
        out = recolor(img, fn)
        dest = os.path.join(OUT, dst)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        out.save(dest)
        print(f"OK {dst} ({out.width}x{out.height})")


if __name__ == "__main__":
    main()
