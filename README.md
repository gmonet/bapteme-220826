# Baptême civil d'Hélène & Agathe — site des invités

Page unique, statique, publiée sur GitHub Pages : le programme des 21, 22 et
23 août 2026 et les infos pratiques. Pas de build, pas de framework, aucune
dépendance ni police externe. On ouvre `index.html` dans un navigateur et ça
marche, y compris hors ligne une fois la page chargée.

```
index.html                 la page (contenu)
style.css                  palette claire/sombre, mise en page mobile first, impression
script.js                  surligne l'onglet de nav de la section visible (facultatif)
img/*.webp                 les 12 motifs aquarelle détourés
theme.png                  la planche d'origine, source des motifs
outils/decoupe_motifs.py   redécoupe img/ depuis theme.png (Pillow requis)
.nojekyll                  publie les fichiers tels quels
```

Poids : 28 Ko de HTML/CSS/JS, 113 Ko d'images (chargées en différé sauf la
planète de l'en-tête).

## Le thème

Univers du *Petit Prince*, découpé depuis `theme.png` : la planète aux deux
volcans en en-tête (deux volcans, deux filles), le réverbère pour le vendredi,
le renard pour le samedi, l'avion pour le dimanche, le puits pour les infos
pratiques, et un motif par carte. Palette papier crème / ocre / terre cuite /
feuillage, titres en serif, texte en sans-serif système.

En mode sombre, l'en-tête devient un ciel étoilé (les étoiles sont en CSS, pas
en image). Trois motifs — le mouton, le puits et la rose sous cloche — sont
peints avec la couleur du papier ; ils reçoivent un halo crème (`.motif--paper`)
pour rester lisibles sur fond sombre.

Pour retoucher les découpes (marge, taille, seuil de détourage) :

```bash
python3 outils/decoupe_motifs.py
```

**Droits sur les illustrations** : `theme.png` vient de toi, je ne connais pas
sa licence. Le dépôt étant public, vérifie qu'elle autorise la republication si
l'image provient d'une banque d'images.

## Les trois trous à compléter

Ils portent tous le même commentaire dans `index.html` :

```bash
grep -n "À COMPLÉTER" index.html
```

1. **Lien de la carte Pizzayoloo** (samedi 19h15) — remplacer `href="#"` et
   retirer la classe `todo`.
2. **Numéro de téléphone** (carte « Nous joindre ») — remplacer `href="tel:"`
   par `href="tel:+336XXXXXXXX"`, remplacer le texte affiché, retirer `todo`.
3. **Carte « Sur place »** (draps et serviettes, parking, tenue) — déjà écrite
   mais masquée : compléter les trois lignes puis supprimer l'attribut `hidden`.

## Publier / mettre à jour

Le dépôt et GitHub Pages sont déjà en place. Pour publier une modification :

```bash
git add .
git commit -m "Ajout du numéro de téléphone"
git push
```

Le site se redéploie tout seul en une à deux minutes (onglet **Actions** du
dépôt pour suivre, ou `gh run watch`). Si un invité voit encore l'ancienne
version, un rafraîchissement forcé suffit.

Si tu dois refaire l'installation depuis zéro :

```bash
git init -b main
git add . && git commit -m "Site du baptême"
gh repo create bapteme-220826 --public --source=. --remote=origin --push
gh api -X POST repos/gmonet/bapteme-220826/pages -f 'source[branch]=main' -f 'source[path]=/'
```

L'URL s'affiche dans **Settings → Pages** (« Your site is live at… ») et dans
l'encart **About** de la page d'accueil du dépôt.

## Bon à savoir sur la visibilité

Le dépôt est public : les prénoms, l'adresse du gîte et les dates sont visibles
par qui connaît l'URL — tu l'as accepté. La page porte quand même
`<meta name="robots" content="noindex, nofollow">`, qui demande aux moteurs de
ne pas l'indexer ; supprime cette ligne dans `index.html` si tu préfères
qu'elle ressorte dans les recherches.

Pour rendre le dépôt privé plus tard : Settings → General → *Danger Zone* →
*Change repository visibility*. Attention, **Pages sur dépôt privé demande un
compte payant** (GitHub Pro) ; sur un compte gratuit, le site publié
s'éteindrait.

## Vérifier avant d'envoyer le lien

- [ ] Les trois `À COMPLÉTER` sont traités (ou assumés tels quels).
- [ ] Les liens Maps ouvrent la bonne adresse depuis un téléphone.
- [ ] Le lien `tel:` déclenche l'appel.
- [ ] `Ctrl+P` : le programme tient sur une page.

Aperçu local :

```bash
python3 -m http.server 8000   # puis http://localhost:8000
```
