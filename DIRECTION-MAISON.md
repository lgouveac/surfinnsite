# Direction 3 : « Maison »

Branche `refonte-maison`, ouverte le 12/11/2026 à partir de `refonte-synthese`. Premier jet.

## Le problème à résoudre

La version 2 (`refonte-synthese`) est plus vivante et hiérarchise mieux l'information, mais elle parle à des 18-30 ans. La clientèle visée est désormais plus âgée : 30 ans et plus, souvent en télétravail, CSP+, budget plus élevé.

Ce qui fait « jeune » dans la version 2 n'est pas le mouvement. Ce sont cinq signaux :

1. La police de titres (Londrina Solid) : ronde, grasse, proche de l'affiche de festival.
2. Les cartes penchées, les photos en « polaroid » et les stickers.
3. Les grands aplats jaunes.
4. Les chiffres et numéros géants, les mots au contour épais.
5. Les mouvements à rebond.

## Le parti pris

La plateforme de marque v6 donne la réponse : « Premium dans ce qui s'achète, populaire dans ce qui se vit ». Le site est ce qui s'achète : il doit donc être premium dans son exécution, et laisser les photos, les noms et les détails vrais porter le côté populaire.

Elle décrit aussi le ton : hôte et pas animateur, chaleureux et pas effusif, sûr et pas vendeur, cultivé et pas professoral. La version 2 a parfois le ton de l'animateur. Cette direction prend celui de l'hôte.

Référence visuelle : un magazine de voyage ou une maison d'hôtes soignée, pas une auberge de jeunesse.

## Ce qui change

| Élément | Version 2 | Maison |
|---|---|---|
| Titres | Londrina Solid, très gras, jusqu'à 136 px | Fraunces (serif), graisse normale, 68 px au plus |
| Mot « SURF INN » sur la vidéo d'accueil | Londrina | Londrina, inchangé : c'est la signature |
| Cartes et photos | penchées, cadre blanc, stickers | droites, angles peu arrondis, sans cadre |
| Jaune | aplats entiers | boutons, chiffres, filets |
| Fonds | jaune, écume, encre | sable, écume, encre |
| Chiffres | géants | serif fin, taille moyenne |
| Mouvement | rebonds, rotations | fondus plus lents, léger soulèvement au survol |

## Ce qui est conservé

Tout ce qui rendait la version 2 expérientielle : révélations au défilement, pellicule « Le Brésil, c'est… », texte de « Pourquoi Surf Inn existe » qui s'éclaire, photos qui glissent dans leur cadre, chiffres qui comptent, jauges, houle du Guide surf, menu mobile plein écran, planche de défilement. Aucun texte n'a changé, donc rien ne bouge côté SEO et lisibilité par les IA.

## Comment c'est fait

Un seul fichier, `outils/experience/maison.css`, posé par-dessus `couche.css` par `outils/experience.py`. Le supprimer redonne la version 2 à l'identique. La police Fraunces est ajoutée à l'appel Google Fonts existant.

## Ce que ce premier jet ne fait pas

Le registre visuel ne suffit pas à convaincre ce public. Restent, par ordre d'effet attendu :

1. **Choix des photos** (première passe faite, voir plus bas). Plusieurs images clés montraient des groupes de vingtenaires en maillot (« Pour qui » sur l'accueil, pilier « Se poser », héros de Rio). Pour un public de 30 ans et plus : chambres privées, bureau avec vue, table du petit-déjeuner, un cours à trois, des visages de 30-45 ans. C'est le levier le plus fort et il dépend des photos disponibles.
2. **Page « Travailler et surfer »** (`/work-and-surf/`, prévue par la plateforme) : Starlink, bureaux, chambres avec bureau, fuseau horaire, journée type. La plateforme demande que ces arguments restent sur cette page et sur les pages produit, pas sur l'accueil.
3. **Chambres privées en premier** dans l'onglet Le camp et dans le tunnel, dortoirs ensuite.
4. **Le conseiller plutôt que le prix** : la plateforme en fait un marqueur premium. À rendre visible près des boutons « Créer mon séjour » (un nom, un visage, un délai de réponse).
5. **Avis** : mettre en avant ceux de voyageurs plus âgés ou en télétravail (l'un d'eux écrit « j'ai la quarantaine »).
6. **Textes** : quelques formules d'animateur à reprendre (« probablement mouillé »).

## Photos : première passe (12/11/2026)

Six images clés remplacées, uniquement avec des photos déjà présentes sur le site. Les remplacements sont dans `outils/experience.py` (bloc « Photos clés »), donc propres à cette branche.

| Emplacement | Avant | Après |
|---|---|---|
| Accueil, pilier « Apprendre » | quatre personnes qui posent avec leurs planches | un moniteur qui tient la main d'une élève sur sa planche |
| Accueil, pilier « Se poser » | trois vingtenaires en maillot | le hamac d'une chambre privée (Itacaré) |
| Page « Pour qui », profil « Se poser » | groupe en rang devant les planches | la table du petit-déjeuner |
| Rio, « Le quotidien » | groupe en rang | le jardin de la Surf House |
| Rio, « Le quotidien » | tablée de bières, le soir | le salon du Surf Club |
| Rio, « Le quotidien » | sortie nocturne devant une fresque | point de vue en randonnée |

Retours de Kévin du 12/11 : « Le quotidien » de Rio ne montre que des photos de Rio (l'accolade et la table du petit-déjeuner sont à Bahia, retirées de cette page) ; la surfeuse d'origine est remise sur « Pour qui » de l'accueil ; « Explorer » garde le couple.

**Pellicule « Le Brésil, c'est… »** : les cartes passent en largeur. Les photos sources sont larges et basses (souvent 1000 × 444) ; dans des cartes hautes, elles étaient recadrées au centre et agrandies plus de deux fois sur un écran Retina, d'où le flou et les cadrages ratés. Le zoom lent est retiré. Aucune retouche d'image.

Deux de ces choix appliquent une règle de la plateforme : « aucune photo de groupe en rang ».

Non touché : les vidéos d'en-tête, les galeries de chambres, les photos d'expériences, le pilier « Apprendre » (quatre personnes qui posent avec leurs planches, à voir).

Ce qui manque dans la photothèque du site pour ce public : des visages de 35-50 ans, une personne en visioconférence ou au travail vue de face, un couple, une chambre privée avec quelqu'un dedans. Toutes les photos de travail montrent la même personne de dos.

## Page « Travailler et surfer » (12/11/2026)

Nouvelle page, en trois langues : `/work-and-surf/`, `/fr/travailler-et-surfer/`, `/pt/trabalhar-e-surfar/`. Elle est dans le gabarit (bloc `isWork`), avec sa route, son titre, ses balises de langue, le plan du site et `llms.txt`. Lien dans le pied de page.

Contenu : ce qu'il y a pour travailler (Starlink, coin coworking, bureau en chambre, restaurants), le fuseau horaire, les deux camps avec lien vers les chambres, un avis de long séjour, trois questions, appel à créer son séjour.

Tout ce qui est affirmé vient de textes déjà présents sur le site. Deux choses sont nouvelles et à valider :

- **Le fuseau horaire.** La page dit : 4 à 5 heures de moins qu'à Paris, donc aux horaires européens on travaille tôt et l'après-midi est libre ; aux horaires nord-américains, ce sont les matinées. La page « Pour qui » dit aujourd'hui l'inverse (« matinées libres pour surfer quand on travaille aux horaires européens ») : c'est une erreur à corriger là-bas.
- **Le portugais** est à relire par Lucas, comme le reste.

Pas encore fait : lien depuis l'accueil et depuis le profil « Travailler » de « Pour qui », données structurées pour les trois questions, tarifs ou conditions de long séjour (je n'ai aucune information dessus), débit Starlink mesuré.

## Questions ouvertes

- **Fraunces** est une proposition. Si le studio d'identité livre une police de titres, elle la remplace en changeant une ligne.
- **La planche « Fais défiler pour surfer »** : conservée, mais c'est l'élément le plus ludique qui reste.
- **Itacaré** garde sa palette verte et orange.

## Chargement des vidéos et boutons de l'accueil (12/11/2026)

- **Vidéos de fond** : la vidéo reste invisible tant qu'elle ne joue pas vraiment ; l'image d'attente est affichée derrière. Le navigateur n'a donc plus rien sur quoi poser son bouton de lecture (cas d'un chargement lent ou du mode économie d'énergie de l'iPhone, où la vidéo ne démarre pas : l'image fixe reste). Pendant le chargement, un filet lumineux jaune glisse tout en haut de l'écran, neuf secondes au plus. Code : `videos()` dans `couche.js`.
- **Boutons** : logique à deux niveaux. Principal : « Créer mon séjour » (jaune). Secondaire : bouton plein sombre (`data-vers-onglet`), utilisé pour « Découvrir Surf Inn Rio », « Découvrir Surf Inn Bahia » sur l'accueil et pour « Voir le camp », « Voir toutes les expériences », « Voir les packages et les cours » sur les pages camp.

## Retours mobile de Kévin (12/11/2026, soir)

- **Menu des onglets des pages camp** : collé au bas de l'en-tête. Il avait 28 px de marge au-dessus, où le fond de page apparaissait.
- **Galerie ouverte sur téléphone** (expériences, chambres) : la photo est limitée à 44 % de la hauteur, le texte tient dessous et peut défiler, le fond est opaque. Le bouton « Créer mon séjour », la bulle WhatsApp et la bande de défilement sont masqués tant que la galerie est ouverte.
- **Packages sur téléphone** : chaque carte tient entière à l'écran (onglet Packages : 608 → 410 px ; tunnel : 496 → 339 px). Photo plus basse, texte resserré ; la ligne « X nuits en chambre partagée ou privée » est retirée sur téléphone, la durée restant dans la pastille. Dans le tunnel, le sous-titre de l'étape est masqué sur téléphone.
- **Tunnel** : après le choix du camp, les dates sont amenées à l'écran.
- **Vidéos qui ne démarrent qu'au défilement** : non reproduit. Sur la préversion, sans toucher l'écran, les trois vidéos démarrent 1,5 à 5 secondes après l'affichage de la page (WebKit iPhone et Chrome mobile). Le démarrage au premier geste est le comportement prévu quand l'iPhone est en mode économie d'énergie, qui refuse toute lecture automatique.

## Survol des boutons (13/11/2026)

Relevé sur douze pages (`audit/retours/survol.mjs`). Avant, « Créer mon séjour » avait trois comportements au survol : rouge de l'ancienne charte (menu du haut, en-têtes, formulaire de contact), aucun changement (appels finaux, bande « Envie de venir ? », page Travailler et surfer). Et les boutons secondaires passaient au jaune, c'est-à-dire à la couleur du bouton principal.

Maintenant, partout :

- **Principal** (jaune) : jaune plus soutenu au survol. Sur Itacaré (orange) : orange plus soutenu.
- **Secondaire** (sombre) : bleu-vert « mer » au survol. Sur Itacaré (vert) : vert plus clair.
