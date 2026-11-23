# Photos à fournir en meilleure définition

Passe du 12/11/2026 sur `refonte-maison`, toutes pages, ordinateur (1440 px de large) et mobile. Script : `audit/retours/nettete.mjs`.

## Constat

Aucune photo du site ne dépasse 1 100 px de large : elles ont été compressées pour le mobile. Sur mobile, tout est net. Sur ordinateur, 24 photos sont affichées plus grandes que leur fichier, et un écran Retina double encore le besoin. Les bandeaux pleine largeur sont les plus touchés : agrandis environ 3 fois.

Ce n'est pas rattrapable par une retouche : il manque des pixels. Il faut les fichiers d'origine.

## Ce qui a été fait dans le code

- Les photos ne sont plus agrandies de 14 à 18 % pour glisser dans leur cadre au défilement (photos des camps sur l'accueil, appels finaux, photo de Lucas). Gain : la photo de Recreio de l'accueil passe d'un agrandissement de 1,9 à 1,6.
- La pellicule « Le Brésil, c'est… » est en cartes larges (voir DIRECTION-MAISON.md).

## Fichiers à réexporter

Largeur à viser : **2 400 px** pour un bandeau pleine largeur, **1 600 px** pour une photo en demi-largeur, **1 000 px** pour une vignette. Format JPEG ou WebP, qualité 80.

### Bandeaux pleine largeur (priorité 1)

| Agrandissement | Fichier actuel | Taille | Où |
|---|---|---|---|
| 3,3× | bandeau d'en-tête d'« À propos » (sans nom, `4642689c…`) | 1000 × 430 | À propos, en-tête |
| 3,0× | `ph-work-m` | 960 × 640 | Travailler et surfer, en-tête ; pilier « Travailler » |
| 3,0× | `ph-ita-palms-m` | 960 × 540 | Itacaré, appel final de chaque onglet |
| 2,9× | bandeau d'en-tête de « Pour qui » (sans nom, `53722858…`) | 1100 × 473 | Pour qui, en-tête |
| 2,9× | `cta-about-1-recommande-groupe-pedra-FV038` | 1000 × 500 | À propos, appel final |
| 2,6× | photo de l'appel final de l'accueil (sans nom, `867b184a…`) | 1100 × 459 | Accueil, « Construisez votre surf trip » |
| 2,6× | `ph-rio-cta-m` | 1100 × 619 | Rio, appel final de chaque onglet ; menu « Nos surf camps » |

### Photos en demi-largeur (priorité 2)

| Agrandissement | Fichier actuel | Taille | Où |
|---|---|---|---|
| 1,8× | `ph-ita-aerial-m` | 960 × 540 | Itacaré, aperçu, « Surfer à Itacaré » |
| 1,7× | surfeuse de « Pour qui » (sans nom, `03712117…`) | 683 × 1024 | Accueil, « Pour qui » |
| 1,7× | `ph-ita-headland-m` | 960 × 540 | Accueil, carte Itacaré |
| 1,7× | `surfclub-cowork-sea-c` | 1000 × 450 | Travailler et surfer, carte Rio |
| 1,6× | `17072026-DJI_0515` | 1000 × 563 | Accueil, carte Recreio |
| 1,6× | `lucas-boards-c` | 665 × 1000 | À propos, « Pourquoi Surf Inn existe » |
| 1,6× | `ita-facade-palms-s-c` | 1100 × 611 | Itacaré, aperçu, « Un camp entouré de verdure » |
| 1,5× | `cowork-03-note5-COW006` | 800 × 533 | Travailler et surfer, carte Itacaré |
| 1,5× | `ph-rd-pontal-drone-m` | 960 × 656 | Rio, aperçu, « Entre la plage et le rythme de la ville » |

### Vignettes (priorité 3)

| Agrandissement | Fichier actuel | Taille | Où |
|---|---|---|---|
| 2,3× | `rio-lua-night` | 335 × 597 | Rio, « Recreio, le Rio des surfeurs » |
| 2,0× | `rio-small-riders` | 387 × 516 | Rio, « Recreio, le Rio des surfeurs » |
| 1,9× | `ita-double-1-c` | 630 × 1000 | Itacaré, Le camp, chambres |
| 1,8× | `tiririca_onda` | 640 × 418 | Itacaré, Le camp, bloc des planches |
| 1,7× | `DSC06417-c` | 667 × 1000 | Itacaré, Le camp, espaces communs |
| 1,7× | `ph-rd-crew-m` | 720 × 960 | Rio, Le camp |
| 1,6× | `brand/pesca` | 547 × 365 | Itacaré, Expériences |
| 1,6× | `brand/video-analysis` | 519 × 385 | Itacaré, Expériences |

L'agrandissement est mesuré pour un écran Retina de 1440 px de large. Sur un écran standard, divise par deux.

Non mesuré : les vidéos, les galeries ouvertes en grand, les photos du tunnel.
