#!/usr/bin/env python3
"""Découpe les 12 motifs de theme.png en WebP détourés dans img/.

Usage : python3 outils/decoupe_motifs.py   (depuis la racine du dépôt)
Dépendance : Pillow uniquement.

Le fond crème du dessin est retiré par remplissage depuis le pourtour de
chaque vignette : les aplats crème *enclavés* (la laine du mouton, le fond du
puits, le verre de la cloche) sont volontairement conservés, sinon ces motifs
deviennent des silhouettes vides. Sur fond sombre, style.css place derrière
eux un halo de papier (classe .motif--paper).
"""
from PIL import Image, ImageChops, ImageDraw, ImageFilter

SOURCE = "theme.png"
FOND = (242, 236, 208)     # crème du papier
MARGE = 14                 # marge autour de chaque vignette avant détourage
SENTINELLE = (255, 0, 255) # couleur temporaire marquant le fond
GRAND_COTE = {"planete": 300}   # taille d'export ; 200 px par défaut

# coordonnées des 12 vignettes dans la planche (x0, y0, x1, y1)
VIGNETTES = {
    "planete":   (81, 118, 270, 387),
    "rose":      (388, 118, 559, 387),
    "renard":    (676, 118, 867, 387),
    "mouton":    (970, 118, 1214, 387),
    "baobab":    (41, 468, 306, 764),
    "boa":       (343, 468, 633, 764),
    "reverbere": (701, 468, 863, 764),
    "puits":     (946, 468, 1209, 764),
    "avion":     (38, 874, 306, 1076),
    "lune":      (407, 874, 583, 1076),
    "etoiles":   (705, 874, 881, 1076),
    "echarpe":   (959, 874, 1217, 1076),
}


def main():
    src = Image.open(SOURCE).convert("RGB")
    W, H = src.size
    for nom, (x0, y0, x1, y1) in VIGNETTES.items():
        boite = (max(0, x0 - MARGE), max(0, y0 - MARGE),
                 min(W, x1 + MARGE), min(H, y1 + MARGE))
        vignette = src.crop(boite)
        travail = vignette.copy()
        w, h = travail.size

        # amorcer le remplissage tout autour : seul le fond relié au bord part
        amorces = ([(x, 0) for x in range(0, w, 6)] + [(x, h - 1) for x in range(0, w, 6)]
                   + [(0, y) for y in range(0, h, 6)] + [(w - 1, y) for y in range(0, h, 6)])
        for point in amorces:
            if travail.getpixel(point) != SENTINELLE:
                ImageDraw.floodfill(travail, point, SENTINELLE, thresh=34)

        plein = Image.new("RGB", travail.size, SENTINELLE)
        canaux = ImageChops.difference(travail, plein).split()
        alpha = ImageChops.lighter(ImageChops.lighter(canaux[0], canaux[1]), canaux[2])
        alpha = alpha.point(lambda v: 0 if v < 12 else 255)
        alpha = alpha.filter(ImageFilter.GaussianBlur(0.6))  # bords adoucis

        sortie = vignette.convert("RGBA")
        sortie.putalpha(alpha)
        sortie = sortie.crop(sortie.getbbox())

        cible = GRAND_COTE.get(nom, 200)
        echelle = cible / max(sortie.size)
        if echelle < 1:
            sortie = sortie.resize((round(sortie.width * echelle),
                                    round(sortie.height * echelle)), Image.LANCZOS)
        sortie.save(f"img/{nom}.webp", "WEBP", quality=80, method=6)
        print(f"img/{nom}.webp {sortie.size[0]}x{sortie.size[1]}")


if __name__ == "__main__":
    main()
