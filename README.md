# Surf Inn · site bêta

*English version: [README.en.md](README.en.md).*

Ce dépôt contient le site de Surf Inn, deux surf camps au Brésil (Rio de Janeiro et Itacaré, Bahia), en anglais, français et portugais. Il est publié sur Vercel à l'adresse `https://surfinn-beta.vercel.app`, sans mot de passe mais masqué aux moteurs de recherche. Ce document s'adresse à la personne qui reprend le site pour la mise en production et le backend (Flowcode) ; l'historique détaillé des changements est en bas, dans la section « Historique ».

La cible durable est le site Astro `surfinnrio/surfinn-site`. Ce dépôt-ci est la version qui sert de référence en attendant.

## Comment le site est fait

`index.html` est un **fichier empaqueté** (format « bundler » hérité de Claude Design, qu'on n'utilise plus depuis le 09/11/2026). On ne le modifie jamais à la main : le HTML et tout le code React du site sont dans le bloc `<script type="__bundler/template">`, sous forme d'une chaîne JSON ; les traductions, le moteur de rendu et quelques feuilles de style sont dans le bloc `<script type="__bundler/manifest">`, en base64 (parfois compressé en gzip). Un petit chargeur en tête de page décode le tout dans le navigateur. Les images sont servies à part depuis `assets/` (le bloc `__bundler/external` fait le lien entre un identifiant et un chemin), et les vidéos depuis `videos/`.

`index.html` reste la seule source de vérité : les outils de `outils/` le décodent, le modifient puis le réécrivent.

### Chaîne de construction

Python 3 suffit, sans dépendance. Depuis la racine du dépôt :

```bash
python3 outils/paquet.py extraire     # décode index.html dans .travail/ (gabarit.html + textes/), dossier jetable ignoré par git
python3 outils/experience.py          # pose les couches et les corrections dans .travail/
python3 outils/paquet.py empaqueter   # réécrit index.html à partir de .travail/
python3 outils/images_mobiles.py      # seulement après ajout ou remplacement d'une photo dans assets/ (demande Pillow)
```

Ensuite : commit et push. Vercel redéploie seul.

- `paquet.py extraire` écrit `.travail/gabarit.html` (le gabarit HTML et le code du site) et `.travail/textes/<uuid>.<ext>` (traductions `i18n`, moteur de rendu, CSS, décompressés).
- `experience.py` modifie `.travail/gabarit.html` et le fichier de traductions de `.travail/textes/`. Il est conçu pour être relancé sur un `index.html` déjà construit : la couche CSS et JS est réécrite entre les repères `<!-- couche-experience:debut -->` et `<!-- couche-experience:fin -->`, et chaque remplacement ne s'applique que si son résultat est absent. Il s'arrête avec un message quand un repère attendu est introuvable ou ambigu, et refuse certaines erreurs connues du moteur de gabarit (voir les pièges ci-dessous).
- `paquet.py empaqueter` réencode le gabarit et les textes dans `index.html`. Une modification faite directement dans `.travail/gabarit.html` (sans passer par `experience.py`) est donc conservée : elle part dans `index.html` et sera lue telle quelle à la prochaine extraction.

- `images_mobiles.py` fabrique les versions réduites des photos (`assets/m/<nom>-480|720|960.webp`) et pose, dans la tête de `index.html` entre `<!-- images-mobiles:debut -->` et `<!-- images-mobiles:fin -->`, le script qui les sert aux écrans de 900 px ou moins (srcset et taille affichée réelle). L'ordinateur et la galerie plein écran gardent les photos d'origine. `empaqueter` ne touche pas à ce script ; il n'est à relancer que quand les photos changent (sinon une nouvelle photo est simplement servie en taille d'origine).

Les autres scripts de `outils/` :

- `outils/experience/` contient les sources de la couche posée par `experience.py` : `couche.css`, `couche.js`, `maison.css`, `mobile.css` (règles mobiles, voir `REGLES-MOBILE.md`) et `stickers.json`. Elles sont relues à chaque passage.
- `echelle.py`, `activites.py` et `legal.py` ne se lancent pas seuls : ce sont des modules importés par `experience.py`, donc **rejoués à chaque construction**. `echelle.py` ramène les tailles de texte à neuf valeurs, `activites.py` contient les descriptions des activités dans les trois langues, `legal.py` le contenu des pages légales (informations légales, confidentialité, conditions de réservation, à faire valider par un juriste avant le lancement). Attention à l'exception décrite plus bas pour `legal.py`.
- `retours_ami.py` (avec `retours_ami.css`) est **ponctuel** : il a été lancé une fois le 12/11/2026 et son résultat est déjà dans `index.html`. Il ne faut pas le relancer.
- `paquet.py externaliser` est une opération unique, déjà faite : elle a sorti les images du manifeste vers `assets/`.

### Pièges connus

- **camelCase suivi de ` =`** : dans un `<script>` du gabarit, le moteur de gabarit réécrit une variable en camelCase suivie de ` =` comme s'il s'agissait d'un attribut (`fooBar =` devient `sc-camel-foo-bar =`). Utiliser des noms sans majuscule (`foo_bar`). `experience.py` refuse ce motif dans `couche.js`.
- **`viewBox=`** : dans un SVG en `data:`, `viewBox=` est réécrit de la même façon. `experience.py` le contourne en encodant le `B` (`view%42ox`).
- **`{{` dans les feuilles et scripts de la couche** : interdit, le moteur le prendrait pour une variable. `experience.py` s'arrête s'il en trouve.
- **Blocs gardés par un test** : certains blocs de `experience.py` ne s'exécutent que si leur résultat est absent du gabarit (par exemple les pages légales, `if "legal: { en: 'legal/'" not in s`). Comme le gabarit est déjà construit, ils ne se rejouent pas : modifier `legal.py` ne change pas le site. Il faut ajouter dans `experience.py` un remplacement explicite de l'ancien texte par le nouveau.
- **Zone indentée avant « Lot vocabulaire »** : l'endroit où l'on ajoute habituellement un lot de corrections, juste avant la ligne `    # Lot vocabulaire (17/11/2026, option A`, est à l'intérieur d'un grand bloc indenté de 4 espaces (`if os.path.exists(mobile):`). Tout code ajouté là doit être indenté de 4 espaces ; sinon, la suite du fichier devient le corps du dernier `if` ajouté, ce qui fonctionne par hasard puis casse.
- **Noms déjà pris** : avant d'ajouter une donnée à l'objet d'un camp, vérifier que le nom n'existe pas déjà plus bas (c'était le cas d'`expIntro`) ; la dernière clé l'emporte.
- **Palette** : à la fin d'`experience.py`, des couleurs sont converties sur tout le gabarit, feuilles de style comprises. Une couleur écrite dans `mobile.css` peut donc être changée à la construction.
- **Contrôle utile** après un gros changement : repartir d'un `index.html` ancien (`git checkout <commit> -- index.html`), relancer la chaîne complète et comparer au résultat courant.

### Mesure d'audience et cookies

- Google Tag Manager : conteneur `GTM-WH4MTLKG`, posé dans le gabarit. Il porte Google Analytics, Microsoft Clarity et les événements du site envoyés dans `dataLayer` (`virtual_page_view`, `funnel_open`, `generate_lead`, `share_click`, `share_visit`). **Le conteneur n'est pas publié** : c'est voulu, pour ne pas mélanger le trafic de la bêta avec celui du site actuel.
- Cookiebot (identifiant `4b033d94-b9f9-4c38-b4ff-26b90636072e`) est **éteint** par l'interrupteur `COOKIEBOT_ACTIF = False` dans `outils/experience.py`, parce que le site vise d'abord le Brésil. Éteint, il n'y a pas de bandeau, le consentement Google (Consent Mode v2) est accordé par défaut et le lien « Gérer mes cookies » est masqué. Pour le rallumer : mettre `True`, relancer la chaîne de construction. Le code de Cookiebot est resté en place. À reconsidérer dès que le site visera l'Europe (idéalement en n'affichant le bandeau qu'aux visiteurs européens).

## Les fichiers à la racine

- `index.html` : le site entier, empaqueté (voir plus haut).
- `assets/` : les images, nommées par empreinte, servies avec un cache d'un an.
- `videos/` : les vidéos d'ouverture des pages, en deux versions. Le chargeur choisit `videos/hero-<page>-mobile.mp4` quand le petit côté de l'écran fait moins de 600 px et `videos/hero-<page>-ordi.mp4` sinon (variable `heroMobile` en tête de `index.html`), pour l'accueil, Rio et Itacaré.
- `vercel.json` : configuration Vercel. Il ajoute l'en-tête `X-Robots-Tag: noindex, nofollow` à toutes les réponses, met en cache les images, impose la barre finale dans les adresses, redirige `/en/…` vers la racine et `/surf-camp/` vers l'accueil, et renvoie toutes les adresses de page vers `index.html` (le site choisit lui-même la page et la langue à partir de l'adresse).
- `middleware.js` : fonction Vercel exécutée avant chaque page (pas pour les images, vidéos ni fichiers). Elle insère dans le HTML envoyé le titre, la description et les balises de partage (Open Graph, Twitter) propres à l'adresse demandée, pour que les aperçus WhatsApp, Instagram ou iMessage fonctionnent sans exécuter le site. Depuis le 18/11/2026, elle pose aussi dans la page brute la canonical, les hreflang (en, fr, pt, x-default = anglais) et, sur les pages camp, le fil d'Ariane en JSON-LD (`script#fil-ariane`), avec les mêmes attributs que le JavaScript du site, qui les met à jour sans doublon. Les correspondances d'adresses entre langues sont dans ses tables `PAGES` et `ONGLETS` : à tenir à jour avec `ROUTES`/`ONGLETS` du site et le script de langue en tête d'`index.html`. Elle calcule un ETag faible (index.html + texte injecté) et répond 304 quand rien n'a changé, avec `Cache-Control: public, max-age=0, must-revalidate`. Elle pose les en-têtes de sécurité (constante `SECURITE`, à garder identique à `vercel.json`) et l'en-tête `noindex`. Elle n'utilise plus de cookie de pays : `surfinn_country` n'est plus posé depuis le 18/11/2026.
- `seo.js` : les titres et descriptions de chaque adresse, dans les trois langues (`t` et `d` pour l'onglet et Google, `st` et `sd` pour les aperçus de partage, `i` pour l'image de partage). Il est lu par `middleware.js` côté serveur, et recopié dans le gabarit par `experience.py` pour le navigateur : après une modification de `seo.js`, relancer la chaîne de construction.
- `sitemap.xml` : la liste des 60 adresses du site avec leurs équivalents dans les autres langues (`hreflang`).
- `llms.txt` : le texte du site page par page, à l'intention des outils d'IA, parce que le site est rendu en JavaScript.
- `robots.txt` : autorise l'exploration par tous les robots. L'indexation est empêchée par l'en-tête `noindex`, pas par ce fichier.
- `package.json` et `package-lock.json` : une seule dépendance, `@vercel/functions` (utilisée par `middleware.js`), et Node 20 ou plus, la version minimale qu'elle demande. Il n'y a pas d'étape de build côté Vercel.
- `DECISIONS.md`, `DIRECTION-MAISON.md`, `DIRECTION-CHALEUR.md`, `REGLES-MOBILE.md`, `PHOTOS-A-FOURNIR.md` : notes de conception (arbitrages, directions graphiques, règles mobiles, photos à refaire).

Les adresses suivent le schéma `/surf-camp/<destination>/<onglet>/` pour les pages camp et `/about-us/`, `/reviews/`, `/faq/`, `/contact/`, etc. pour les autres ; l'anglais est à la racine, le français sous `/fr/` et le portugais sous `/pt/`, avec des adresses traduites. Les anciens dossiers `fr/`, `pt/` et `en/` ont été supprimés.

Ne sont pas versionnés (voir `.gitignore`) : `.travail/`, et les dossiers de travail `audit/`, `maquettes/`, `mesure/` et l'archive `audit-usabilite-beta-20261109.zip`, qui ne restent que sur le poste de Kévin. Les références à `audit/…` dans l'historique ci-dessous pointent donc vers des fichiers absents du dépôt.

## Avant la mise en production (Flowcode)

1. **Brancher les formulaires.** Aujourd'hui, ni le tunnel de réservation ni le formulaire de contact n'envoient quoi que ce soit : à la validation, l'état du composant passe simplement à `submitted: true` (tunnel) ou `contactSent: true` (contact), sans aucune requête réseau, et le visiteur voit l'écran de remerciement. Le backend est entièrement à faire. Un commentaire du gabarit décrit déjà la forme prévue des données du tunnel (cherchez `visitsurfinn.com custom package` dans `.travail/gabarit.html`).
2. **Retirer le `noindex`** à deux endroits : l'en-tête de `vercel.json` (bloc `"source": "/(.*)"`) **et** la ligne `h.set('X-Robots-Tag', 'noindex, nofollow')` de `middleware.js` (fonction de réponse, à côté de la constante `SECURITE`). Retirer l'un sans l'autre laisse les pages masquées.
3. **Changer de domaine dans `sitemap.xml` et `llms.txt`**, qui pointent tous deux vers `https://surfinn-beta.vercel.app`.
4. **Figer les adresses canoniques sur `https://www.visitsurfinn.com`.** Le code du site construit aujourd'hui `canonical`, `hreflang` et `og:url` à partir de `location.origin` (dans le navigateur) et de l'origine de la requête (dans `middleware.js`, fonction `domaine(url)`, à remplacer par `https://www.visitsurfinn.com`) : sur une préversion ou sur le domaine Vercel, elles pointeraient vers la mauvaise adresse.
5. **Publier le conteneur Tag Manager `GTM-WH4MTLKG`** le jour du lancement, pas avant (tant qu'il n'est pas publié, rien n'est mesuré : c'est voulu, pour ne pas mêler le trafic de la bêta). Il porte déjà Google Analytics (`G-J9J8RM4DX3`), Microsoft Clarity (`zfoewm9k5t`) et les événements du site. Accès : compte Google de Surf Inn (à demander à Kévin). Juste après la publication :
   - vérifier que le temps réel de Google Analytics et les enregistrements Clarity reçoivent des visites sur `www.visitsurfinn.com` ;
   - dans Google Analytics, marquer l'événement `generate_lead` (demande envoyée) comme événement clé, pour compter les demandes comme conversions.
6. **Redirections des anciennes adresses du site Framer : posées dans `vercel.json` (23/11/2026).** Les 11 redirections du plan `REDIRECTIONS.xlsx` sont en place. Le blog n'est pas redirigé : les deux articles sont repris aux mêmes adresses (`blog/`, pages statiques produites par `python3 outils/blog.py` à partir de `outils/blog/`), sauf l'article au tiret long, redirigé vers la même adresse sans tiret. Les origines portent une barre finale : avec `trailingSlash`, Vercel ajoute la barre avant d'appliquer les redirections, d'où deux sauts (308 vers `/ancienne/`, puis 308 vers la page finale), vérifiés sur l'aperçu. Reste à faire après la bascule : tester chaque ancienne adresse (onglet « Vérifications »).
7. **Images de `framerusercontent.com` : rapatriées dans `assets/` (23/11/2026)**, table `FRAMER` de `outils/experience.py` (la reconstruction s'arrête si une adresse Framer réapparaît).
8. Vérifier aussi : le domaine déclaré dans Cookiebot (seul `surfinn-beta.vercel.app` l'est) si on le rallume, et la relecture juridique des pages légales (`outils/legal.py`).
9. **À chaque photo ajoutée ou remplacée dans `assets/`, lancer `python3 outils/images_mobiles.py`** (demande Pillow : `pip3 install Pillow`), puis committer `assets/m/` et `index.html`. Ce script fabrique les versions réduites servies aux téléphones. Sans lui, rien ne casse, mais la nouvelle photo est envoyée en taille d'origine aux téléphones. Attention : une photo remplacée **sous le même nom** reste en cache un an chez les visiteurs (`Cache-Control: immutable` sur `/assets/`) ; donner un nouveau nom à toute photo modifiée.

Le dépôt pèse environ 400 Mo, surtout à cause des quelque 200 versions successives d'`index.html` (2,3 Mo chacune) conservées dans l'historique git. Si le poids gêne, on peut réécrire l'historique (par exemple avec `git filter-repo`) ou repartir d'un dépôt neuf contenant seulement l'état actuel ; ce n'est pas fait ici, parce que cela change tous les identifiants de commit et oblige chacun à recloner.

## Historique

Ce qui suit est le journal des changements tenu pendant la bêta, du plus ancien au plus récent, conservé tel quel à deux corrections près (signalées entre crochets). Les détails des branches de refonte sont dans `DECISIONS.md`, `DIRECTION-MAISON.md`, `DIRECTION-CHALEUR.md` et `REGLES-MOBILE.md`.

### Par rapport à l'export Claude Design (09/11 au 11/11/2026)

`index.html` est un fichier empaqueté : les textes et le code sont dans le bloc `__bundler/template` (texte JSON), les traductions dans le fichier `i18n.js` encodé dans le bloc `__bundler/manifest`.

- `detectLang()` : parcourt toutes les langues du navigateur (`navigator.languages`) et garde la première disponible parmi `en`, `fr`, `pt`.
- `isBrazilian()` : renvoie vrai seulement si le cookie `surfinn_country` vaut `BR`. Ce cookie est posé par `middleware.js` à partir du pays détecté par Vercel. [Périmé : la fenêtre brésilienne a été retirée et le cookie `surfinn_country` n'est plus posé depuis le 18/11/2026.]
- Vidéos : les 3 WebM ont été retirés du manifeste ; la page charge `/videos/hero-accueil.mp4`, `/videos/hero-rio.mp4` et `/videos/hero-itacare.mp4` (MP4 H.264, 30 images/s). [Périmé : ces trois fichiers ont été remplacés par les versions `-ordi` et `-mobile` décrites plus bas, puis retirés du dépôt le 18/11/2026.]
- Retours de Lucas (v18, 09/11) : traductions `i18n.js` v18, 61 corrections de l'anglais, 40 planches dont 20 Baltazar, accroche de Rio vide en PT, fenêtre brésilienne en bas de l'écran.
- Funnel de réservation (export `standaloneV20261109b`, dernier export Claude Design) : étapes Voyage, Séjour (type de chambre seulement) et Package refaites, chambre triple à Itacaré, « Surf Inn » corrigé dans les noms de packages. Fusionné avec la v18 ; la ligne du funnel en PT dit aussi « (depois do surf) ».
- Corrections de l'audit d'usabilité du 09/11/2026 (`audit/plan-corrections-20261109.md`) : images sorties du fichier (20,5 Mo → 1,9 Mo), écran d'attente traduit, `<title>` par langue, éléments cliquables atteignables au clavier avec focus visible, bulle WhatsApp en icône sur mobile et masquée dans le tunnel (et quand elle passerait sur un bouton), bouton du hero qui ouvre toujours le tunnel, camp obligatoire à l'étape 1 et présélectionné depuis une page camp, indice de défilement sur la barre d'onglets mobile, boutons −/+ de 44 px, délai « réponse rapide » partout, libellé unique du bouton mobile, messages WhatsApp préremplis traduits, singulier et date PT du récapitulatif, lien de la FAQ wifi, Rio « wifi rapide » en FR/PT, liens Instagram nommés, image Framer retirée, exemple de numéro neutre en EN, réassurance en double retirée.
- Retours de Lucas (09/11/2026) : un numéro WhatsApp par camp (Rio +55 21 99923-1992, Itacaré +55 73 99825-7683 ; sans camp connu, Rio), packages renommés (Surf In Rio, Onda Carioca, Surf Intensive ; Surf In Bahia, Onda Baiana, Surf Intensive), cours à Itacaré à 8h.
- Retours mobile de Kévin (10/11/2026) : hero de l'accueil, de « Pour qui » et d'« À propos » remontés ou centrés sur mobile ; barre « Créer mon séjour » en bouton flottant à côté de l'icône WhatsApp, masquée quand le menu est ouvert ; en-têtes des cartes camp sur une ligne ; menu « Our concept / Notre concept / Nosso conceito » ; textes des 4 piliers, de « Le Brésil, c'est… », de « Pour qui » et d'« À propos » réécrits dans les 3 langues ; « sous 24h » retiré des pages camp, Pour qui et À propos en FR et PT ; citation provisoire de Lucas retirée ; rôles d'Igor (gérant des surf camps) et de Kévin (marketing et stratégie).
- Correctif iPhone (10/11/2026) : champs en 16 px sur mobile (Safari zoomait sur les champs de 15 px et la page se décalait ensuite sur les côtés) ; calendrier centré dans l'écran sur mobile, sur un fond assombri.
- Retours du 10/11/2026 (suite) : tunnel sans présélection du camp, camp et dates exigés à l'étape 1 (ou « dates pas encore fixées ») ; textes de l'accueil (devant les vagues, piliers Apprendre et Se poser, « Le Brésil, c'est jouer ») ; rôles de Lucas (fondateur et gérant de Surf Inn Rio) et d'Igor (gérant de Surf Inn Bahia).
- Tunnel (10/11/2026) : étape Hébergement à Rio sans la description du haut ; l'écran descend vers la liste des chambres après le choix privée/partagée ; « Continuer » grisé ramène à ce qui manque (camp, dates, chambre, e-mail) ; bandeau récap retiré des étapes Package, Options et Coordonnées.
- Pages Rio et Itacaré, mobile (10/11/2026) : flèches de la barre d'onglets centrées, à gauche dès qu'on a défilé, masquées en fin ; textes de l'aperçu de Rio ; avis affichés en entier (plus de « Lire la suite ») ; tuiles d'activités non cliquables sur mobile ; vrai logo dans le bloc Instagram ; galerie : flèches sous la photo sur mobile, fond figé, photos préchargées, doublon retiré ; fenêtre des planches sans l'encart bleu ; onglet Packages sans le bloc final « Créer mon séjour ».
- Tunnel et accueil (10/11/2026) : marge rétablie à gauche de la rangée de packages ; récapitulatif en lignes (une information par ligne, « Modifier » à côté du titre) ; page finale courte, sans la note d'hébergement ni la vidéo de Lucas ; photos des camps de l'accueil non cliquables sur mobile ; « Le Brésil, c'est… » : les 4 mots sur une ligne et la phrase pour les Brésiliens sous les cartes, sur mobile.
- Hero de l'accueil et pied de page (10/11/2026) : plus de contour bleu au toucher des champs Destination et Dates ; sur mobile, champs Destination, Dates et Voyageurs en verre dépoli (la vidéo se voit derrière) ; espaces rétablis dans « ★ 4,9 · 438 avis Google » du pied de page.
- Pages camp, suite (10/11/2026) : photos de « Votre séjour » non cliquables sur mobile ; sous-titre des avis retiré ; galeries photos utilisables en glissant du doigt ; cartes « Espaces communs » et « Chambres » réduites à une photo sur mobile pour tenir dans l'écran ; « Randonnée cascade » dans les packages et bouton flottant masqué sur l'onglet Packages ; plus de « des gens d'ici » en français ; flèches de la barre d'onglets en vert sur Itacaré.
- Carte Google Maps à la demande (10/11/2026) : sur les pages camp, un aperçu (nom du camp, bouton « Afficher la carte », lien « Ouvrir dans Google Maps ») remplace la carte tant qu'on ne la demande pas. Moins de scripts Google, pages plus légères, plus d'erreurs Google quand on change de page pendant le chargement.
- Lot du 10/11/2026 (soir) : champs du hero en blanc translucide sans flou ; fermeture des galeries sans retour en haut de page ; arrivée sur une page camp par le menu comme à la première visite (onglet Aperçu, barre d'onglets au début) ; Instagram à 4 photos sur mobile ; pastille « Voir les photos » sur les cartes du camp ; module Baltazar Customs plus court ; tunnel : dates sans clavier, photo de chambre partagée d'Itacaré, « Composer mon package » guidé (Continuer grisé tant que rien n'est choisi) ; « Retour au site » vers l'accueil.
- Reconstruction : une vérification de syntaxe JavaScript (composant, scripts, traductions) bloque la mise en paquet en cas d'erreur.
- Lot du 11/11/2026 : accueil, pilier « Apprendre » regroupé en cinq puces (surf, surf guiding et analyse vidéo ; portugais ; percussion avec les rythmes brésiliens ; capoeira ; futevôlei et altinha), plus de cours de cuisine ; page « Notre concept », tags de la carte « Explorer » au même format que les autres cartes (fond blanc, contour plein).
- Vidéos hero sur téléphone (11/11/2026) : versions mobiles `videos/hero-*-mobile.mp4` (centre recadré en portrait à pleine résolution, H.264 sans son, environ 3 fois plus légères : accueil 4,7 Mo au lieu de 14,6 Mo, Itacaré 4,2 au lieu de 13,3, Rio 1,9 au lieu de 5,4), choisies au chargement quand le petit côté de l'écran fait moins de 600 px. Les ordinateurs gardent les originaux.
- Nouvelle vidéo d'ouverture de Rio (20/11/2026) : source iPhone 4K HDR 60 i/s de 22 s (114 Mo), passée en SDR par `avconvert --preset Preset1920x1080` (macOS), puis encodée avec ffmpeg en H.264 30 i/s sans son : `hero-rio-ordi.mp4` en 1280×720 (CRF 30, 5,3 Mo) et `hero-rio-mobile.mp4` recadrée au centre en 480×720 (CRF 28, 2,8 Mo). Même méthode pour remplacer une autre vidéo : garder les noms de fichiers, rien d'autre à changer.
- Lecture automatique sur iPhone (11/11/2026) : les vidéos reçoivent un vrai attribut `muted` (React ne l'écrit pas, ce qui empêche Safari iOS de lancer la vidéo seule et fait apparaître un bouton lecture), la lecture est relancée dès que possible et au premier toucher (mode économie d'énergie), et le bouton lecture natif d'iOS est masqué.
- Consentement et suivi (11/11/2026) : Google Consent Mode v2 posé en tête de page, tout refusé par défaut ; emplacements pour Cookiebot (chargé sans bloquer la page, blocage manuel, langue du visiteur) et Google Tag Manager (vides tant que les identifiants ne sont pas fournis : aucun appel à Google, Meta ou Cookiebot) ; événements envoyés dans `dataLayer` pour GTM : `virtual_page_view` (le site change de page sans changer d'adresse), `funnel_open`, `generate_lead` (demande envoyée, sans donnée personnelle).
- Une adresse par page et par langue (11/11/2026) : structure `/surf-camp/<destination>/<onglet>/` (onglets : `accommodation`, `activities`, `packages`, `surf-guide`), pages de service à la racine (`/about-us/`, `/reviews/`, `/faq/`, `/contact/`, `/who-is-it-for/`), anglais à la racine, `/fr/` et `/pt/` avec adresses traduites. L'adresse décide de la langue ; un bandeau propose la langue du navigateur, sans redirection. Titre de page, canonical, hreflang réciproques avec x-default et fil d'Ariane (JSON-LD) mis à jour à chaque page ; menu, pied de page et onglets en vrais liens `<a href>`. Côté Vercel : réécriture de toutes les adresses de page vers `index.html`, `/en/…` et `/surf-camp/` redirigés, `sitemap.xml` généré. Les anciens dossiers `fr/`, `en/`, `pt/` sont supprimés.
- Cookiebot branché (11/11/2026) : identifiant 4b033d94-b9f9-4c38-b4ff-26b90636072e, préréglage RGPD (consentement explicite, bouton « Tout refuser », tous les visiteurs), bandeau en anglais, français et portugais du Brésil, sans bouton flottant ; lien « Gérer mes cookies » dans le pied de page (rouvre le bandeau).
- Accueil immersif (11/11/2026, préversion) : vidéo plein écran sous un menu transparent (logo et liens en blanc) ; le menu redevient opaque dès qu'on défile ; à l'arrivée directe sur l'accueil, la vidéo s'affiche seule avec un indice de défilement, puis le contenu du hero apparaît au premier défilement, toucher ou clic, ou après 2,5 s de vidéo en lecture (6 s au plus si elle tarde) ; bouton flottant et bulle WhatsApp apparaissent avec lui. Désactivé si l'utilisateur demande moins d'animations.
- Menu transparent sur les cinq pages du menu (11/11/2026) : accueil, Rio, Itacaré, Pour qui, À propos ; la photo ou la vidéo passe sous le menu, qui reste transparent jusqu'à ce que le titre (H1) du hero l'atteigne. Sur l'accueil, le titre s'affiche tout de suite (élément mesuré par Google pour le LCP) ; seuls le sous-titre, le formulaire et les boutons attendent.
- Vidéos ordinateur allégées (11/11/2026) : `videos/hero-*-ordi.mp4` (accueil et Itacaré en 1600×900 à 2 Mb/s, 4,8 et 4,4 Mo au lieu de 14,6 et 13,3 ; Rio 2,9 Mo au lieu de 5,4) ; image d'attente de l'accueil préchargée en priorité.
- Tunnel (11/11/2026) : bouton ✕ retiré ; le logo ramène à l'accueil (sélection conservée ; après envoi, le tunnel repart de zéro).
- robots.txt (11/11/2026) : exploration autorisée pour tous les robots et outils d'IA ; la bêta reste hors des moteurs grâce à l'en-tête X-Robots-Tag noindex.

### Branche `refonte-experientielle` (ouverte le 11/11/2026)

Branche de travail pour adapter le site aux idées de la maquette d'un ami développeur (vidéo du 11/11/2026). Elle part de l'état de `corrections-audit-beta` du même jour ; `main` et `corrections-audit-beta` continuent de porter la bêta actuelle. Préversion Vercel : `https://surfinn-beta-git-refonte-experientielle-surf-inn.vercel.app`.

Pistes retenues de la maquette :
- Accroche immédiate : la marque en très grandes lettres sur la vidéo, une phrase, rien d'autre.
- Couleurs franches par grands aplats (jaune soleil, bleu-vert profond, blanc cassé) et une typographie de titre plus affirmée.
- Aller à l'essentiel : moins d'informations, une page qui donne envie, un contact simple (téléphone, e-mail).
- Réserver en moins de 30 secondes et en 3 clics : module de réservation intégré à la page (formule, jour, horaire, nombre de personnes, prix affiché, bouton).
- « Choisissez votre plage » : les spots sur une carte, un clic pour réserver.
- La première leçon en 3 étapes, une FAQ courte, un appel final (« Bora surfar ? »).
- Navigation par sections avec un indicateur de progression en bas d'écran.

Différence à garder en tête : la maquette vend des cours à la journée ; Surf Inn vend surtout des séjours (hébergement + package), sur deux destinations.

#### Premier essai (11/11/2026)
- Polices Londrina Solid (titres) et Chivo (texte), chargées depuis Google Fonts.
- Couleurs « surf » : soleil `#FFC531`, mer `#0B6A73`, encre `#06323B`, bouée `#F2542D`, écume `#F2F8F6` ; sections teintées en aplats jaune soleil, boutons jaunes à texte encre.
- Accueil : « SURF INN » en très grandes lettres sur la vidéo, le H1 juste dessous.
- La marée : vague fixe en bas d'écran ; la planche avance avec le défilement, chaque titre de section est une bouée cliquable, le nom de la section en cours s'affiche sous la planche ; bouton flottant, bulle WhatsApp et pied de page remontent au-dessus.
- Couche appliquée uniquement quand la reconstruction tourne sur cette branche (script `corrections_refonte.py`).
- Menu flottant mobile (11/11/2026) : une fois la photo passée, plus de fond derrière le menu ; le logo s'efface au défilement ; le bouton menu devient une pastille ronde flottante ; sur Rio et Itacaré, la barre d'onglets monte tout en haut, la pastille à son extrémité.
- Fusion des barres (11/11/2026) : sur Rio et Itacaré, quand la barre d'onglets atteint le haut, le menu principal s'efface (ordinateur) et la barre d'onglets prend sa place avec le logo de la maison et « Rio de Janeiro » / « Itacaré » à gauche ; sur mobile, logo à gauche, pastille du menu à droite.
- Physique de la planche (11/11/2026), reprise de la maquette : deux houles qui voyagent en sens contraire (la mer bouge seule), planche qui rattrape le défilement avec inertie (accélère puis ralentit), se cabre selon sa vitesse, sillage qui s'éclaire avec la vitesse, petit coup de rame en haut de page.

### Branche `refonte-synthese` (11/11/2026)

Synthèse de `refonte-experientielle` (base) et des derniers correctifs de `main` (apparition du hero, `llms.txt`), plus une couche expérientielle. Arbitrages dans `DECISIONS.md`.

- Couche expérientielle : sources dans `outils/experience/` (`couche.css`, `couche.js`, `stickers.json`), posée par `python3 outils/experience.py` entre `extraire` et `empaqueter` (idempotent). Elle ne s'active que si le script tourne (`html[data-exp]`) et respecte « réduire les animations ».
- « Le Brésil, c'est… » : aplat encre, mots géants, pellicule de photos à faire glisser, stickers.
- « Pourquoi Surf Inn existe » : aplat soleil, photo qui se pose et texte qui s'éclaire au défilement.
- Révélation au défilement des titres de section et des cartes.
- Piège supplémentaire du moteur de gabarit : `viewBox=` dans un SVG en `data:` est réécrit lui aussi (contourné dans `experience.py`).
