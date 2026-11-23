# Surf Inn · beta site

*English translation of `README.md` (20/11/2026). The French file is the reference; if the two ever differ, trust `README.md`. File, folder, function and command names are left as they are in the code, which is in French: `outils` = tools, `paquet` = package, `extraire` = extract, `empaqueter` = pack, `travail` = work, `gabarit` = template, `textes` = texts, `ordi` = desktop, `couche` = layer, `repère` = marker.*

This repository contains the website of Surf Inn, two surf camps in Brazil (Rio de Janeiro and Itacaré, Bahia), in English, French and Portuguese. It is published on Vercel at `https://surfinn-beta.vercel.app`, with no password but hidden from search engines. This document is written for the people taking over the site for the production launch and the backend (Flowcode); the detailed change log is at the bottom, in the "History" section.

The long-term target is the Astro site `surfinnrio/surfinn-site`. This repository is the reference version in the meantime.

## How the site is built

`index.html` is a **bundled file** (the "bundler" format inherited from Claude Design, which has not been used since 09/11/2026). It is never edited by hand: the HTML and all of the site's React code live in the `<script type="__bundler/template">` block, as a JSON string; the translations, the rendering engine and a few stylesheets live in the `<script type="__bundler/manifest">` block, in base64 (sometimes gzip-compressed). A small loader at the top of the page decodes everything in the browser. Images are served separately from `assets/` (the `__bundler/external` block maps an identifier to a path), and videos from `videos/`.

`index.html` remains the single source of truth: the tools in `outils/` decode it, modify it and write it back.

### Build chain

Python 3 is enough, with no dependency. From the repository root:

```bash
python3 outils/paquet.py extraire     # decodes index.html into .travail/ (gabarit.html + textes/), a disposable folder ignored by git
python3 outils/experience.py          # applies the layers and fixes inside .travail/
python3 outils/paquet.py empaqueter   # rewrites index.html from .travail/
python3 outils/images_mobiles.py      # only after adding or replacing a photo in assets/ (needs Pillow)
```

Then commit and push. Vercel redeploys on its own.

- `paquet.py extraire` writes `.travail/gabarit.html` (the HTML template and the site code) and `.travail/textes/<uuid>.<ext>` (`i18n` translations, rendering engine, CSS, decompressed).
- `experience.py` modifies `.travail/gabarit.html` and the translations file in `.travail/textes/`. It is designed to be re-run on an already built `index.html`: the CSS and JS layer is rewritten between the markers `<!-- couche-experience:debut -->` and `<!-- couche-experience:fin -->`, and each replacement only applies if its result is absent. It stops with a message when an expected marker is missing or ambiguous, and rejects some known template-engine errors (see the pitfalls below).
- `paquet.py empaqueter` re-encodes the template and the texts into `index.html`. A change made directly in `.travail/gabarit.html` (without going through `experience.py`) is therefore kept: it goes into `index.html` and will be read as is at the next extraction.

- `images_mobiles.py` produces the reduced versions of the photos (`assets/m/<name>-480|720|960.webp`) and places, in the `<head>` of `index.html` between `<!-- images-mobiles:debut -->` and `<!-- images-mobiles:fin -->`, the script that serves them to screens of 900 px or less (srcset and actual displayed size). Desktop and the full-screen gallery keep the original photos. `empaqueter` does not touch this script; it only needs to be re-run when photos change (otherwise a new photo is simply served at its original size).

The other scripts in `outils/`:

- `outils/experience/` contains the sources of the layer applied by `experience.py`: `couche.css`, `couche.js`, `maison.css`, `mobile.css` (mobile rules, see `REGLES-MOBILE.md`) and `stickers.json`. They are re-read on every run.
- `echelle.py`, `activites.py` and `legal.py` are not run on their own: they are modules imported by `experience.py`, so **they are replayed on every build**. `echelle.py` reduces text sizes to nine values, `activites.py` holds the activity descriptions in the three languages, `legal.py` the content of the legal pages (legal notice, privacy, booking terms, to be validated by a lawyer before launch). Beware of the exception described below for `legal.py`.
- `retours_ami.py` (with `retours_ami.css`) is a **one-off**: it was run once on 12/11/2026 and its result is already in `index.html`. Do not run it again.
- `paquet.py externaliser` is a one-off operation, already done: it moved the images out of the manifest into `assets/`.

### Known pitfalls

- **camelCase followed by ` =`**: inside a `<script>` of the template, the template engine rewrites a camelCase variable followed by ` =` as if it were an attribute (`fooBar =` becomes `sc-camel-foo-bar =`). Use names without capitals (`foo_bar`). `experience.py` rejects this pattern in `couche.js`.
- **`viewBox=`**: in a `data:` SVG, `viewBox=` is rewritten the same way. `experience.py` works around it by encoding the `B` (`view%42ox`).
- **`{{` in the layer's stylesheets and scripts**: forbidden, the engine would treat it as a variable. `experience.py` stops if it finds one.
- **Blocks guarded by a test**: some blocks of `experience.py` only run if their result is absent from the template (for example the legal pages, `if "legal: { en: 'legal/'" not in s`). Since the template is already built, they are not replayed: editing `legal.py` does not change the site. You need to add to `experience.py` an explicit replacement of the old text with the new one.
- **Indented zone before "Lot vocabulaire"**: the place where batches of fixes are usually added, just before the line `    # Lot vocabulaire (17/11/2026, option A`, is inside a large block indented by 4 spaces (`if os.path.exists(mobile):`). Any code added there must be indented by 4 spaces; otherwise the rest of the file becomes the body of the last `if` added, which works by chance and then breaks.
- **Names already taken**: before adding a field to a camp's object, check that the name does not already exist further down (that was the case for `expIntro`); the last key wins.
- **Palette**: at the end of `experience.py`, colours are converted across the whole template, stylesheets included. A colour written in `mobile.css` can therefore be changed during the build.
- **Useful check** after a big change: start again from an older `index.html` (`git checkout <commit> -- index.html`), re-run the whole chain and compare with the current result.

### Analytics and cookies

- Google Tag Manager: container `GTM-WH4MTLKG`, placed in the template. It carries Google Analytics, Microsoft Clarity and the site events sent to `dataLayer` (`virtual_page_view`, `funnel_open`, `generate_lead`, `share_click`, `share_visit`). **The container is not published**: this is intentional, so beta traffic is not mixed with the current site's traffic.
- Cookiebot (ID `4b033d94-b9f9-4c38-b4ff-26b90636072e`) is **switched off** by the flag `COOKIEBOT_ACTIF = False` in `outils/experience.py`, because the site targets Brazil first. When off, there is no banner, Google consent (Consent Mode v2) is granted by default and the "Manage my cookies" link is hidden. To turn it back on: set `True`, re-run the build chain. The Cookiebot code is still in place. To be reconsidered as soon as the site targets Europe (ideally by showing the banner to European visitors only).

## Files at the root

- `index.html`: the whole site, bundled (see above).
- `assets/`: images, named by hash, served with a one-year cache.
- `videos/`: the opening (hero) videos of the pages, in two versions. The loader picks `videos/hero-<page>-mobile.mp4` when the short side of the screen is under 600 px and `videos/hero-<page>-ordi.mp4` otherwise (variable `heroMobile` at the top of `index.html`), for the home page, Rio and Itacaré.
- `vercel.json`: Vercel configuration. It adds the header `X-Robots-Tag: noindex, nofollow` to every response, caches images, enforces the trailing slash in URLs, redirects `/en/…` to the root and `/surf-camp/` to the home page, and rewrites every page URL to `index.html` (the site itself picks the page and language from the URL).
- `middleware.js`: Vercel function run before every page (not for images, videos or files). It injects into the HTML sent the title, description and sharing tags (Open Graph, Twitter) specific to the requested URL, so that WhatsApp, Instagram or iMessage previews work without running the site. Since 18/11/2026 it also writes into the raw page the canonical, the hreflang tags (en, fr, pt, x-default = English) and, on camp pages, the breadcrumb in JSON-LD (`script#fil-ariane`), with the same attributes as the site's JavaScript, which updates them without duplicates. The URL mappings between languages are in its `PAGES` and `ONGLETS` tables: keep them in sync with the site's `ROUTES`/`ONGLETS` and the language script at the top of `index.html`. It computes a weak ETag (index.html + injected text) and answers 304 when nothing has changed, with `Cache-Control: public, max-age=0, must-revalidate`. It sets the security headers (constant `SECURITE`, to keep identical to `vercel.json`) and the `noindex` header. It no longer uses a country cookie: `surfinn_country` has not been set since 18/11/2026.
- `seo.js`: the titles and descriptions of every URL, in the three languages (`t` and `d` for the browser tab and Google, `st` and `sd` for share previews, `i` for the share image). It is read by `middleware.js` on the server, and copied into the template by `experience.py` for the browser: after changing `seo.js`, re-run the build chain.
- `sitemap.xml`: the list of the site's 60 URLs with their equivalents in the other languages (`hreflang`).
- `llms.txt`: the site's text page by page, for AI tools, because the site is rendered in JavaScript.
- `robots.txt`: allows crawling by all robots. Indexing is prevented by the `noindex` header, not by this file.
- `package.json` and `package-lock.json`: a single dependency, `@vercel/functions` (used by `middleware.js`), and Node 20 or later, the minimum version it requires. There is no build step on Vercel.
- `DECISIONS.md`, `DIRECTION-MAISON.md`, `DIRECTION-CHALEUR.md`, `REGLES-MOBILE.md`, `PHOTOS-A-FOURNIR.md`: design notes in French (trade-offs, visual directions, mobile rules, photos to redo).

URLs follow the pattern `/surf-camp/<destination>/<tab>/` for camp pages and `/about-us/`, `/reviews/`, `/faq/`, `/contact/`, etc. for the others; English is at the root, French under `/fr/` and Portuguese under `/pt/`, with translated URLs. The old `fr/`, `pt/` and `en/` folders have been removed.

Not versioned (see `.gitignore`): `.travail/`, and the working folders `audit/`, `maquettes/`, `mesure/` and the archive `audit-usabilite-beta-20261109.zip`, which only exist on Kévin's computer. References to `audit/…` in the history below therefore point to files that are not in the repository.

## Before going to production (Flowcode)

1. **Connect the forms.** Today, neither the booking funnel nor the contact form sends anything: on submit, the component state simply switches to `submitted: true` (funnel) or `contactSent: true` (contact), with no network request, and the visitor sees the thank-you screen. The backend is entirely to be built. A comment in the template already describes the intended shape of the funnel data (search for `visitsurfinn.com custom package` in `.travail/gabarit.html`).
2. **Remove the `noindex`** in two places: the header in `vercel.json` (block `"source": "/(.*)"`) **and** the line `h.set('X-Robots-Tag', 'noindex, nofollow')` in `middleware.js` (response function, next to the `SECURITE` constant). Removing one without the other leaves the pages hidden.
3. **Change the domain in `sitemap.xml` and `llms.txt`**, which both point to `https://surfinn-beta.vercel.app`.
4. **Pin the canonical URLs to `https://www.visitsurfinn.com`.** The site code currently builds `canonical`, `hreflang` and `og:url` from `location.origin` (in the browser) and from the request origin (in `middleware.js`, function `domaine(url)`, to be replaced with `https://www.visitsurfinn.com`): on a preview or on the Vercel domain, they would point to the wrong address.
5. **Publish the Tag Manager container `GTM-WH4MTLKG`** on launch day, not before (as long as it is not published, nothing is measured: this is intentional, so beta traffic is not mixed in). It already carries Google Analytics (`G-J9J8RM4DX3`), Microsoft Clarity (`zfoewm9k5t`) and the site events. Access: Surf Inn's Google account (ask Kévin). Right after publishing:
   - check that Google Analytics real-time and Clarity recordings receive visits on `www.visitsurfinn.com`;
   - in Google Analytics, mark the `generate_lead` event (request sent) as a key event, so requests count as conversions.
6. **Redirects of the old Framer URLs: in place in `vercel.json` (23/11/2026).** The 11 redirects of the `REDIRECTIONS.xlsx` plan are set. The blog is not redirected: both articles are kept at the same URLs (`blog/`, static pages generated by `python3 outils/blog.py` from `outils/blog/`), except the article whose URL had an em dash, redirected to the same URL without it. Sources end with a slash: with `trailingSlash`, Vercel adds the slash before applying redirects, hence two hops (308 to `/old/`, then 308 to the final page), checked on the preview. Still to do after the switch: test each old URL ("Vérifications" tab).
7. **Images from `framerusercontent.com`: brought into `assets/` (23/11/2026)**, `FRAMER` table in `outils/experience.py` (the build stops if a Framer URL comes back).
8. Also check: the domain declared in Cookiebot (only `surfinn-beta.vercel.app` is) if it is turned back on, and the legal review of the legal pages (`outils/legal.py`).
9. **Every time a photo is added or replaced in `assets/`, run `python3 outils/images_mobiles.py`** (needs Pillow: `pip3 install Pillow`), then commit `assets/m/` and `index.html`. This script produces the reduced versions served to phones. Without it nothing breaks, but the new photo is sent to phones at its original size. Careful: a photo replaced **under the same name** stays cached for a year in visitors' browsers (`Cache-Control: immutable` on `/assets/`); give a new name to any modified photo.

The repository weighs about 400 MB, mostly because of the roughly 200 successive versions of `index.html` (2.3 MB each) kept in the git history. If the size is a problem, the history can be rewritten (for example with `git filter-repo`) or a fresh repository can be started with only the current state; this has not been done here, because it changes every commit identifier and forces everyone to re-clone.

## History

What follows is the change log kept during the beta, from oldest to newest, kept as is apart from two corrections (marked in square brackets). Details of the redesign branches are in `DECISIONS.md`, `DIRECTION-MAISON.md`, `DIRECTION-CHALEUR.md` and `REGLES-MOBILE.md` (in French).

### Compared with the Claude Design export (09/11 to 11/11/2026)

`index.html` is a bundled file: the texts and code are in the `__bundler/template` block (JSON text), the translations in the `i18n.js` file encoded in the `__bundler/manifest` block.

- `detectLang()`: goes through all the browser's languages (`navigator.languages`) and keeps the first one available among `en`, `fr`, `pt`.
- `isBrazilian()`: returns true only if the `surfinn_country` cookie equals `BR`. This cookie is set by `middleware.js` from the country detected by Vercel. [Outdated: the Brazilian pop-up was removed and the `surfinn_country` cookie has not been set since 18/11/2026.]
- Videos: the 3 WebM files were removed from the manifest; the page loads `/videos/hero-accueil.mp4`, `/videos/hero-rio.mp4` and `/videos/hero-itacare.mp4` (MP4 H.264, 30 fps). [Outdated: these three files were replaced by the `-ordi` and `-mobile` versions described below, then removed from the repository on 18/11/2026.]
- Lucas's feedback (v18, 09/11): `i18n.js` translations v18, 61 fixes to the English, 40 boards including 20 by Baltazar, empty Rio tagline in PT, Brazilian pop-up at the bottom of the screen.
- Booking funnel (export `standaloneV20261109b`, the last Claude Design export): Trip, Stay (room type only) and Package steps redone, triple room in Itacaré, "Surf Inn" fixed in package names. Merged with v18; the funnel line in PT also says "(depois do surf)".
- Fixes from the usability audit of 09/11/2026 (`audit/plan-corrections-20261109.md`): images moved out of the file (20.5 MB → 1.9 MB), loading screen translated, `<title>` per language, clickable elements reachable by keyboard with visible focus, WhatsApp bubble as an icon on mobile and hidden in the funnel (and when it would cover a button), hero button that always opens the funnel, camp mandatory at step 1 and preselected from a camp page, scroll hint on the mobile tab bar, 44 px −/+ buttons, "quick reply" delay everywhere, single label for the mobile button, prefilled WhatsApp messages translated, singular and PT date in the summary, wifi FAQ link, Rio "fast wifi" in FR/PT, named Instagram links, Framer image removed, neutral phone number example in EN, duplicated reassurance removed.
- Lucas's feedback (09/11/2026): one WhatsApp number per camp (Rio +55 21 99923-1992, Itacaré +55 73 99825-7683; when no camp is known, Rio), packages renamed (Surf In Rio, Onda Carioca, Surf Intensive; Surf In Bahia, Onda Baiana, Surf Intensive), lessons in Itacaré at 8 am.
- Kévin's mobile feedback (10/11/2026): hero of the home, "Who is it for" and "About" pages moved up or centred on mobile; "Create my stay" bar turned into a floating button next to the WhatsApp icon, hidden when the menu is open; camp card headers on one line; "Our concept / Notre concept / Nosso conceito" menu; texts of the 4 pillars, of "Brazil is…", of "Who is it for" and of "About" rewritten in the 3 languages; "within 24h" removed from camp, Who is it for and About pages in FR and PT; provisional quote from Lucas removed; roles of Igor (surf camps manager) and Kévin (marketing and strategy).
- iPhone fix (10/11/2026): fields at 16 px on mobile (Safari zoomed in on 15 px fields and the page then shifted sideways); calendar centred on screen on mobile, over a darkened background.
- Feedback of 10/11/2026 (continued): funnel without a preselected camp, camp and dates required at step 1 (or "dates not set yet"); home page texts (in front of the waves, Learn and Unwind pillars, "Brazil is play"); roles of Lucas (founder and manager of Surf Inn Rio) and Igor (manager of Surf Inn Bahia).
- Funnel (10/11/2026): Accommodation step in Rio without the top description; the screen scrolls down to the room list after choosing private/shared; a greyed "Continue" takes you to what is missing (camp, dates, room, email); summary banner removed from the Package, Options and Contact details steps.
- Rio and Itacaré pages, mobile (10/11/2026): tab bar arrows centred, on the left once scrolled, hidden at the end; Rio overview texts; reviews shown in full (no more "Read more"); activity tiles not clickable on mobile; real logo in the Instagram block; gallery: arrows under the photo on mobile, fixed background, photos preloaded, duplicate removed; boards pop-up without the blue box; Packages tab without the final "Create my stay" block.
- Funnel and home (10/11/2026): left margin restored on the package row; summary as lines (one item per line, "Edit" next to the title); short final page, without the accommodation note or Lucas's video; home camp photos not clickable on mobile; "Brazil is…": the 4 words on one line and the sentence for Brazilians under the cards, on mobile.
- Home hero and footer (10/11/2026): no more blue outline when tapping the Destination and Dates fields; on mobile, Destination, Dates and Travellers fields in frosted glass (the video shows through); spaces restored in "★ 4.9 · 438 Google reviews" in the footer.
- Camp pages, continued (10/11/2026): "Your stay" photos not clickable on mobile; reviews subtitle removed; photo galleries usable by swiping; "Common areas" and "Rooms" cards reduced to one photo on mobile to fit the screen; "Waterfall hike" in the packages and floating button hidden on the Packages tab; no more "des gens d'ici" in French; tab bar arrows in green on Itacaré.
- Google Maps on demand (10/11/2026): on camp pages, a preview (camp name, "Show the map" button, "Open in Google Maps" link) replaces the map until it is requested. Fewer Google scripts, lighter pages, no more Google errors when changing page during loading.
- Batch of 10/11/2026 (evening): hero fields in translucent white without blur; closing galleries without jumping back to the top; arriving on a camp page from the menu as on a first visit (Overview tab, tab bar at the start); Instagram with 4 photos on mobile; "See the photos" badge on camp cards; shorter Baltazar Customs block; funnel: dates without the keyboard, shared room photo for Itacaré, guided "Build my package" (Continue greyed out until something is chosen); "Back to site" goes to the home page.
- Rebuild: a JavaScript syntax check (component, scripts, translations) blocks packing if there is an error.
- Batch of 11/11/2026: home, "Learn" pillar grouped into five bullets (surf, surf guiding and video analysis; Portuguese; percussion with Brazilian rhythms; capoeira; futevôlei and altinha), no more cooking classes; "Our concept" page, tags on the "Explore" card in the same format as the other cards (white background, solid outline).
- Hero videos on phones (11/11/2026): mobile versions `videos/hero-*-mobile.mp4` (centre cropped to portrait at full resolution, H.264 without sound, about 3 times lighter: home 4.7 MB instead of 14.6 MB, Itacaré 4.2 instead of 13.3, Rio 1.9 instead of 5.4), chosen at load time when the short side of the screen is under 600 px. Desktops keep the originals.
- New Rio opening video (20/11/2026): iPhone 4K HDR 60 fps source of 22 s (114 MB), converted to SDR with `avconvert --preset Preset1920x1080` (macOS), then encoded with ffmpeg in H.264 30 fps without sound: `hero-rio-ordi.mp4` in 1280×720 (CRF 30, 5.3 MB) and `hero-rio-mobile.mp4` centre-cropped to 480×720 (CRF 28, 2.8 MB). Same method to replace another video: keep the file names, nothing else to change.
- Autoplay on iPhone (11/11/2026): videos get a real `muted` attribute (React does not write it, which stops iOS Safari from starting the video on its own and shows a play button), playback is restarted as soon as possible and on the first touch (low power mode), and the native iOS play button is hidden.
- Consent and tracking (11/11/2026): Google Consent Mode v2 placed at the top of the page, everything denied by default; slots for Cookiebot (loaded without blocking the page, manual blocking, visitor's language) and Google Tag Manager (empty until the IDs are provided: no call to Google, Meta or Cookiebot); events sent to `dataLayer` for GTM: `virtual_page_view` (the site changes page without changing URL), `funnel_open`, `generate_lead` (request sent, with no personal data).
- One URL per page and per language (11/11/2026): structure `/surf-camp/<destination>/<tab>/` (tabs: `accommodation`, `activities`, `packages`, `surf-guide`), service pages at the root (`/about-us/`, `/reviews/`, `/faq/`, `/contact/`, `/who-is-it-for/`), English at the root, `/fr/` and `/pt/` with translated URLs. The URL decides the language; a banner suggests the browser's language, without redirecting. Page title, canonical, reciprocal hreflang with x-default and breadcrumb (JSON-LD) updated on every page; menu, footer and tabs as real `<a href>` links. On Vercel: every page URL rewritten to `index.html`, `/en/…` and `/surf-camp/` redirected, `sitemap.xml` generated. The old `fr/`, `en/`, `pt/` folders are deleted.
- Cookiebot connected (11/11/2026): ID 4b033d94-b9f9-4c38-b4ff-26b90636072e, GDPR preset (explicit consent, "Deny all" button, all visitors), banner in English, French and Brazilian Portuguese, without a floating button; "Manage my cookies" link in the footer (reopens the banner).
- Immersive home (11/11/2026, preview): full-screen video under a transparent menu (logo and links in white); the menu becomes opaque again as soon as you scroll; when landing directly on the home page, the video shows alone with a scroll hint, then the hero content appears on the first scroll, tap or click, or after 2.5 s of video playing (6 s at most if it is slow); the floating button and WhatsApp bubble appear with it. Disabled if the user asks for reduced motion.
- Transparent menu on the five menu pages (11/11/2026): home, Rio, Itacaré, Who is it for, About; the photo or video goes under the menu, which stays transparent until the hero title (H1) reaches it. On the home page, the title shows immediately (the element Google measures for LCP); only the subtitle, the form and the buttons wait.
- Lighter desktop videos (11/11/2026): `videos/hero-*-ordi.mp4` (home and Itacaré in 1600×900 at 2 Mb/s, 4.8 and 4.4 MB instead of 14.6 and 13.3; Rio 2.9 MB instead of 5.4); home poster image preloaded with priority.
- Funnel (11/11/2026): ✕ button removed; the logo goes back to the home page (selection kept; after sending, the funnel starts from scratch).
- robots.txt (11/11/2026): crawling allowed for all robots and AI tools; the beta stays out of search engines thanks to the X-Robots-Tag noindex header.

### Branch `refonte-experientielle` (opened on 11/11/2026)

Working branch to adapt the site to the ideas of a mock-up by a developer friend (video of 11/11/2026). It starts from the state of `corrections-audit-beta` on the same day; `main` and `corrections-audit-beta` keep carrying the current beta. Vercel preview: `https://surfinn-beta-git-refonte-experientielle-surf-inn.vercel.app`.

Ideas kept from the mock-up:
- Immediate hook: the brand in very large letters over the video, one sentence, nothing else.
- Bold colours in large flat areas (sun yellow, deep blue-green, off-white) and a more assertive heading typeface.
- Get to the point: less information, a page that makes people want to come, simple contact (phone, email).
- Book in under 30 seconds and 3 clicks: booking module built into the page (formula, day, time, number of people, price shown, button).
- "Choose your beach": the spots on a map, one click to book.
- The first lesson in 3 steps, a short FAQ, a final call ("Bora surfar?").
- Section-based navigation with a progress indicator at the bottom of the screen.

Difference to keep in mind: the mock-up sells day lessons; Surf Inn mainly sells stays (accommodation + package), in two destinations.

#### First attempt (11/11/2026)
- Fonts Londrina Solid (headings) and Chivo (body), loaded from Google Fonts.
- "Surf" colours: sun `#FFC531`, sea `#0B6A73`, ink `#06323B`, buoy `#F2542D`, foam `#F2F8F6`; sections tinted in flat sun yellow, yellow buttons with ink text.
- Home: "SURF INN" in very large letters over the video, the H1 just below.
- The tide: fixed wave at the bottom of the screen; the board moves forward with scrolling, each section title is a clickable buoy, the current section name shows under the board; floating button, WhatsApp bubble and footer move up above it.
- Layer applied only when the rebuild runs on this branch (script `corrections_refonte.py`).
- Floating mobile menu (11/11/2026): once past the photo, no more background behind the menu; the logo fades out on scroll; the menu button becomes a round floating badge; on Rio and Itacaré, the tab bar moves to the very top, with the badge at its end.
- Merged bars (11/11/2026): on Rio and Itacaré, when the tab bar reaches the top, the main menu fades out (desktop) and the tab bar takes its place with the house logo and "Rio de Janeiro" / "Itacaré" on the left; on mobile, logo on the left, menu badge on the right.
- Board physics (11/11/2026), taken from the mock-up: two swells travelling in opposite directions (the sea moves on its own), a board that catches up with scrolling with inertia (speeds up then slows down), tilts according to its speed, a wake that brightens with speed, a small paddle stroke at the top of the page.

### Branch `refonte-synthese` (11/11/2026)

Synthesis of `refonte-experientielle` (base) and the latest fixes from `main` (hero appearance, `llms.txt`), plus an experiential layer. Trade-offs in `DECISIONS.md`.

- Experiential layer: sources in `outils/experience/` (`couche.css`, `couche.js`, `stickers.json`), applied by `python3 outils/experience.py` between `extraire` and `empaqueter` (idempotent). It only activates if the script has run (`html[data-exp]`) and respects "reduce motion".
- "Brazil is…": flat ink background, giant words, a strip of photos to swipe, stickers.
- "Why Surf Inn exists": flat sun background, a photo that lands and text that lights up on scroll.
- Scroll reveal of section titles and cards.
- Additional template-engine pitfall: `viewBox=` in a `data:` SVG is rewritten too (worked around in `experience.py`).
