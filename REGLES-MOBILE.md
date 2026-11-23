# Règles de conception mobile

Branche `main-anglify-mobile-inspi`, ouverte le 14/11/2026 à partir de `main`. Règles déduites de la version mobile d'anglify.com (mesurée à 390 × 760), puis appliquées à Surf Inn. Tout est dans `outils/experience/mobile.css`, sous 720 px de large : l'ordinateur ne change pas.

## Ce qu'on observe sur anglify.com

| # | Règle | Ce qu'on voit |
|---|---|---|
| 1 | **Le texte d'abord, l'image dessous** | L'en-tête tient sur un fond uni : titre, phrase, bouton, notes. La photo n'arrive qu'en bas de l'écran. Rien n'est écrit sur une image. |
| 2 | **Une section, un écran** | Chaque section se lit sans défiler : un titre, un court texte, un visuel ou une liste. |
| 3 | **Les listes défilent sur le côté** | Les cartes (méthode, avis) sont en bande horizontale ; la carte suivante dépasse pour montrer qu'il y a une suite, avec deux flèches. |
| 4 | **Un seul bouton, toujours le même** | Une barre fixe en bas reprend l'action principale dès qu'on quitte l'en-tête. Le bouton secondaire est en contour. |
| 5 | **Un rythme régulier** | Fonds qui alternent d'une section à l'autre, marges identiques, titres de 30 à 40 px, texte de 18 à 19 px. |
| 6 | **La preuve tout de suite** | Les notes (Google, Mon Compte Formation) sont dans le premier écran, sous le bouton. |
| 7 | **Un menu discret** | Logo et menu dans une pastille flottante qui laisse voir la page. |

## Ce qui est appliqué à Surf Inn

| Règle | Avant | Maintenant |
|---|---|---|
| 1 | Titre et formulaire posés sur la vidéo | Texte et formulaire sur fond vert uni, la vidéo en bandeau dessous (accueil, Rio, Itacaré, « Pour qui », « Travailler et surfer ») |
| 2 et 3 | « Apprendre. Travailler… » : 2,7 écrans | Bande à faire glisser, 0,9 écran |
| 2 et 3 | Profils de « Pour qui » : 4,9 écrans | Bande, 1,2 écran |
| 2 et 3 | Piliers, équipe et « Notre façon de vivre » d'« À propos » : 2,7 + 1,7 + 2,7 écrans | Trois bandes, chacune sous un écran |
| 2 | Avis de l'accueil : 1,3 écran | Notes sur une ligne, cartes plus larges, 0,9 écran |
| 2 | Carte et quartier de Rio : 1,8 écran | Carte plus basse, trois blocs en bande, sous un écran |
| 2 | « Le quotidien » de Rio : 1,7 écran | Grille de trois colonnes, 0,85 écran |
| 5 | Marges de 56 à 64 px, titres de tailles variables | 40 px partout, titres de 25 à 30 px |

Les règles 4, 6 et 7 étaient déjà respectées (bouton « Créer mon séjour » fixe en bas, note Google dans l'en-tête, menu en pastille).

## Résultat mesuré

| Page | Longueur avant | Maintenant | Sections de plus d'un écran |
|---|---|---|---|
| Accueil | 13,1 écrans | 9,5 | 6 → 2 |
| Rio | 14,1 | 11,6 | 4 → 2 |
| Itacaré | — | 10,4 | 1 |
| Pour qui | 7,5 | 3,8 | 1 |
| À propos | 10,1 | 5,4 | 3 → 0 |
| Travailler et surfer | 7,5 | 6,5 | 2 → 0 |

Script de mesure : `audit/retours/sections.mjs`.

## Ce qui dépasse encore

- **En-têtes** (1,1 à 1,2 écran) : volontaire. Le texte et le formulaire tiennent dans le premier écran, la vidéo dépasse en bas pour inviter à défiler, comme la photo d'Anglify.
- **« Un surf camp pour débutant ou confirmé »** (accueil, 1,08) et **« Un surf camp face à la plage de Macumba »** (Rio, 1,09) : ce sont des listes de sept et quatre lignes. Pour passer sous un écran, il faut raccourcir le texte, pas la mise en page.
- **Profils de « Pour qui »** (1,16) : même cause, les textes sont longs.

## Non traité

Onglets Le camp, Expériences, Packages et Guide surf des pages camp ; pages FAQ, Avis et Contact ; tunnel de réservation.

## Retours de Kévin (14/11/2026)

- **Vidéos d'en-tête** : affichées à leur format d'origine, en portrait 2:3 (390 × 585 sur un iPhone), au lieu d'un bandeau de 260 px qui les coupait en hauteur. L'en-tête fait donc environ 1,6 écran : le texte et le formulaire dans le premier, la vidéo entière dans le suivant.
- **Plus d'apparition progressive** du contenu de l'en-tête sur téléphone : tout est affiché d'emblée.
- **Pages camp** : le menu des onglets est placé entre le texte de l'en-tête et la vidéo. L'en-tête est « défait » en CSS (`display:contents`) pour ordonner texte, onglets et vidéo. Conséquence : en haut de ces pages, la barre du logo est sur fond clair au lieu d'être transparente.
- **« La région » en cartes postales** (ordinateur et mobile) : papier clair, photo dans une marge blanche, petit timbre et oblitération dans le coin, nom du lieu en serif au-dessus d'une ligne pointillée.

## Remise à plat (14/11/2026, soir)

À la demande de Kévin, l'affichage mobile revient à celui de `main`, sauf les en-têtes. Tout ce qui avait été fait pour faire tenir chaque section dans un écran est retiré : photos abaissées, textes réduits ou coupés, marges resserrées, listes en bandes. Les tableaux « Ce qui est appliqué » et « Résultat mesuré » ci-dessus décrivent donc un état qui n'est plus en place.

**Ce qui reste sur cette branche**

- En-têtes : texte et formulaire sur fond uni, vidéo entière en portrait dessous, contenu affiché d'emblée.
- Pages camp : onglets entre le texte et la vidéo.
- « La région » : cartes postales (timbre) pour les paysages seulement (Surf, Plage, Nature, Vie tranquille) ; les sorties (Musique live, Fête, Nuit) prennent un air de billet d'entrée, avec deux encoches et une ligne de découpe ; Culture et Cuisine restent des cartes simples.
- La seconde phrase de l'en-tête de l'accueil (« Venez pour le surf, repartez avec le Brésil. ») est remise.

**Suite** : les sections seront ramenées à un écran une par une, avec Kévin. État de départ mesuré : accueil 13,8 écrans (7 sections sur 11 dépassent un écran), Rio 14,8 écrans (4 sur 11).
- **Bouton flottant « Créer mon séjour »** : il s'efface dès qu'un bouton d'action est à l'écran, principal ou secondaire (« Découvrir Surf Inn Rio », « Voir le camp »…), et plus seulement quand « Créer mon séjour » y est déjà. Mesuré : visible sur 61 % du défilement de l'accueil et 66 % de celui de Rio, jamais en même temps qu'un autre bouton (`audit/retours/flottant.mjs`).

## Retours de Kévin du 15/11/2026

- **Galerie « Pris sur le vif »** : trois photos retirées (l'accolade en double, la tablée de bières, le dîner au flash). Neuf photos, en 3 × 3 sur téléphone et en une rangée sur ordinateur.
- **« Le Brésil, c'est… »** : le petit titre « Partir surfer au Brésil » est retiré, le titre repasse en très grand, la ligne « Brésilien ? » remonte juste sous le titre. La tong devient une paire qui marche.
- **Avis de l'accueil (téléphone)** : la section tient sur un écran (0,79 au lieu de 1,28). Les trois notes sont sur une ligne, la carte suivante dépasse, les flèches sont visibles, le texte d'un avis est limité à neuf lignes (l'avis complet s'ouvre sur Google).
- **Fenêtres ouvertes** : la page derrière ne défile plus (cartes du concept, galeries, planches, tunnel).
- **Fenêtres du concept (téléphone)** : tout tient à l'écran sans défilement, y compris sur un petit téléphone (664 px de haut).
- **Trait sous le menu** : la bordure du menu restait visible quand le menu est transparent ; retirée.
- **Boutons principaux** : même dessin partout. Quatre rappels (« Envie de venir ? », appel final de l'accueil, « À propos », « Vous préparez un long séjour ? ») avaient le texte en vert moyen au lieu du vert très foncé.
- **« Envie de venir ? »** : bande claire (jaune pâle) entre la section sombre et les avis, titre plus grand. Elle se fondait dans le vert de la section du dessus.
- **Section du concept** : le bouton flottant ne s'y affiche plus (les cartes sont cliquables). La fermeture d'une carte ne fait plus remonter en haut de page : le blocage du défilement passe par le geste et non plus par `overflow:hidden`.
- **Fenêtres du concept** : retour à l'affichage aéré d'origine (grande photo, la fenêtre défile), à la demande de Kévin. Ligne « Cours de portugais » retirée de la carte « Apprendre ».
- **« Le Brésil, c'est… »** : le sous-texte de chaque mot n'est plus affiché (les photos le disent déjà ; il reste dans la page pour les moteurs et les lecteurs d'écran). Les deux tongs dansent un pas de passinho : pivots pointe-talon, pas croisé, petit saut, glissé, la seconde en miroir.

## En-têtes à la manière d'outsite.co et section Brésil (15/11/2026, soir)

- **En-têtes mobiles** (accueil, Rio, Itacaré, « Pour qui ») : la vidéo d'abord, sur 58 % de la hauteur de l'écran, sans texte dessus ; le titre, la phrase et le formulaire juste dessous. Sur l'accueil, la marque « SURF INN » reste posée sur le bas de la vidéo. Sur les pages camp, l'ordre est vidéo, texte, onglets. Ceci remplace l'ordre « texte puis vidéo » repris d'Anglify. La danse des tongs est ralentie (2,7 s par mesure).
- **Bouton flottant** : il ne s'affiche pas non plus tant que le formulaire ou le titre de l'en-tête est à l'écran.
- **« Le Brésil, c'est… »** : les photos viennent juste sous le titre, pour lire « Le Brésil, c'est… une eau chaude toute l'année ». Les quatre mots passent sous les photos, en pastilles de navigation (celle en cours en jaune) ; « Brésilien ? » vient après. Ordinateur et mobile.

## Premier écran mobile, deuxième version (15/11/2026, nuit)

- **Premier écran** (accueil, Rio, Itacaré) : il ne montre que la vidéo, presque entière (elle prend toute la hauteur moins 250 px sur l'accueil, moins 216 px sur les pages camp), la marque sur l'accueil, le titre, la phrase, et le bouton flottant « Créer mon séjour ». Le formulaire de l'accueil et le texte long des pages camp n'apparaissent qu'au défilement. Le menu est transparent par-dessus la vidéo. Vérifié à 760 et 664 px de haut.
- **Mots du Brésil** : de retour dans leur dessin d'origine (grands, au trait, celui en cours en jaune souligné), sous les photos. Les pastilles sont abandonnées.
- **« Envie de venir ? »** : de retour sur fond vert.
- **Avis de l'accueil** : affichés en entier (plus de coupe à neuf lignes), et les cartes ne sont plus des liens. Les pages Google restent accessibles par les pastilles de notes. La section fait 0,87 écran sur téléphone.

## Retours du 16/11/2026

- **Premier écran de l'accueil (téléphone)** : plus de vide sous la phrase. Le module « Destination · Dates · Voyageurs » est en blanc, sur une seule ligne, juste sous la phrase ; le bouton flottant « Créer mon séjour » lui sert de bouton (celui du module est masqué sur téléphone). La note Google de l'en-tête n'est plus affichée sur téléphone. La vidéo prend la hauteur de l'écran moins 326 px.
- **Module de l'en-tête (tous écrans)** : champs en blanc, flèche de « Destination » dans la couleur d'accent (elle restait bleue).
- **Galerie de l'accueil** : titre « La vie avec Surf Inn », sous-texte retiré.
- **Emplacement des pages camp (téléphone)** : « Le quartier », « Venir » et « Pourquoi cet endroit » sont repliés ; un toucher les déroule. Carte abaissée à 230 px. La section tient sur un écran.
- **Rio, « Votre séjour » (téléphone)** : les quatre puces ne sont plus affichées (à valider avec Lucas) ; la section tient sur un écran.
- **Libellés** : « Découvrir le camp → » et « Découvrir toutes les expériences → » (français).
- **Bandes à faire glisser** : elles ne bougent plus de haut en bas (8 px de jeu vertical supprimés).
- **Puces des cartes camp de l'accueil** : texte complet sur ordinateur (rétabli), version courte sur téléphone, dans les trois langues. Recreio : « Le quartier avec le plus de spots de Rio », « Hébergement devant les vagues », « Autour : bars de plage, concerts et nature ». Itacaré : « Une des meilleures côtes de surf du Brésil ». Les deux textes sont dans la page ; l'un est masqué selon la largeur (`data-long` / `data-court`).
- **Zoom à la saisie sur iPhone** : Safari zoome quand on touche un champ dont le texte fait moins de 16 px ; c'était le cas des champs « Destination » et « Dates » depuis leur passage sur une ligne (12,5 px). Tous les champs du site sont à 16 px sur téléphone ; ceux du module de l'en-tête sont réduits à 80 % à l'affichage pour garder leur taille.

## Premier écran « capsule » (16/11/2026, soir)

- **Accueil, téléphone** : vidéo, marque, titre, puis une capsule à deux champs (« Destination », « Dates ») et le bouton « Créer mon séjour » ancré dessous, dans la page. « Voyageurs » n'est plus dans le premier écran. Le bouton flottant et la bulle WhatsApp ne s'affichent pas tant que l'en-tête est à l'écran.
- **Description** : sous le bouton, en deux temps. D'abord « Venez pour le surf, repartez avec le Brésil. » en serif italique jaune, puis la phrase descriptive en petit.
- **Parcours vérifié** : destination et dates choisies dans la capsule, puis le bouton ouvre le tunnel directement à l'étape Hébergement du bon camp.
- **Galerie « La vie avec Surf Inn »** : retirée de l'accueil (masquée, le code reste).
- **Corrigé** : l'empilement des cartes du concept ne fonctionnait plus (le blocage du défilement vertical des bandes s'appliquait à tort à cette section) ; l'espace sous « Brésilien ? » passe de 64 à 26 px.
- **Pages camp** : la galerie « Le quotidien » de Rio est retirée (masquée) ; le module Instagram prend le titre « Le quotidien à Surf Inn Rio » / « Le quotidien à Surf Inn Bahia », dans les trois langues.
- **Menu « Destination » sur téléphone** : toujours au centre de l'écran, sur un voile, comme le calendrier. Il se plaçait d'après la position du champ au moment du toucher, d'où des ouvertures très basses.
- **Capsule** : plus de flèche dans « Destination » sur téléphone (elle recouvrait le texte).
- **Concept de l'accueil** : phrase raccourcie sur téléphone, sans la liste des quatre verbes ; texte complet sur ordinateur.
- **Voyageurs** : sur téléphone, le nombre de voyageurs se règle dans la fenêtre des dates (ligne « Voyageurs » avec − et +, hors tunnel). Le champ « Dates » de l'accueil affiche « 10 → 17 déc. · 3 pers. ». Parcours vérifié : le nombre est repris dans le tunnel. Sur ordinateur, les trois champs sont inchangés.
