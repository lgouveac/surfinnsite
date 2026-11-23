# Direction 4 : « Chaleur » (retours de Lucas)

Branche `refonte-chaleur`, ouverte le 13/11/2026 à partir de `refonte-maison`, après la réunion Kévin / Lucas du 12/11/2026.

Constat de la réunion : la nouvelle direction est plus vivante et convertira mieux que la version initiale, mais la police serif fait « journal », le bleu-vert refroidit le site, la bande du bas fait enfantin et on ne voit pas assez de gens.

## Ce qui change par rapport à Maison

| Point de la réunion | Ce qui est fait |
|---|---|
| Bande du bas (planche, « Fais défiler pour surfer ») | Retirée partout. |
| Le surf dans le tunnel | La planche avance d'étape en étape sur une ligne d'eau, à la place des barres. |
| Police des titres | Gabarito (linéale ronde, grasse), tailles ramenées : 54 px au plus sur ordinateur, 34 px sur mobile. La serif Fraunces ne reste que sur les cartes photo de « Le Brésil, c'est… ». |
| Site trop froid | Le bleu-vert devient un vert profond (`#0C3B32`), le fond un crème chaud (`#F7F4EA`), les accents un vert plus franc. Le jaune ne bouge pas. |
| Survol de « Créer mon séjour » | Du jaune au vert (`#4BC68F`, vif et un peu pastel), avec une petite tong qui apparaît au bout du bouton. |
| Tong | Au survol du bouton principal, et une fois dans « Le Brésil, c'est… ». Nulle part ailleurs. |
| Preuve sociale | Nouvelle section « Le quotidien à Surf Inn » juste sous l'en-tête de l'accueil : douze photos de voyageurs, de moniteurs et de l'équipe, grille simple, sans effet. |
| Photos des deux camps (accueil) | Inchangées : Recreio vu du ciel et Itacaré avec la forêt (essai avec la cour du Surf Club et la façade de Bahia annulé à la demande de Kévin). |
| Pilier « Belong » | Retour de la photo du Kombi. En français : « Se retrouver » au lieu de « Se poser ». |
| Pilier « Apprendre » | Deux élèves debout sur la même vague. |
| Clin d'œil brésilien | Masqué quand le site est en portugais (accueil et « Pour qui »), conservé en français et en anglais. |

## Photos ajoutées depuis le Drive

Cinq photos du dossier `Téléchargements Mac/Foto & Video/Surf` (fichiers « Beginner Classes » et « Surf Group », 6000 × 4000), copiées dans `assets/drive-*.jpg` : une pour « Apprendre », quatre dans la galerie. **À confirmer par Kévin ou Lucas : ces photos viennent-elles bien de Surf Inn ?** Les lycras sont orange et jaunes, sans logo visible.

Autres dossiers du Drive repérés et non exploités : `SURF IN RIO` (55 photos), `Surf In Rio - Maio 2025 2` (91), `Vídeos e fotos` (181, dont 80 de chambres).

## Non fait

- Formulation « Tu parles portugais ? » proposée par Lucas pour le clin d'œil : gardé « Brésilien ? ».
- « Pourquoi voyager au Brésil » pour un public brésilien : pas de décision en réunion.
- Vidéo d'en-tête : montage.
- Photos de téléphone de Lucas, pistes de polices de Lucas : à intégrer quand elles arrivent.

## Couleurs d'action et planche du tunnel (13/11/2026)

- **Deux logiques de couleur, par camp.** Rio et le reste du site : sélection en vert (`--accent`), bouton principal jaune qui passe au vert au survol. Itacaré, page et tunnel : sélection et bouton principal en orange. Les variables sont `--accent`, `--accent-fond`, `--principal`, `--principal-texte`, `--principal-survol`.
- **Plus de rouge ni de bleu de l'ancienne charte.** Tunnel (cartes choisies, pastilles « Choisi », bouton « Continuer », cases à cocher, survols), onglets des pages camp, pastilles, bordures, textes sur fond sombre. Contrôlé par `audit/retours/anciennes.mjs` (douze pages et le tunnel des deux camps) et `audit/retours/rouge.mjs`. Restent volontairement : les étoiles des avis (ocre) et le sous-titre pêche des en-têtes.
- **Planche du tunnel.** Une seule planche qui glisse en 1,7 s d'une étape à l'autre, se cabre pendant le trajet et laisse un sillage, puis reprend son balancement. Code : `etapes()` dans `couche.js`.
