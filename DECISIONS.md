# Branche `refonte-synthese` : arbitrages du 11/11/2026

Synthèse préparée pendant l'absence de Kévin. Rien n'a été touché sur `main`.

## Ce qui vient d'où

| Élément | Origine |
|---|---|
| Polices Londrina Solid + Chivo, couleurs « surf », « SURF INN » géant, marée en bas avec planche et bouées, menu mobile flottant, barre d'onglets fusionnée, physique de la planche | `refonte-experientielle` |
| Apparition échelonnée du hero, `llms.txt` | `main` / `corrections-audit-beta` (fusion sans conflit) |
| Toutes les corrections de l'audit, retours de Lucas et de Kévin, SEO (adresses par langue, hreflang, sitemap), Cookiebot, GTM | déjà communs aux branches |
| Couche expérientielle (`outils/experience/`) | nouveau |
| Ligne de planche sous le menu | `refonte-maree-haut`, **non reprise** |

## Arbitrages

1. **Base = refonte, pas la bêta actuelle.** Boj trouve le site « SaaS à l'ancienne » et Kévin a constaté que Londrina ne marche qu'avec sa police de texte et ses couleurs : c'est le cas sur la refonte.
2. **Planche en bas plutôt qu'en haut.** La version du bas sert aussi de navigation (bouées cliquables, nom de la section) et correspond à l'indicateur de progression de la maquette. La version du haut est plus discrète mais n'apporte que le décor. À confirmer : sur mobile, la marée prend environ 65 px en bas d'écran.
3. **Aucun texte changé ni retiré.** Les modules sont rhabillés et animés ; les mots restent les mêmes dans la page, donc `llms.txt` et le SEO restent valables.
4. **Mouvement uniquement en CSS et en petit script, sans bibliothèque ni vidéo ajoutée.** Poids ajouté : environ 20 Ko. Tout est désactivé avec « réduire les animations », et sans script le site s'affiche comme avant.
5. **Stickers Brésil utilisés à petite dose** (coco, ballon de futevôlei, parasol) alors que Kévin n'a pas encore choisi dans les planches : faciles à retirer ou à changer (`outils/experience/stickers.json`).
6. **Choix déjà tranchés non rouverts** : backend reporté, textes en portugais visibles, « Créer mon package » en premier, structure des adresses.
7. **Pas de réservation à la journée en 3 clics** comme dans la maquette : Surf Inn vend des séjours. Le module du hero (camp, dates, voyageurs, bouton) reste le chemin court.

## Modules rendus expérientiels

- **« Le Brésil, c'est… » (accueil / Notre concept)** : grand aplat encre, titre géant, les quatre mots en lettres géantes au contour (le mot actif se remplit en jaune avec un trait ondulé), photos en pellicule horizontale à faire glisser (doigt ou souris), cartes légèrement penchées qui se redressent au survol, entrée en cascade rejouée à chaque changement de mot, zoom lent des photos, deux stickers flottants.
- **« Pourquoi Surf Inn existe » (À propos)** : aplat jaune soleil, la photo de Lucas arrive penchée et se pose pendant le défilement, le texte s'éclaire ligne à ligne au rythme du défilement, sticker parasol.
- **Piliers d'À propos** : cartes révélées en cascade, qui se soulèvent au survol.
- **Les quatre piliers de l'accueil (Apprendre, Travailler, Se poser, Explorer)** : affiches légèrement penchées qui se redressent au survol, pastille « + » jaune qui tourne ; sur téléphone, les quatre cartes s'empilent comme un jeu de cartes pendant le défilement.
- **Les quatre profils de « Pour qui »** : même traitement en cascade, photo qui s'approche au survol.
- **Photos des deux camps et de « Pour qui » (accueil), appel final** : la photo glisse dans son cadre au défilement ; titre géant sur l'appel final.
- **Partout** : titres de section et cartes des bandes horizontales révélés à l'arrivée dans l'écran.

## Reste ouvert

- Les messages vocaux de Boj ne sont pas dans les conversations : seuls ses retours déjà notés (maquette, lecture par les IA) sont pris en compte.
- Planche en bas ou en haut ; stickers à garder ou non ; police de texte (Chivo ici, Rubik et Figtree proposées).
- Modules encore « classiques » : l'intérieur des pages camp (hébergement, activités, packages, guide de surf), les avis, la FAQ. Le bloc de chiffres des pages camp existe dans le code mais n'est pas affiché : rien à animer.
- Le texte reste affiché par JavaScript : la vraie réponse SEO/IA est le site Astro ; `llms.txt` fait le pont.
- Vérifié en local sous Chrome (ordinateur et mobile 390 px, avec et sans « réduire les animations ») ; **pas encore vérifié sur un vrai iPhone / Safari**.

## Retours de Kévin après relecture (11/11/2026, soir)

- Direction validée : polices, combinaison et couleurs.
- Barre de quatre couleurs sous le menu retirée partout (ordinateur et mobile).
- Libellé sous la planche : il reprend le petit titre en majuscules de la section (« Le concept Surf Inn », « Pour qui »…) plutôt que le titre long ; « Avis » devient « Nos avis » en français ; sans petit titre, le titre de la section. Sur téléphone, il est centré et s'affiche en entier.
- Rio et Itacaré sur mobile : plus de logo dans le menu secondaire, qui prend toute la largeur en haut ; la pastille du menu principal passe juste dessous ; la flèche de défilement des onglets est de nouveau visible.
- Menu mobile ouvert : écran plein en couleur encre, grands liens (la page en cours en jaune), bouton qui devient une croix jaune, page figée derrière ; il ne se confond plus avec la page quand on a défilé.

## Autres pages retravaillées (11/11/2026, soir)

- **Pages camp, chiffres du spot** (5 spots, 340+ jours, 26 °C…) : panneau encre, chiffres géants en jaune qui comptent en arrivant dans l'écran ; le texte d'origine est remis tel quel à la fin. Sur téléphone, bande sombre à faire glisser.
- **Pages camp, « Notre façon d'enseigner »** : quatre temps, grands numéros au contour qui se remplissent à l'arrivée.
- **Pages camp, « Le quotidien »** (Rio) : photos posées comme des tirages, penchées, qui se redressent et grossissent au survol.
- **Pages camp, appel final** : titre géant, photo qui glisse au défilement.
- **À propos, l'équipe** : portraits plus grands, penchés, avec un halo jaune ou bleu-vert.
- Non retravaillés : onglets Le camp, Expériences, Packages et Guide surf ; carte, région, Instagram, avis, FAQ.


## Onglets des pages camp (12/11/2026)

Même principe que les lots précédents : aucun texte modifié, tout passe par `outils/experience/` (attributs `data-lieux`, `data-faits`, `data-tirages`, `data-inclus`, `data-experiences`, `data-forfaits`, et `data-methode` réutilisé).

- **Le camp** : les trois lieux de Rio en affiches légèrement penchées qui se redressent au survol ; bloc du shaper avec chiffres géants qui comptent et photos posées comme des tirages ; pastilles « Inclus dans chaque séjour » qui apparaissent en cascade.
- **Expériences** : section sur aplat encre, grand titre, sous-titres en jaune, mosaïque de photos penchées qui se redressent et zooment au survol (bande à faire glisser sur mobile, inchangée).
- **Packages surf** : cartes qui se soulèvent au survol, jauge d'intensité qui se remplit à l'arrivée, « Le déroulé d'une session » en grands numéros qui se remplissent (même traitement que « Notre façon d'enseigner »).
- Non retravaillés : onglet Guide surf, espaces communs et chambres (carrousels existants), FAQ.
- À voir : sur Itacaré, le chiffre du shaper affiche « 1st » en français (contenu existant, non modifié).


## Onglet Guide surf (12/11/2026)

Aucun texte modifié (attributs `data-saisons`, `data-spots`).

- **Saisons** : quatre affiches légèrement penchées, mois en grand et en jaune ; au pied de chaque carte, une houle dessinée dont la hauteur suit la taille des vagues annoncée (lue dans le texte par `houle()` dans `couche.js`) et qui monte à l'arrivée. Sur mobile, les quatre saisons deviennent une bande à faire glisser (la page perd environ 500 px).
- **Spots** : noms en grand, cartes qui arrivent une à une par la gauche.
- Titre de section et sous-titres agrandis, comme dans Expériences.
- Piège noté : le moteur de gabarit réécrit `viewBox` et `preserveAspectRatio` même dans une image SVG intégrée au CSS ; ils y sont écrits `view%42ox` et `preserve%41spect%52atio`.


## Retours de Kévin sur l'aperçu des pages camp et l'accueil (12/11/2026)

- **Boutons vers les onglets** (aperçu Rio et Itacaré) : « Voir le camp », « Voir toutes les expériences » et « Voir les packages et les cours » ont maintenant le même bouton plein (attribut `data-vers-onglet`), plus grand, qui passe au jaune au survol. Avant : un bouton et deux liens de texte de couleurs différentes.
- **Chiffres « Surfer à… »** : la taille du chiffre suit la largeur de sa colonne (et non plus celle de l'écran), donc plus de débordement. Itacaré (6 chiffres) : 3 colonnes sur 2 rangées ; Rio (5 chiffres) : 5 colonnes dès 1000 px.
- **Accueil, bande « Envie de venir ? »** : bouton en encre sur l'aplat jaune (il était jaune sur jaune).
- **Nom du camp à côté du logo** : en blanc tant que le menu est posé sur la vidéo ou la photo, couleur d'origine ensuite.
- Vu en passant, non traité : sur mobile, le bouton flottant « Créer mon séjour » (jaune) passe au-dessus de sections jaunes pendant le défilement.


## Retours d'usage d'un ami de Kévin (12/11/2026)

Posés par `outils/retours_ami.py` (styles dans `outils/retours_ami.css`), sur les trois versions du site.

1. **Cookies** : le bandeau Cookiebot n'est plus une fenêtre au milieu de l'écran. Carte en bas à gauche (bandeau en bas sur mobile), couleurs du site, « Refuser » et « Tout autoriser » de même taille, onglet Détails conservé pour le choix par catégorie. Ne s'affiche que sur le domaine déclaré chez Cookiebot ; réglé sur le site en ligne par injection des styles.
2. **Vidéo trop rapide** : non traité, c'est une question de montage (plans plus longs). La ralentir donnerait un rendu artificiel.
3. **Tunnel** : croix de sortie en haut à droite (il n'y en avait pas, on ne sortait que par le logo).
4. **Bouton du bas de l'accueil** : même bouton que celui du haut.
5. **Instagram sur l'accueil** : nouveau bloc avant l'appel final, six photos et les liens vers @surfinnrio et @surfinnbahia. La remarque « la vidéo d'en-tête fait trop marketing » relève du montage.
6. **Menu** : « Nos surf camps » remplace les deux entrées Rio de Janeiro et Itacaré sur ordinateur et ouvre un sélecteur avec photo. Le menu mobile garde les deux liens.
7. **Clins d'œil en portugais** (« Brasileiro? Você já sabe… » sur l'accueil, « E aí, brasileiro? » sur Pour qui) : visibles par tous, précédés du même mot dans la langue du visiteur (« Brésilien ? Brasileiro? Você já sabe… », « Brésilien ? E aí, brasileiro? »). En portugais, pas d'amorce.
8. **Tunnel, étape Package** : les quatre cartes tiennent sur une ligne sur ordinateur (la quatrième était hors écran).
9. **Menu** : « Nos surf camps » est aligné sur les autres entrées (il était 4,5 px trop haut).
10. **« Le Brésil, c'est… »** : le défilement automatique des mots ne tourne que lorsque la section est à l'écran. Le visiteur arrive toujours sur « surfer », reste cinq secondes par mot, et le défilement se met en pause dès que la section sort de l'écran.
11. **« Le Brésil, c'est… »** : le défilement automatique s'arrête pour de bon dès que le visiteur touche aux photos (doigt, clic, molette horizontale), comme lorsqu'il clique sur un mot. Sur ordinateur, il est en pause tant que la souris est sur les photos.
10 bis. **Cookies sur téléphone** (14/11) : bandeau compact, environ un quart de l'écran au lieu de près de la moitié ; le texte défile dans son cadre, les trois choix restent visibles.

## Échelle typographique (14/11/2026)

Le relevé des 17 pages comptait 30 tailles de texte sur téléphone et 39 sur ordinateur. Le site suit maintenant une échelle de neuf tailles, posée par `outils/echelle.py` au moment où la couche est construite (le gabarit n'est pas modifié).

| Rôle | Téléphone | Ordinateur |
|---|---|---|
| Légende, libellé | 12 | 12 |
| Petit texte, pied de page | 14 | 14 |
| Texte courant, boutons | 16 | 16 |
| Texte mis en avant | 18 | 18 |
| Titre de carte | 21 | 24 |
| Sous-titre | 24 | 30 |
| Titre de section | 29 | 40 |
| Titre de page | 33 | 56 |
| Grands chiffres, « Le Brésil, c'est… » | 48 | 72 |

Hors échelle : le nom « SURF INN » sur la vidéo (logo) et les chiffres dont la taille suit la largeur de leur carte.
Polices : Chivo (texte), Gabarito (titres), Permanent Marker (phrase d'accroche seulement), Londrina Solid (logo). Fraunces est retirée. Graisses de Chivo : 400, 600, 700.
Toute nouvelle règle de style doit prendre une taille de cette échelle ; `audit/retours/tailles.mjs` refait le relevé.
