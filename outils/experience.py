#!/usr/bin/env python3
"""Pose la couche expérientielle dans .travail/gabarit.html (à lancer entre « extraire » et « empaqueter »).

    python3 outils/paquet.py extraire
    python3 outils/experience.py
    python3 outils/paquet.py empaqueter

Idempotent : la couche est réécrite entre ses deux repères. Sources : outils/experience/couche.css, couche.js,
et les stickers de outils/experience/stickers.json (dessins de la série Brésil du 11/11/2026).
"""
import json, os, re, sys, urllib.parse

ICI = os.path.dirname(os.path.abspath(__file__))
GAB = os.path.join(os.path.dirname(ICI), '.travail', 'gabarit.html')
DEBUT, FIN = '<!-- couche-experience:debut -->', '<!-- couche-experience:fin -->'
FILTRE = ('<filter id="d" x="-20%" y="-20%" width="140%" height="140%"><feMorphology in="SourceAlpha" operator="dilate" radius="5" result="d"/>'
          '<feFlood flood-color="#fff"/><feComposite in2="d" operator="in" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')


def uri(corps):
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><defs>' + FILTRE + '</defs>' + corps.replace('url(#decoupe)', 'url(#d)') + '</svg>'
    return 'url("data:image/svg+xml,' + urllib.parse.quote(re.sub(r'\s+', ' ', svg), safe="/:=' ,.()-").replace('viewBox', 'view%42ox') + '")'  # « viewBox= » serait réécrit par le moteur de gabarit


def remplace(s, avant, apres, n=1):
    if apres in s:
        return s
    if s.count(avant) != n:
        sys.exit(f'Repère introuvable ou ambigu ({s.count(avant)}×) : {avant[:70]}')
    return s.replace(avant, apres)


# Photos de la branche refonte-chaleur (uuid des images déjà présentes ; chemins /assets/… pour les nouvelles)
PHOTO_RIO = 'a253b5c9-0275-448e-ab43-06117c3e13ad'   # cour du Surf Club, les planches au mur
PHOTO_ITA = 'b973596c-088b-442f-85c4-ffde153fc07a'   # façade et jardin de Surf Inn Bahia
VRAIES = [
    ('/assets/drive-cours-tape.jpg', 'Surf lessons', '50% 40%'), ('carte-6-accolade-HOS007.webp', 'Guests and team together', '50% 35%'),
    ('cta-about-1-recommande-groupe-pedra-FV038-s-c.webp', 'Guests and team together', '50% 50%'), ('ph-rd-popup-m.webp', 'Pop-up practice on the sand', '50% 50%'),
    ('capoeira-group-c.webp', 'Guests and team together', '50% 40%'),
    ('/assets/drive-groupe-planches.jpg', 'Guests and team together', '50% 60%'), ('carte-4-table-HOS012-c.webp', 'Breakfast at the big table', '50% 60%'),
    
    ('/assets/drive-cours-plage.jpg', 'Surf lessons', '35% 40%'), ('/assets/drive-cours-sable.jpg', 'Pop-up practice on the sand', '50% 45%'),
]
s = open(GAB, encoding='utf-8').read()
if DEBUT in s:
    s = s[:s.index(DEBUT)] + s[s.index(FIN) + len(FIN) + 1:]

# Repères posés dans le gabarit (attributs seulement, aucun texte modifié)
s = remplace(s, '<!-- MEET LUCAS: photo + short story + pull quote, then a team photo and a video block -->\n  <section style="',
             '<!-- MEET LUCAS: photo + short story + pull quote, then a team photo and a video block -->\n  <section data-pourquoi="1" style="')
s = remplace(s, '<div style="position:relative;border-radius:24px;overflow:hidden;aspect-ratio:4/5;background:#C9DAE3;">\n        <img src="2c5f9b6e',
             '<div data-pourquoi-photo="1" style="position:relative;border-radius:24px;overflow:hidden;aspect-ratio:4/5;background:#C9DAE3;">\n        <img src="2c5f9b6e')
s = remplace(s, '<p style="font-size:18px;line-height:1.65;color:#33566E;margin:0 0 26px;text-wrap:pretty;">Lucas started Surf Inn',
             '<p data-pourquoi-texte="1" style="font-size:18px;line-height:1.65;color:#33566E;margin:0 0 26px;text-wrap:pretty;">Lucas started Surf Inn')
s = remplace(s, '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr));gap:16px;">\n        <sc-for list="{{ aboutPillars }}"',
             '<div data-piliers="1" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr));gap:16px;">\n        <sc-for list="{{ aboutPillars }}"')

s = remplace(s, '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px;">\n        <sc-for list="{{ verbs }}"',
             '<div data-verbes="1" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px;">\n        <sc-for list="{{ verbs }}"', 2)
s = remplace(s, 'gap:20px;">\n      <sc-for list="{{ whoBlocks }}"', 'gap:20px;" data-profils="1">\n      <sc-for list="{{ whoBlocks }}"')
# Pages camp et équipe
s = remplace(s, '<div data-hscroll="1" style="max-width:1240px;margin:clamp(36px,5vw,56px) auto 0;display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:18px;">\n      <sc-for list="{{ camp.whyCards }}"',
             '<div data-hscroll="1" data-chiffres="1" style="max-width:1240px;margin:clamp(36px,5vw,56px) auto 0;display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:18px;">\n      <sc-for list="{{ camp.whyCards }}"')
s = remplace(s, 'gap:18px;margin-bottom:30px;">\n        <sc-for list="{{ camp.methodPoints }}"', 'gap:18px;margin-bottom:30px;" data-methode="1">\n        <sc-for list="{{ camp.methodPoints }}"')
s = remplace(s, 'gap:8px;">\n        <sc-for list="{{ camp.realDays }}"', 'gap:8px;" data-quotidien="1">\n        <sc-for list="{{ camp.realDays }}"')
s = remplace(s, 'gap:16px;">\n        <sc-for list="{{ team }}"', 'gap:16px;" data-equipe="1">\n        <sc-for list="{{ team }}"')
# Onglets des pages camp (Le camp, Expériences, Packages surf)
s = remplace(s, 'gap:18px;margin-top:32px;">\n            <sc-for list="{{ camp.stay.unitCards }}"', 'gap:18px;margin-top:32px;" data-lieux="1">\n            <sc-for list="{{ camp.stay.unitCards }}"')
s = remplace(s, 'margin-top:6px;">\n            <sc-for list="{{ camp.shaper.facts }}"', 'margin-top:6px;" data-faits="1">\n            <sc-for list="{{ camp.shaper.facts }}"')
s = remplace(s, 'height:clamp(260px,30vw,380px);">\n          <sc-for list="{{ camp.shaper.shots }}"', 'height:clamp(260px,30vw,380px);" data-tirages="1">\n          <sc-for list="{{ camp.shaper.shots }}"')
s = remplace(s, 'margin:0 0 14px;">\n            <sc-for list="{{ camp.included }}"', 'margin:0 0 14px;" data-inclus="1">\n            <sc-for list="{{ camp.included }}"')
s = remplace(s, 'margin:0 0 14px;">\n            <sc-for list="{{ camp.onDemand }}"', 'margin:0 0 14px;" data-inclus="1">\n            <sc-for list="{{ camp.onDemand }}"')
if 'data-forfaits="1"' not in s:  # déjà posé quand le gabarit a été construit (la carte n'est plus cliquable depuis le 20/11/2026)
    s = remplace(s, 'gap:16px;margin-bottom:14px;">\n        <div sc-camel-on-click="{{ camp.createPack }}"', 'gap:16px;margin-bottom:14px;" data-forfaits="1">\n        <div sc-camel-on-click="{{ camp.createPack }}"')
s = remplace(s, 'gap:16px;margin-bottom:52px;">\n        <sc-for list="{{ lessonSteps }}"', 'gap:16px;margin-bottom:52px;" data-methode="1">\n        <sc-for list="{{ lessonSteps }}"')
# Onglet Guide surf
s = remplace(s, 'gap:14px;margin-bottom:52px;">\n        <sc-for list="{{ camp.seasons }}"', 'gap:14px;margin-bottom:52px;" data-saisons="1">\n        <sc-for list="{{ camp.seasons }}"')
s = remplace(s, 'gap:12px;">\n            <sc-for list="{{ camp.spots }}"', 'gap:12px;" data-spots="1">\n            <sc-for list="{{ camp.spots }}"')
# Aperçu des pages camp : les trois boutons vers Le camp, Expériences et Packages surf, harmonisés
s = remplace(s, '<span sc-camel-on-click="{{ goTabCamp }}" style="cursor:pointer;display:inline-block;', '<span sc-camel-on-click="{{ goTabCamp }}" data-vers-onglet="1" style="cursor:pointer;display:inline-block;')
s = remplace(s, '<span sc-camel-on-click="{{ goTabExperiences }}" data-coral-text="1" style="cursor:pointer;align-self:flex-start;', '<span sc-camel-on-click="{{ goTabExperiences }}" data-vers-onglet="1" style="cursor:pointer;align-self:flex-start;')
s = remplace(s, '<span sc-camel-on-click="{{ goTabLessons }}" style="cursor:pointer;font-weight:700;color:#368CAF;', '<span sc-camel-on-click="{{ goTabLessons }}" data-vers-onglet="1" style="cursor:pointer;font-weight:700;color:#368CAF;')
if 'data-experiences="1"' not in s:
    i = s.index('<!-- EXPERIENCES (production'); j = s.index('<section style="', i)
    s = s[:j] + '<section data-experiences="1" style="' + s[j + len('<section style="'):]
if 'data-appel="1"' not in s:
    i = s.index('<!-- CAMP FINAL CTA'); j = s.index('<section style="', i)
    s = s[:j] + '<section data-appel="1" style="' + s[j + len('<section style="'):]

# La marée demande son libellé à la couche (petit titre plutôt que titre long)
s = remplace(s, "(INDICE[l] || INDICE.en) : (sections[actif].innerText || '').trim();",
             "(INDICE[l] || INDICE.en) : (window.surfinn_libelle ? window.surfinn_libelle(sections[actif]) : (sections[actif].innerText || '').trim());")

stk = json.load(open(os.path.join(ICI, 'experience', 'stickers.json'), encoding='utf-8'))
variables = '  :root{' + ''.join(f'--stk-{k}:{uri(v)};' for k, v in stk.items()) + '}\n'
css = open(os.path.join(ICI, 'experience', 'couche.css'), encoding='utf-8').read()
js = open(os.path.join(ICI, 'experience', 'couche.js'), encoding='utf-8').read()
# Direction « Maison » : registre plus adulte, posé par-dessus la couche (voir DIRECTION-MAISON.md)
maison = os.path.join(ICI, 'experience', 'maison.css')
if os.path.exists(maison):
    css += open(maison, encoding='utf-8').read()
    # Photos clés choisies pour un public de 30 ans et plus (voir DIRECTION-MAISON.md). Seules les images changent, pas les textes.
    A = "window.__asset('uploads/%s')"
    # Accueil, pilier « Se poser » : trois vingtenaires en maillot -> le hamac d'une chambre privée
    # Accueil, « Pour qui » : la surfeuse d'origine est remise (retour de Kévin du 12/11)
    fin = ' alt="Surf Inn guests on the beach" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;'
    s = s.replace('<img src="8cac39f3-9afe-4808-a6d3-7ba8af1da2ab"' + fin + 'object-position:18% 50%;">', '<img src="20b7227f-4a35-4664-9991-c6a93a05e0fd"' + fin + '">')
    # Accueil, pilier « Apprendre » : quatre personnes qui posent avec leurs planches -> un moniteur qui tient la main d'une élève sur sa planche
    # « Pour qui », profil « Se poser » : groupe en rang devant les planches -> la table du petit-déjeuner
    s = remplace(s, "not a program', img: " + A % 'ph-group-m.webp' + ", pos: '50% 55%'", "not a program', img: " + A % 'carte-4-table-HOS012-c.webp' + ", pos: '50% 60%'")
    # Rio, « Le quotidien » : uniquement des photos de Rio. Groupe en rang -> le jardin de la Surf House ; tablée de bières -> le salon du Surf Club
    for img, alt, pos in (('ph-group-m.webp', 'Guests and team together', '50% 55%'), ('carte-6-accolade-HOS007.webp', 'Guests and team together', '50% 35%')):
        s = s.replace("{ img: " + A % img + ", alt: '" + alt + "', pos: '" + pos + "' }", "{ img: " + A % 'ph-sh-garden-m.webp' + ", alt: 'In the garden', pos: '50% 50%' }")
    for img, alt, pos in (('ph-rd-table-m.webp', 'Guests around the table at night', '50% 50%'), ('carte-4-table-HOS012-c.webp', 'Breakfast at the big table', '50% 60%')):
        s = s.replace("{ img: " + A % img + ", alt: '" + alt + "', pos: '" + pos + "' }", "{ img: " + A % 'ph-sc-lounge-m.webp' + ", alt: 'Lounge and TV corner', pos: '50% 50%' }")
    s = remplace(s, "{ img: " + A % 'ph-rd-night-m.webp' + ", alt: 'A night out in front of a mural', pos: '50% 50%' }", "{ img: " + A % 'carte-5-mirante-HIK026-c.webp' + ", alt: 'Hikes & viewpoints', pos: '50% 50%' }")
    # Accueil : « Découvrir Surf Inn Rio / Bahia » deviennent de vrais boutons secondaires (le principal reste « Créer mon séjour »)
    for cible in ('goRio', 'goItacare'):
        s = remplace(s, '<span sc-camel-on-click="{{ ' + cible + ' }}" role="link" sc-camel-tab-index="0" style="cursor:pointer;font-weight:700;color:#368CAF;font-size:17px;', '<span sc-camel-on-click="{{ ' + cible + ' }}" role="link" sc-camel-tab-index="0" data-vers-onglet="1" style="cursor:pointer;font-weight:700;color:#368CAF;font-size:17px;')
    # ═══ Retours de Lucas (réunion du 12/11/2026), branche refonte-chaleur ═══
    # Polices : Gabarito pour les titres (Fraunces ne reste que sur les cartes de « Le Brésil, c'est… »)
    POL = 'family=Chivo:wght@400;600;700&family=Londrina+Solid:wght@400;900'
    for anc in (POL + '&display=swap', POL + '&family=Fraunces:opsz,wght@9..144,400..600&display=swap'):
        s = s.replace(anc, POL + '&family=Fraunces:opsz,wght@9..144,400..600&family=Gabarito:wght@600;700&display=swap')
    s = s.replace('&family=Gabarito:wght@600;700&display=swap', '&family=Gabarito:wght@600;700&family=Permanent+Marker&display=swap')
    # Fraunces retirée (14/11/2026) : les noms des cartes passent dans la police des titres, trois polices plus celle du logo
    s = s.replace('&family=Fraunces:opsz,wght@9..144,400..600', '')
    # Bande du bas (planche, « Fais défiler pour surfer ») retirée partout : le script ne s'installe plus
    s = s.replace("    if (!document.body || document.querySelector('[data-maree]')) return;\n    document.body.appendChild(maree);", "    return; // bande du bas retirée (retour de Lucas)\n    document.body.appendChild(maree);")
    # Pilier « Belong » : retour de la photo du Kombi (les trois personnes qui rient)
    for avant in ("label: 'Belong', title: \"Just stay. That's a complete plan.\", img: ", "title: 'Belong', grad: 'linear-gradient(150deg,#E9A13B,#ED6267)', img: "):
        s = s.replace(avant + A % 'ita-hammock-terrace-s-c.webp', avant + A % 'ph-belong-m.webp')
    # Pilier « Apprendre » : plusieurs élèves sur la même vague
    for avant in ("label: 'Learn', title: 'Surf, music and capoeira lessons', img: ", "title: 'Learn', grad: 'linear-gradient(150deg,#234668,#368CAF)', img: "):
        for img in ('ph-learn-m.webp', 'ph-pk-surfinrio-m.webp'):
            s = s.replace(avant + A % img, avant + "'/assets/drive-cours-vague.jpg'")
        s = s.replace(avant + A % 'ph-exp-lessons-m.webp', avant + "'/assets/drive-cours-vague.jpg'")
    # Accueil, cartes des deux camps : photos d'origine remises (Recreio vu du ciel, Itacaré et sa forêt), à la demande de Kévin
    s = s.replace('<img src="' + PHOTO_RIO + '" alt="Surf Inn Rio, Recreio" style="width:100%;height:100%;object-fit:cover;object-position:50% 55%;display:block;">', '<img src="f664ecf4-5dc1-4913-9bc5-612b28ac951e" alt="Surf in Rio de Janeiro" style="width:100%;height:100%;object-fit:cover;object-position:50% 55%;display:block;">')
    s = s.replace('<img src="' + PHOTO_ITA + '" alt="Surf Inn Bahia, Itacaré" style="width:100%;height:100%;object-fit:cover;display:block;">', '<img src="ac86cb62-c12a-47ba-8325-18afb36b02ed" alt="Jungle-backed beach in Itacaré, Bahia" style="width:100%;height:100%;object-fit:cover;display:block;">')
    # Clins d'œil en portugais : masqués quand le site est en portugais (ils laissent entendre que le site est fait pour les étrangers)
    if 'showBrNote' not in s:
        SI = '<sc-if value="{{ showBrNote }}" hint-placeholder-val="{{ true }}">'
        i = s.index('<p data-bresil-note="1"'); j = s.index('</p>', i) + 4
        s = s[:i] + SI + s[i:j] + '</sc-if>' + s[j:]
        a = '  <!-- BRASILEIROS, em português, de propósito -->\n'
        i = s.index(a) + len(a); j = s.index('</section>', i) + len('</section>')
        s = s[:i] + '  ' + SI + '\n' + s[i:j] + '\n  </sc-if>' + s[j:]
        s = remplace(s, "showBrLead: this.state.lang !== 'pt',", "showBrLead: this.state.lang !== 'pt', showBrNote: this.state.lang !== 'pt',")
    # Accueil : de vraies photos de voyageurs et de l'équipe, juste sous l'en-tête
    if 'data-vrai="1"' not in s:
        gal = """  <!-- VRAIES PHOTOS : voyageurs et équipe, preuve sociale (retour de Lucas) -->
  <section style="background:#FFFBF3;padding:clamp(48px,6vw,80px) clamp(24px,5vw,72px);">
    <div style="max-width:1240px;margin:0 auto;">
      <p style="font-weight:700;font-size:14px;letter-spacing:0.14em;text-transform:uppercase;color:#368CAF;margin:0 0 12px;">In real life</p>
      <h2 style="font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:clamp(28px,3.4vw,42px);line-height:1.08;margin:0 0 10px;color:#234668;text-wrap:pretty;">Real days at Surf Inn</h2>
      <p style="font-size:17px;line-height:1.55;color:#4A6A80;max-width:640px;margin:0 0 28px;">Guests, coaches and the team, as they are.</p>
      <div data-vrai="1" style="display:grid;grid-template-columns:repeat(6,1fr);gap:8px;">
        <sc-for list="{{ homeVrai }}" as="hv" hint-placeholder-count="12">
          <div style="position:relative;aspect-ratio:1;overflow:hidden;border-radius:10px;background:#C9DAE3;"><img src="{{ hv.img }}" alt="{{ hv.alt }}" loading="lazy" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{{ hv.pos }};"></div>
        </sc-for>
      </div>
    </div>
  </section>

"""
        s = remplace(s, '  <!-- OUR SURF CAMPS, section header', gal + '  <!-- OUR SURF CAMPS, section header')
        s = remplace(s, "      isWho: page === 'who', isFaq: page === 'faq',", "      homeVrai: [],\n      isWho: page === 'who', isFaq: page === 'faq',")
    i = s.index('<!-- VRAIES PHOTOS'); j = s.index('<div data-vrai="1"', i)
    s = s[:i] + s[i:j].replace('Taken by guests and the team, not by a photographer.', 'Guests, coaches and the team, as they are.') + s[j:]
    TX = os.path.join(os.path.dirname(GAB), 'textes', '71cd2ba0-e21d-4eee-9a5b-32dc222146da.js')
    # Textes de la galerie (13/11) : on dit qui l'on voit et on répond au doute « photos de banque d'images ou d'IA »
    i = s.index('<!-- VRAIES PHOTOS'); j = s.index('<div data-vrai="1"', i); bl = s[i:j]
    for av, ap in (('In real life', 'Caught in the moment'), ('Real days at Surf Inn', "The people you'll meet here"), ('Guests, coaches and the team, as they are.', 'No models, no stock photos: guests, coaches and the team, in Rio and Itacaré.')):
        bl = bl.replace('>' + av + '</', '>' + ap + '</')
    s = s[:i] + bl + s[j:]
    t = open(TX, encoding='utf-8').read()
    if '"Caught in the moment":' not in t:
        for lang, tr in (('fr', ('Pris sur le vif', 'Les gens que vous allez croiser', 'Ni figurants ni banque d’images : des voyageurs, des moniteurs et l’équipe, à Rio et à Itacaré.')), ('pt', ('Do jeito que é', 'A galera que você vai encontrar', 'Sem modelo e sem banco de imagem: hóspedes, professores e equipe, no Rio e em Itacaré.'))):
            anc = '  "%s": {\n' % lang
            t = t.replace(anc, anc + '    "Caught in the moment": %s,\n    "The people you\'ll meet here": %s,\n    "No models, no stock photos: guests, coaches and the team, in Rio and Itacaré.": %s,\n' % tuple(json.dumps(x, ensure_ascii=False) for x in tr))
        open(TX, 'w', encoding='utf-8').write(t)
    # Tunnel : plus de rouge de l'ancienne charte. Les couleurs de sélection passent par --accent (vert pour Rio et le reste du site,
    # orange pour Itacaré), le bouton « Continuer » par --principal. La barre des étapes garde son repère (lu par etapes()).
    L = s.split('\n'); dans = False
    for k, l in enumerate(L):
        if 'bg: isIn || isOut ?' in l: dans = True
        if dans and 'label, bar: i + 1 <= step' not in l:
            l = l.replace("primaryBg: stepInvalidMsg(step) ? '#B8CBD4' : '#ED6267'", "primaryBg: stepInvalidMsg(step) ? '#B8CBD4' : 'var(--principal)'")
            L[k] = l.replace("'#ED6267'", "'var(--accent)'").replace("'#FCEBEB'", "'var(--accent-fond)'")
        if dans and 'primaryBg:' in l: break
    s = '\n'.join(L)
    # Galerie de l'accueil (Kévin, 16/11) : titre « La vie avec Surf Inn », sous-texte retiré
    i = s.index('<!-- VRAIES PHOTOS'); j = s.index('<div data-vrai="1"', i); bl = s[i:j]
    bl = bl.replace(">The people you'll meet here</", '>Life with Surf Inn</')
    k = bl.find('<p style="font-size:17px;line-height:1.55;color:#4A6A80;max-width:640px;margin:0 0 28px;">')
    if k >= 0:
        bl = bl[:k] + bl[bl.index('</p>', k) + 4:].lstrip('\n ')
        bl = bl.replace('margin:0 0 10px;color:#234668;text-wrap:pretty;">Life with Surf Inn</h2>', 'margin:0 0 24px;color:#234668;text-wrap:pretty;">Life with Surf Inn</h2>\n      ')
    s = s[:i] + bl + s[j:]
    t = open(TX, encoding='utf-8').read()
    if '"Life with Surf Inn":' not in t:
        for lang, tr in (('fr', 'La vie avec Surf Inn'), ('pt', 'A vida com a Surf Inn')):
            anc = '  "%s": {\n' % lang
            t = t.replace(anc, anc + '    "Life with Surf Inn": %s,\n' % json.dumps(tr, ensure_ascii=False))
        open(TX, 'w', encoding='utf-8').write(t)
    # Instagram à portée de main sous la galerie ; le bloc Instagram du bas de page, devenu doublon, est retiré
    if 'data-vrai-insta' not in s:
        i = s.index('<div data-vrai="1"'); j = s.index('</sc-for>', i); j = s.index('</div>', j) + 6
        s = s[:j] + """
      <p data-vrai-insta="1" style="display:flex;flex-wrap:wrap;align-items:center;gap:8px 22px;margin:22px 0 0;font-size:16px;color:#4A6A80;"><span>More of this, every day, on Instagram:</span><a href="https://www.instagram.com/surfinnrio/" target="_blank" rel="noopener" style="font-weight:700;color:#368CAF;text-decoration:none;">@surfinnrio →</a><a href="https://www.instagram.com/surfinnbahia/" target="_blank" rel="noopener" style="font-weight:700;color:#368CAF;text-decoration:none;">@surfinnbahia →</a></p>""" + s[j:]
    a = "  <!-- INSTAGRAM sur l'accueil"
    if a in s:
        i = s.index(a); j = s.index('</section>', i) + len('</section>')
        s = s[:i] + s[j:].lstrip('\n')
    t = open(TX, encoding='utf-8').read()
    if '"More of this, every day, on Instagram:"' not in t:
        for lang, tr in (('fr', 'La suite, au jour le jour, sur Instagram :'), ('pt', 'Tem mais, todo dia, no Instagram:')):
            anc = '  "%s": {\n' % lang
            t = t.replace(anc, anc + '    "More of this, every day, on Instagram:": %s,\n' % json.dumps(tr, ensure_ascii=False))
        open(TX, 'w', encoding='utf-8').write(t)
    # La liste est réécrite à chaque passage (l'ordre « pos, alt, img » évite d'être touché par les remplacements du « quotidien » de Rio)
    don = "      homeVrai: [" + ', '.join("{ pos: '%s', alt: '%s', img: %s }" % (pos, alt, (A % f) if not f.startswith('/') else "'" + f + "'") for f, alt, pos in VRAIES) + "],\n"
    i = s.index("      homeVrai: ["); j = s.index("\n", i) + 1
    s = s[:i] + don + s[j:]
    # Traductions propres à cette branche
    TX = os.path.join(os.path.dirname(GAB), 'textes', '71cd2ba0-e21d-4eee-9a5b-32dc222146da.js')
    t = open(TX, encoding='utf-8').read()
    for a, b in (('"A place to Learn. Work. Belong. Explore.": "Apprendre. Travailler. Se poser. Explorer."', '"A place to Learn. Work. Belong. Explore.": "Apprendre. Travailler. Se retrouver. Explorer."'), ('"Belong": "Se poser"', '"Belong": "Se retrouver"'), ('apprendre, travailler, se poser et explorer', 'apprendre, travailler, se retrouver et explorer')):
        t = t.replace(a, b)
    if '"Guests, coaches and the team, as they are.":' not in t:
        for lang, tr in (('fr', ('En vrai', 'Le quotidien à Surf Inn', 'Les voyageurs, les moniteurs et l’équipe, tels qu’ils sont.')), ('pt', ('Na real', 'O dia a dia na Surf Inn', 'Hóspedes, professores e equipe, do jeito que são.'))):
            anc = '  "%s": {\n' % lang
            t = t.replace(anc, anc + '    "In real life (home)": %s,\n    "Real days at Surf Inn (home)": %s,\n    "Guests, coaches and the team, as they are.": %s,\n' % tuple(json.dumps(x, ensure_ascii=False) for x in tr))
    open(TX, 'w', encoding='utf-8').write(t)
# Règles mobiles inspirées d'anglify.com (voir REGLES-MOBILE.md)
mobile = os.path.join(ICI, 'experience', 'mobile.css')
if os.path.exists(mobile):
    css += open(mobile, encoding='utf-8').read()
    # Voyageurs dans la fenêtre des dates (téléphone, hors tunnel) ; le champ « Dates » de l'accueil affiche alors dates et nombre de personnes
    if 'data-dp-voyageurs' not in s:
        _i = s.index('<div data-dp-pop="1"'); _j = s.index('<div style="display:flex;align-items:center;justify-content:space-between;gap:12px;margin-top:12px;padding-top:12px;border-top:1px solid rgba(54,140,175,0.14);">', _i)
        s = s[:_j] + """<div data-dp-voyageurs="1" style="align-items:center;justify-content:space-between;gap:12px;margin-top:12px;padding-top:12px;border-top:1px solid rgba(54,140,175,0.14);">
      <span style="font-size:14px;font-weight:700;color:#234668;">Travelers</span>
      <div style="display:flex;align-items:center;gap:16px;">
        <span data-step-btn="1" sc-camel-on-click="{{ peopleMinus }}" role="button" aria-label="−" style="cursor:pointer;width:36px;height:36px;border-radius:50%;background:#DEEBF2;color:#234668;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:20px;line-height:1;">−</span>
        <span style="font-weight:800;color:#234668;font-size:17px;min-width:18px;text-align:center;">{{ people }}</span>
        <span data-step-btn="1" sc-camel-on-click="{{ peoplePlus }}" role="button" aria-label="+" style="cursor:pointer;width:36px;height:36px;border-radius:50%;background:#DEEBF2;color:#234668;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:20px;line-height:1;">+</span>
      </div>
    </div>
    """ + s[_j:]
        _a = 'value="{{ datesValue }}" data-nudge="{{ datesNudge }}" placeholder="Add your dates"'
        _k = s.index(_a); s = s[:_k] + 'value="{{ datesValueAccueil }}" data-nudge="{{ datesNudge }}" placeholder="Add your dates"' + s[_k + len(_a):]
        _a = "      datesValue: S.checkin && S.checkout ?"
        assert s.count(_a) == 1
        s = s.replace(_a, """      datesValueAccueil: (() => {
        const long = S.checkin && S.checkout ? fmt(S.checkin).replace(/ \\d{4}$/, '') + ' → ' + fmt(S.checkout) : S.checkin ? fmt(S.checkin) + ' → …' : '';
        if (typeof window === 'undefined' || window.innerWidth > 720 || !(S.checkin && S.checkout)) return long;
        const a = fmt(S.checkin).replace(/ \\d{4}$/, ''), b = fmt(S.checkout).replace(/ \\d{4}$/, '');
        const ma = a.replace(/^\\d+\\s*/, ''), mb = b.replace(/^\\d+\\s*/, '');
        const dates = ma && ma === mb ? a.replace(ma, '').trim() + ' → ' + b : a + ' → ' + b;
        const mot = ({ fr: 'pers.', pt: 'pess.' })[this.state.lang] || (S.people > 1 ? 'guests' : 'guest');
        return dates + ' · ' + S.people + ' ' + mot;
      })(),
""" + _a)
    # Menu « Destination » : repère pour le centrer sur téléphone (il se plaçait selon la position du champ, parfois très bas)
    s = s.replace('<div style="position:fixed;z-index:401;top:{{ dmTop }};left:{{ dmLeft }};', '<div data-dm-pop="1" style="position:fixed;z-index:401;top:{{ dmTop }};left:{{ dmLeft }};')
    # Pages camp (16/11) : le module Instagram prend le titre « Le quotidien à Surf Inn Rio / Bahia » ; la galerie « Le quotidien » de Rio, qui faisait doublon, est masquée (mobile.css)
    s = s.replace("igTitle: 'Rio, one session at a time'", "igTitle: 'Daily life at Surf Inn Rio'").replace("igTitle: 'Bahia, straight from the trail'", "igTitle: 'Daily life at Surf Inn Bahia'")
    _tx = os.path.join(os.path.dirname(GAB), 'textes', '71cd2ba0-e21d-4eee-9a5b-32dc222146da.js')
    _t = open(_tx, encoding='utf-8').read()
    if '"Daily life at Surf Inn Rio":' not in _t:
        for _lang, _r, _b in (('fr', 'Le quotidien à Surf Inn Rio', 'Le quotidien à Surf Inn Bahia'), ('pt', 'O dia a dia na Surf Inn Rio', 'O dia a dia na Surf Inn Bahia')):
            _anc = '  "%s": {\n' % _lang
            _t = _t.replace(_anc, _anc + '    "Daily life at Surf Inn Rio": %s,\n    "Daily life at Surf Inn Bahia": %s,\n' % (json.dumps(_r, ensure_ascii=False), json.dumps(_b, ensure_ascii=False)))
        open(_tx, 'w', encoding='utf-8').write(_t)
    # En-tête de l'accueil (16/11) : les deux phrases de la description deviennent deux éléments distincts, pour les placer séparément sur téléphone
    s = s.replace('{{ heroSubA }}<br>{{ heroSubB }}</p>', '<span data-desc-a="1">{{ heroSubA }}</span><br data-desc-br="1"><span data-desc-b="1">{{ heroSubB }}</span></p>')
    # Le bouton flottant ne s'affiche pas tant que le module de l'en-tête est à l'écran (son bouton est de nouveau ancré dans la page)
    s = s.replace("[data-verbes]').forEach(el => {", "[data-verbes],[data-hero-champ]').forEach(el => {")
    # Retours du 16/11 : repères pour les puces de « Votre séjour » et les trois blocs de l'emplacement ; libellés « Découvrir »
    s = s.replace('line-height:1.5;color:#33566E;">\n          <sc-for list="{{ camp.peek.points }}"', 'line-height:1.5;color:#33566E;" data-puces-sejour="1">\n          <sc-for list="{{ camp.peek.points }}"')
    _k = s.find('<div data-carte-apercu="1"')
    if _k > 0 and 'data-emplacement="1"' not in s:
        _m = s.index('<div style="display:flex;flex-direction:column;gap:26px;justify-content:center;">', _k)
        s = s[:_m] + '<div data-emplacement="1" style="display:flex;flex-direction:column;gap:26px;justify-content:center;">' + s[_m + len('<div style="display:flex;flex-direction:column;gap:26px;justify-content:center;">'):]
    _tx = os.path.join(os.path.dirname(GAB), 'textes', '71cd2ba0-e21d-4eee-9a5b-32dc222146da.js')
    _t = open(_tx, encoding='utf-8').read()
    _t = _t.replace('Voir le camp', 'Découvrir le camp').replace('Voir toutes les expériences', 'Découvrir toutes les expériences')
    open(_tx, 'w', encoding='utf-8').write(_t)
    # Avis de l'accueil : les cartes ne sont plus des liens (Kévin, 15/11) ; les pages Google restent accessibles par les pastilles de notes
    _a = '<a href="{{ r.url }}" target="_blank" rel="noopener" style="background:#FFFBF3;border-radius:20px;padding:28px 28px 26px;display:flex;flex-direction:column;gap:16px;text-decoration:none;color:inherit;" style-hover="box-shadow:0 10px 28px rgba(23,42,62,0.10);">'
    if _a in s:
        _i = s.index(_a); _j = s.index('          </a>', _i)
        s = s[:_i] + '<div data-avis="1" style="background:#FFFBF3;border-radius:20px;padding:28px 28px 26px;display:flex;flex-direction:column;gap:16px;color:inherit;">' + s[_i + len(_a):_j] + '          </div>' + s[_j + len('          </a>'):]
    # Accueil, carte Recreio : deux puces raccourcies pour tenir sur une ligne (Kévin, 15/11)
    _tx = os.path.join(os.path.dirname(GAB), 'textes', '71cd2ba0-e21d-4eee-9a5b-32dc222146da.js')
    _t = open(_tx, encoding='utf-8').read()
    # (16/11) ces deux textes longs sont rétablis : la version courte ne sert plus que sur téléphone, voir COURTS plus bas
    _t = _t.replace('"Stay right on the beach, steps from the waves": "Hébergement devant les vagues"', '"Stay right on the beach, steps from the waves": "Hébergement en bord de plage, juste devant les vagues"').replace('a surf vibe and nature": "Autour : bars de plage, concerts et nature"', 'a surf vibe and nature": "Autour : concerts, restaurants, bars de plage et nature"')
    COURTS = (
        ('The neighborhood with the most surf spots in Rio, from Macumba to Grumari', 'The neighborhood with the most surf spots in Rio', 'Le quartier avec le plus de spots de Rio', 'O bairro com mais picos de surf do Rio'),
        ('Stay right on the beach, steps from the waves', 'Stay steps from the waves', 'Hébergement devant les vagues', 'Hospedagem de frente para as ondas'),
        ('All around you: live music, good restaurants and bars, a surf vibe and nature', 'All around you: beach bars, live music and nature', 'Autour : bars de plage, concerts et nature', 'Em volta: bares de praia, shows e natureza'),
        ('One of the best surf coasts in Brazil, with waves for every level', 'One of the best surf coasts in Brazil', 'Une des meilleures côtes de surf du Brésil', 'Um dos melhores litorais de surf do Brasil'),
    )
    _t = _t.replace('"Uma das melhores costas de surf do Brasil"', '"Um dos melhores litorais de surf do Brasil"').replace('"Ao redor: bares de praia, shows e natureza"', '"Em volta: bares de praia, shows e natureza"')
    # Concept de l'accueil : phrase raccourcie sur téléphone (les quatre verbes sont déjà dans le titre et sur les cartes)
    _L = 'Surf Inn offers four ways to live your trip: learn, work, belong and explore, through surf, music and the people you meet. Take all of it, or just the parts you want.'
    _C = 'Surf Inn offers four ways to live your trip, through surf, music and the people you meet. Take all of it, or just the parts you want.'
    s = s.replace('margin:0 0 40px;">' + _L + '</p>', 'margin:0 0 40px;"><span data-long="1">' + _L + '</span><span data-court="1">' + _C + '</span></p>')
    _t = _t.replace('"A Surf Inn propõe quatro jeitos de viver a sua viagem, em torno do surf, da música e das pessoas. Viva tudo, ou só o que der vontade."', '"O Surf Inn propõe quatro jeitos de viver a sua viagem, em torno do surf, da música e das pessoas. Viva tudo ou só o que você quiser."')
    for _lang, _v in (('fr', 'Surf Inn propose quatre façons de vivre votre voyage, autour du surf, de la musique et des gens. Vivez tout, ou seulement ce qui vous tente.'), ('pt', 'O Surf Inn propõe quatro jeitos de viver a sua viagem, em torno do surf, da música e das pessoas. Viva tudo ou só o que você quiser.')):
        _anc = '  "%s": {\n' % _lang
        if json.dumps(_C) + ':' not in _t:
            pass
        _i = _t.index(_anc); _j = _t.index('\n  }', _i)
        if json.dumps(_C) + ':' not in _t[_i:_j]:
            _t = _t[:_i + len(_anc)] + '    %s: %s,\n' % (json.dumps(_C), json.dumps(_v, ensure_ascii=False)) + _t[_i + len(_anc):]
    for _long, _court, _fr, _pt in COURTS:
        s = s.replace('·</span>' + _long + '</li>', '·</span><span data-long="1">' + _long + '</span><span data-court="1">' + _court + '</span></li>')
        for _lang, _v in (('fr', _fr), ('pt', _pt)):
            _anc = '  "%s": {\n' % _lang; _i = _t.index(_anc); _j = _t.index('\n  }', _i)
            if json.dumps(_court) + ':' not in _t[_i:_j]:
                _t = _t[:_i + len(_anc)] + '    %s: %s,\n' % (json.dumps(_court), json.dumps(_v, ensure_ascii=False)) + _t[_i + len(_anc):]
    open(_tx, 'w', encoding='utf-8').write(_t)
    # ═══ Retours de Kévin du 14/11/2026 (soir) : aperçus des camps plus courts sur téléphone, bas de l'accueil ═══
    _t = open(_tx, encoding='utf-8').read()
    def _dico(_t, cle, fr, pt):
        for _lang, _v in (('fr', fr), ('pt', pt)):
            _anc = '  "%s": {\n' % _lang; _i = _t.index(_anc); _j = _t.index('\n  }', _i)
            if json.dumps(cle, ensure_ascii=False) + ':' not in _t[_i:_j] and json.dumps(cle) + ':' not in _t[_i:_j]:
                _t = _t[:_i + len(_anc)] + '    %s: %s,\n' % (json.dumps(cle, ensure_ascii=False), json.dumps(_v, ensure_ascii=False)) + _t[_i + len(_anc):]
        return _t
    # Phrase d'introduction des expériences (aperçu de Rio et d'Itacaré) : texte dicté par Kévin, sans « Chaque activité s'ajoute une par une »
    _vie = 'Add coaching, surf guiding, recovery, music and days out to your stay.'
    s = s.replace('Beyond the surf lessons, everything you can add to your stay: coaching, guiding, recovery, music and days out. Build your trip item by item.</p>', _vie + '</p>')
    _t = _dico(_t, _vie, 'Enrichissez votre séjour de coaching, de surf guiding, de récupération, de musique et de sorties.', 'Enriqueça sua estadia com coaching, surf guiding, recuperação, música e passeios.')
    # Bouton : « Découvrir les expériences » tient sur une ligne
    _t = _t.replace('Découvrir toutes les expériences', 'Découvrir les expériences')
    # Textes d'introduction : version courte sur téléphone (trois lignes au plus), texte complet sur ordinateur
    _rio_surf = 'Surf Recreio, explore the wild beaches out west, and live the city at night.'
    _ita_surf = 'One road, a dozen waves, rainforest in between. Tiririca is five minutes on foot.'
    _ita_camp = 'Right in the center of Itacaré: a leafy garden full of birdsong and a welcoming place to come back to.'
    _ita_region = 'A fishing town wrapped in jungle: waves by day, something on every night.'
    def _court(s, avant, **courts):
        apres = avant.replace('">{{', '"><span data-txt-long="1">{{').replace('}}</p>', '}}</span>' + ''.join('<span data-txt-court="%s">%s</span>' % (k, v) for k, v in courts.items()) + '</p>')
        return s.replace(avant, apres)
    s = _court(s, 'margin:0 0 18px;">{{ camp.whyIntro }}</p>', rio=_rio_surf, itacare=_ita_surf)
    s = _court(s, 'margin:0 0 24px;">{{ camp.placeIntro }}</p>', itacare=_ita_camp)
    s = _court(s, 'max-width:640px;margin:0 0 12px;">{{ camp.regionIntro }}</p>', itacare=_ita_region)
    _t = _dico(_t, _rio_surf, 'Surfez à Recreio, explorez les plages sauvages de l’ouest, et vivez la ville le soir.', 'Surfe no Recreio, explore as praias selvagens da zona oeste e viva a cidade à noite.')
    _t = _dico(_t, _ita_surf, 'Une seule route, une douzaine de vagues, la forêt entre chacune. Tiririca est à cinq minutes à pied.', 'Uma estrada, uma dúzia de ondas e a mata entre elas. A Tiririca fica a cinco minutos a pé.')
    _t = _dico(_t, _ita_camp, 'En plein centre d’Itacaré, un jardin arboré où chantent les oiseaux et un lieu accueillant où revenir.', 'Bem no centro de Itacaré: um jardim arborizado cheio de pássaros e um lugar acolhedor para voltar.')
    _t = _dico(_t, _ita_region, 'Une ville de pêcheurs entourée de jungle : les vagues le jour, une sortie chaque soir.', 'Uma vila de pescadores cercada de mata: ondas de dia, programa toda noite.')
    open(_tx, 'w', encoding='utf-8').write(_t)
    # Bas de l'accueil : sous « Créer mon séjour », un accès direct aux deux camps (sans remonter la page)
    _fin = 'style-hover="background:#234668;color:#FFF8EF;">Request to book</span>\n    </div>\n  </section>\n\n  <!-- PILLAR MODAL -->'
    if 'data-vers-camps' not in s and _fin in s:
        s = s.replace(_fin, 'style-hover="background:#234668;color:#FFF8EF;">Request to book</span>\n      <div data-vers-camps="1"><span sc-camel-on-click="{{ goRio }}" role="link" sc-camel-tab-index="0">Surf Inn Rio →</span><span sc-camel-on-click="{{ goItacare }}" role="link" sc-camel-tab-index="0">Surf Inn Bahia →</span></div>\n    </div>\n  </section>\n\n  <!-- PILLAR MODAL -->')
    # ═══ En-tête des pages camp sur téléphone, piste A retenue par Kévin (14/11/2026) : nom du camp sur la vidéo, champ « Dates », bouton ═══
    if 'data-camp-encart' not in s:
        _i = s.index('<label data-hero-champ="1"', s.index('value="{{ destLabel }}"')); _j = s.index('</label>', _i) + len('</label>')
        _dates = s[_i:_j].replace('data-hero-champ="1"', 'data-camp-dates="1"')
        _corps = '    <div style="position:relative;z-index:2;padding:0 clamp(24px,5vw,72px) clamp(48px,7vh,80px);max-width:1500px;width:100%;box-sizing:border-box;">\n      <p style="font-weight:700;font-size:14px;letter-spacing:0.14em;text-transform:uppercase;color:#F5CE8E;margin:0 0 12px;">{{ camp.eyebrow }}</p>'
        s = remplace(s, _corps, '    <div data-marque-camp="1" aria-hidden="true">Surf Inn <b data-camp="rio">Rio</b><b data-camp="itacare">Bahia</b></div>\n' + _corps.replace('<div style="position:relative;z-index:2;', '<div data-camp-encart="1" style="position:relative;z-index:2;'))
        _cta = '<div style="display:flex;flex-wrap:wrap;align-items:center;gap:16px 24px;">\n        <span data-primary-cta="1" sc-camel-on-click="{{ openFunnelCamp }}" data-coral="1"'
        s = remplace(s, _cta, _cta.replace('\n        <span data-primary-cta', '\n        ' + _dates + '\n        <span data-primary-cta'))
        # Bouton flottant des pages camp : une barre « Dates » + « Créer mon séjour » (essai demandé par Kévin)
        _flot = '<sc-if value="{{ mobileCtaOn }}" hint-placeholder-val="{{ false }}">\n<div data-mobile-cta="1"'
        s = remplace(s, _flot, '<sc-if value="{{ mobileCtaOn }}" hint-placeholder-val="{{ false }}">\n<div data-barre-fond="1"></div>\n' + _dates.replace('data-camp-dates="1"', 'data-barre-dates="1"') + '\n<div data-mobile-cta="1"')
    # Fenêtre des cartes du concept : repère pour la faire tenir sans défilement sur téléphone
    s = s.replace('<sc-if value="{{ rtbModalOpen }}" hint-placeholder-val="{{ false }}">\n    <div sc-camel-on-click="{{ closeRtb }}" style="', '<sc-if value="{{ rtbModalOpen }}" hint-placeholder-val="{{ false }}">\n    <div sc-camel-on-click="{{ closeRtb }}" data-fenetre-concept="1" style="')
    # Le bouton flottant « Créer mon séjour » s'efface dès qu'un bouton d'action est à l'écran, principal ou secondaire (idée de Kévin, 14/11)
    s = s.replace("document.querySelectorAll('[data-primary-cta]').forEach(el => {\n        const r = el.getBoundingClientRect();", "document.querySelectorAll('[data-primary-cta],[data-vers-onglet]').forEach(el => {\n        const r = el.getBoundingClientRect();")
    # … et dans la section du concept, où les cartes sont elles-mêmes cliquables
    s = s.replace("document.querySelectorAll('[data-primary-cta],[data-vers-onglet]').forEach(el => {", "document.querySelectorAll('[data-primary-cta],[data-vers-onglet],[data-verbes]').forEach(el => {")
    # … ni tant que le formulaire ou le titre de l'en-tête est à l'écran (sur téléphone, le bouton de l'en-tête est sous la vidéo)
    s = s.replace("document.querySelectorAll('[data-primary-cta],[data-vers-onglet],[data-verbes]').forEach(el => {", "document.querySelectorAll('[data-primary-cta],[data-vers-onglet],[data-verbes],[data-hero-champ],[data-hero-immersif] h1').forEach(el => {")
    # Deuxième version du premier écran mobile : le bouton flottant y est présent (il ne s'efface que devant le formulaire)
    s = s.replace("[data-verbes],[data-hero-champ],[data-hero-immersif] h1').forEach(el => {", "[data-verbes],[data-hero-champ]').forEach(el => {")
    # Troisième version : le bouton flottant sert de bouton au module de l'en-tête, il reste donc visible devant lui
    s = s.replace("[data-verbes],[data-hero-champ]').forEach(el => {", "[data-verbes]').forEach(el => {")
    # Carte « Apprendre » : les cours de portugais ne sont pas proposés, ligne retirée (Kévin, 15/11)
    s = s.replace("'Surf lessons, surf guiding, video analysis', 'Portuguese lessons: learn the basics or polish your level', ", "'Surf lessons, surf guiding, video analysis', ")
    # La seconde phrase de l'en-tête (« Venez pour le surf, repartez avec le Brésil. ») avait été retirée puis remise à la demande de Kévin (14/11)
    s = s.replace('{{ heroSubA }}</p>', '{{ heroSubA }}<br>{{ heroSubB }}</p>')
    # Cartes de « La région » : le genre (Surf, Beach, Party…) en attribut, pour distinguer paysages et sorties
    s = s.replace('<sc-for list="{{ camp.regionCards }}" as="rg" hint-placeholder-count="6">\n        <div style="', '<sc-for list="{{ camp.regionCards }}" as="rg" hint-placeholder-count="6">\n        <div data-genre="{{ rg.tag }}" style="')
    s = s.replace('<div ref="{{ regionRef }}" data-peek-row="1">', '<div ref="{{ regionRef }}" data-peek-row="1" data-cartes-postales="1">')
    s = s.replace('<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;">\n      <sc-for list="{{ moments }}"', '<div data-bande-mobile="1" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;">\n      <sc-for list="{{ moments }}"')
    # --- Retours d'Alexis du 14/11/2026 : l'alerte du parcours disparaît dès que l'étape est complète.
    if "stepMsg: S.stepMsg ? (stepInvalidMsg(step) || null) : null," not in s:
        s = remplace(s, "      stepMsg: S.stepMsg || null,", "      stepMsg: S.stepMsg ? (stepInvalidMsg(step) || null) : null,")
    # ═══ Retours de Kévin du 16/11/2026 sur l'accueil (d'après les retours d'Alexis) ═══
    # Concept : la phrase s'arrête après « des gens » (« Vivez tout, ou seulement ce qui vous tente » retiré), sur l'accueil seulement.
    _L2 = 'Surf Inn offers four ways to live your trip: learn, work, belong and explore, through surf, music and the people you meet.'
    _C2 = 'Surf Inn offers four ways to live your trip, through surf, music and the people you meet.'
    s = s.replace('<span data-long="1">' + _L + '</span><span data-court="1">' + _C + '</span>', '<span data-long="1">' + _L2 + '</span><span data-court="1">' + _C2 + '</span>')
    _t = open(_tx, encoding='utf-8').read()
    _t = _dico(_t, _L2, 'Surf Inn propose quatre façons de vivre votre voyage : apprendre, travailler, se retrouver et explorer, autour du surf, de la musique et des gens.', 'O Surf Inn propõe quatro jeitos de viver a sua viagem: aprender, trabalhar, pertencer e explorar, em torno do surf, da música e das pessoas.')
    _t = _dico(_t, _C2, 'Surf Inn propose quatre façons de vivre votre voyage, autour du surf, de la musique et des gens.', 'O Surf Inn propõe quatro jeitos de viver a sua viagem, em torno do surf, da música e das pessoas.')
    # Pour qui : le style de voyage (solo, yoga, nomades digitaux, groupes) ; les trois lignes sur le niveau de surf sortent de la liste.
    _aud = [l for l in s.split('\n') if l.startswith("        { label: '") and ", desc: '" in l]
    _garde = ['Solo travelers', 'Yoga lovers', 'Digital nomads', 'Groups']
    if len(_aud) == 7:
        _par = {l.split("label: '")[1].split("'")[0]: l for l in _aud}
        s = s.replace('\n'.join(_aud), '\n'.join(_par[k] for k in _garde))
    _q = 'A surf camp for solo travelers, remote workers and groups.'
    s = s.replace('text-wrap:pretty;">Whatever your level, you belong here.</h2>', 'text-wrap:pretty;">' + _q + '</h2>')
    s = s.replace('<!-- WHO IS SURF INN FOR -->\n  <section style="', '<!-- WHO IS SURF INN FOR -->\n  <section data-pour-qui="1" style="')
    _t = _dico(_t, _q, 'Un surf camp pour voyager seul, télétravailler ou venir en groupe.', 'Um surf camp para viajar sozinho, trabalhar remoto ou vir em grupo.')
    # Pour qui, suite (16/11/2026) : lignes plus courtes (deux lignes au plus sur téléphone), « Voyageurs solo » reformulé.
    for _av, _ap, _fr, _pt in (
        ("{ label: 'Solo travelers', desc: 'Come alone, leave with friends for life' }", "{ label: 'Solo travelers', desc: 'You will not stay on your own for long' }", None, None),
        ("{ label: 'On your own', desc: 'You make friends fast here' }", "{ label: 'Solo travelers', desc: 'You will not stay on your own for long' }", None, None),
        ("desc: 'Yoga lessons every day, Hatha, Vinyasa, Bhakti, included in your stay' },\n        { label: 'Digital nomads'", "desc: 'Yoga lessons every day: Hatha, Vinyasa, Bhakti' },\n        { label: 'Digital nomads'", None, None),
        ("desc: 'Coworking space and fast wifi for a real work/surf balance' }", "desc: 'Starlink and a coworking corner' }", None, None),
        ("desc: 'Friend trips, couples and team retreats, we handle everything' }", "desc: 'With friends, as a couple or as a team' }", None, None),
    ):
        s = s.replace(_av, _ap)
    for _cle, _fr, _pt in (
        ('You will not stay on your own for long', 'vous ne resterez pas seul longtemps', 'você não vai ficar sozinho por muito tempo'),
        ('Yoga lessons every day: Hatha, Vinyasa, Bhakti', 'cours tous les jours (hatha, vinyasa, bhakti)', 'aula todos os dias (hatha, vinyasa, bhakti)'),
        ('Starlink and a coworking corner', 'Starlink et coin coworking', 'Starlink e um espaço de coworking'),
        ('With friends, as a couple or as a team', 'entre amis, en couple ou en équipe', 'com amigos, em casal ou em equipe'),
    ):
        _t = _dico(_t, _cle, _fr, _pt)
    # Fenêtres des quatre piliers du concept (16/11/2026) : textes raccourcis, repère pour la mise en page sur téléphone.
    _ap1 = "Start with surf, then open up to everything around it. The idea isn't to fill your schedule, it's to make curiosity part of the trip."
    s = s.replace("it's to make curiosity part of the trip: a cultural exchange.\",", "it's to make curiosity part of the trip.\",")
    s = s.replace("'Surf lessons, surf guiding, video analysis', 'Percussion lessons (samba, samba reggae, samba afro and other Brazilian rhythms)',", "'Surf lessons, surf guiding, video analysis', 'Percussion lessons',")
    _tr1 = 'Both surf camps have Starlink and a coworking corner, ideal for working.'
    s = s.replace("intro: '" + _tr1 + " And the timezone works with Europe and North America alike.',", "intro: '" + _tr1 + "',")
    _t = _dico(_t, _ap1, 'Commencez par le surf, puis ouvrez-vous à tout ce qui l’entoure. Notre but : faire de votre curiosité une partie du voyage.', 'Comece pelo surf e depois se abra para tudo o que está em volta. Nosso objetivo: fazer da sua curiosidade uma parte da viagem.')
    _t = _dico(_t, _tr1, 'Nos surf camps sont équipés de Starlink et d’un coin coworking, idéal pour travailler.', 'Nossos surf camps têm Starlink e um canto de coworking, ideal para trabalhar.')
    # Titre du concept sur l'accueil (choix de Kévin du 16/11/2026, « J2 ») : ne répète plus les quatre verbes des cartes.
    _j2 = 'A surf camp for traveling differently.'
    s = s.replace('">A place to Learn. Work. Belong. Explore.</h2>', '">' + _j2 + '</h2>')
    _t = _dico(_t, _j2, 'Un surf camp pour voyager autrement.', 'Um surf camp para viajar de outro jeito.')
    # Fin de l'accueil (choix de Kévin du 16/11/2026, piste A) : les deux pastilles sous « Créer mon séjour » deviennent une
    # section « Choisissez votre camp » avec deux cartes photo, pour qu'on comprenne qu'elles mènent aux pages Rio et Bahia.
    _pastilles = '      <div data-vers-camps="1"><span sc-camel-on-click="{{ goRio }}" role="link" sc-camel-tab-index="0">Surf Inn Rio →</span><span sc-camel-on-click="{{ goItacare }}" role="link" sc-camel-tab-index="0">Surf Inn Bahia →</span></div>\n    </div>\n  </section>\n'
    if 'data-suite-camps' not in s and _pastilles in s:
        _carte = lambda go, img, alt, nom, lieu: ('<div data-suite-carte="1" sc-camel-on-click="{{ %s }}" role="link" sc-camel-tab-index="0"><img src="%s" alt="%s" loading="lazy"><div data-suite-voile="1"></div><div data-suite-texte="1"><h3>%s</h3><p>%s</p><span data-suite-lien="1"><span>Discover</span> <span aria-hidden="true">→</span></span></div></div>' % (go, img, alt, nom, lieu))
        s = s.replace(_pastilles, '    </div>\n  </section>\n  <section data-suite-camps="1">\n    <div>\n      <p data-suite-eyebrow="1">Keep exploring</p>\n      <h2>Choose your camp.</h2>\n      <div data-suite-grille="1">'
            + _carte('goRio', 'f664ecf4-5dc1-4913-9bc5-612b28ac951e', 'Surf in Rio de Janeiro', 'Surf Inn Rio', 'Rio de Janeiro · Recreio')
            + _carte('goItacare', 'ac86cb62-c12a-47ba-8325-18afb36b02ed', 'Jungle-backed beach in Itacaré, Bahia', 'Surf Inn Bahia', 'Itacaré · Bahia')
            + '</div>\n    </div>\n  </section>\n')
    for _cle, _fr, _pt in (('Keep exploring', 'Continuer la visite', 'Continue a visita'), ('Choose your camp.', 'Choisissez votre camp.', 'Escolha o seu camp.'), ('Discover', 'Découvrir', 'Conhecer')):
        _t = _dico(_t, _cle, _fr, _pt)
    # Fenêtre « Se retrouver » (16/11/2026) : « même en cours de séjour » retiré.
    _sr = 'Stay without booking a single lesson, add anything later'
    s = s.replace("'" + _sr + ", even mid-stay',", "'" + _sr + "',")
    _t = _dico(_t, _sr, 'Un séjour possible sans aucun cours, avec des activités à ajouter plus tard', 'Dá para ficar sem nenhuma aula e acrescentar atividades depois')
    # ═══ Retours de Kévin du 16/11/2026 (soir) ═══
    # Depuis une page camp, si les dates sont déjà choisies, « Créer mon séjour » ouvre le parcours à l'étape Hébergement
    # (comme depuis l'accueil), et non à l'étape Voyage.
    s = s.replace("openFunnelCamp: () => this.setState(s => ({ dest: page, funnel: true, menuOpen: false, step: s.submitted ? 1 : s.step, submitted: false })),",
                  "openFunnelCamp: () => this.setState(s => ({ dest: page, funnel: true, menuOpen: false, step: s.submitted ? 1 : (s.step === 1 && s.checkin && s.checkout) ? (this.isHub ? this.stepFor('Stay', page) : this.stepFor('Package', page)) : s.step, submitted: false })),")
    # Logo : la version bleue de l'ancienne charte devient verte (assets/logo-surf-inn-vert.png, même dessin).
    s = s.replace("window.__asset('brand/logo-navy.png')", "'/assets/logo-surf-inn-vert.png'")
    # « Réponse rapide… » et phrases voisines : plus de teinte rosée (ancienne charte), crème partout.
    s = s.replace('color:#FFE3D9;', 'color:#F7F4EA;')
    # Accueil (demande de Kévin du 17/11/2026) : les avis remontent entre le concept et « Le Brésil, c'est… ».
    _a, _b, _c = '  <!-- REVIEWS -->\n', '  <!-- WHO IS SURF INN FOR -->\n', '  <!-- SURFING IN BRAZIL, affirmation -->\n'
    if s.count(_a) == 1 and s.count(_b) == 1 and s.count(_c) == 1 and s.index(_c) < s.index(_a) < s.index(_b):
        _avis = s[s.index(_a):s.index(_b)]
        s = s.replace(_avis, '').replace(_c, _avis + _c)
    # Survols et appuis (17/11/2026) : les bleus de l'ancienne charte encore présents dans les effets de survol
    # (flèches des avis, liens, cartes) passent aux verts du site. Seuls les attributs style-hover sont touchés.
    def _vert(m):
        v = m.group(0)
        for _x, _y in (('#234668', '#0C3B32'), ('#368CAF', '#128064'), ('rgba(54,140,175,', 'rgba(18,128,100,'), ('rgba(35,70,104,', 'rgba(12,59,50,'), ('rgba(23,42,62,', 'rgba(12,59,50,'), ('rgba(143,208,232,', 'rgba(18,128,100,')):
            v = v.replace(_x, _y)
        return v
    s = re.sub(r'style-hover="[^"]*"', _vert, s)
    # Restes de bleu au repos (relevé audit/retours/bleus.mjs du 17/11/2026) : gris-bleu du pied de page, bleu nuit des
    # pastilles de niveau et des compteurs de photos. Les bleus de Google, Instagram et Facebook sont laissés (marques).
    for _x, _y in (('#8FA9B5', '#B9C9C1'), ('rgb(143, 169, 181)', '#B9C9C1'), ('color:#172A3E', 'color:#0C3B32'), ('#2E4A66', '#0C3B32'),
                   ('background:rgba(23,42,62,0.55)', 'background:rgba(12,59,50,0.6)'), ('background:rgba(23,42,62,0.72)', 'background:rgba(12,59,50,0.75)'), ('background:rgba(23,42,62,0.45)', 'background:rgba(12,59,50,0.5)')):
        s = s.replace(_x, _y)
    # Accueil (demande de Kévin du 17/11/2026) : le bandeau « Envie de venir ? » au milieu de la page est retiré.
    _m, _r = '  <!-- MID-PAGE FUNNEL ENTRY -->\n', '  <!-- REVIEWS -->\n'
    _w = '  <!-- WHO IS SURF INN FOR -->\n'
    if s.count(_m) == 1:
        _fin = s.index('  </section>\n', s.index(_m)) + len('  </section>\n')
        s = s[:s.index(_m)] + s[_fin:].lstrip('\n')
    # Pages camp (demande de Kévin du 17/11/2026) : sous l'en-tête, la barre « Dates + Créer mon séjour » reste affichée.
    # Elle ne s'efface plus quand un bouton secondaire passe à l'écran, seulement devant le module du haut ou celui du bas.
    s = s.replace("document.querySelectorAll('[data-primary-cta],[data-vers-onglet],[data-verbes]').forEach(el => {",
                  "document.querySelectorAll((this.state.page === 'rio' || this.state.page === 'itacare') ? '[data-nav-top] [data-primary-cta],[data-camp-hero] [data-primary-cta],[data-appel] [data-primary-cta]' : '[data-primary-cta],[data-vers-onglet],[data-verbes]').forEach(el => {")
    # Page À propos (demande de Kévin du 17/11/2026) : sur téléphone, même en-tête que « Pour qui » (photo, puis texte sur fond vert).
    s = s.replace('<section data-about-hero="1" data-hero-immersif="1"', '<section data-about-hero="1" data-who-hero="1" data-hero-immersif="1"')
    # ═══ Retours de Meriem (17/11/2026), variantes choisies par Kévin ═══
    # 1. On parle de « devis dans la journée » plutôt que de « réponse rapide », en gardant « probablement mouillé ».
    _d1, _d2 = 'Your quote within the day, from a real (and probably sandy) person.', 'Your quote within the day, from a real (sandy) person.'
    s = s.replace('A real (and probably sandy) person replies fast.', _d1).replace('A real (sandy) person replies fast.', _d2)
    for _cle in (_d1, _d2):
        _t = _dico(_t, _cle, 'Recevez votre devis dans la journée, par quelqu’un de l’équipe (probablement mouillé).', 'Receba seu orçamento no mesmo dia, por alguém da equipe (depois do surf).')
    # 17/11/2026 : verbe d'action demandé par Kévin (remplace l'ancienne formulation déjà posée)
    _t = _t.replace('Votre devis dans la journée, par quelqu’un', 'Recevez votre devis dans la journée, par quelqu’un').replace('Seu orçamento no mesmo dia, por alguém', 'Receba seu orçamento no mesmo dia, por alguém')
    # 2. Prix des packages, en français : « dès 185 € les 3 nuits » (un prix pour tout le séjour, pas par nuit).
    #    L'anglais et le portugais gardent les deux devises en attendant la décision de Kévin et Lucas.
    _nuits = {'185': 3, '370': 5, '590': 7, '170': 3, '340': 5, '550': 7}
    _t = re.sub(r'"à partir de (\d+)\s€ / [^"]*R\$"', lambda m: '"dès %s € les %d nuits"' % (m.group(1), _nuits[m.group(1)]) if m.group(1) in _nuits else m.group(0), _t)
    _t = re.sub(r'Le prix «\sà partir de\s» correspond', 'Le prix « dès » correspond', _t)
    _note = 'per person, lessons included'
    if 'data-prix-note' not in s:
        s = s.replace('font-size:17px;color:#ED6267;">{{ pk.price }}</span>', 'font-size:17px;color:#ED6267;">{{ pk.price }}</span>\n            <span data-prix-note="1" style="padding:0 24px;">' + _note + '</span>')
        s = s.replace('font-size:16px;color:#ED6267;">{{ pk.price }}</span>', 'font-size:16px;color:#ED6267;">{{ pk.price }}</span>\n                      <span data-prix-note="1">' + _note + '</span>')
    # (la clé devient « per person » plus bas : sans ce test, chaque reconstruction en ajoutait une copie)
    if '\n    "per person": ' not in _t:
        _t = _dico(_t, _note, 'par personne, cours compris', 'por pessoa, aulas incluídas')
    # 3. Étape Options du parcours : une ligne dit qu'on peut ajouter les activités plus tard.
    _opt = 'Add them now or later, once you are here.'
    if 'data-options-note' not in s:
        s = s.replace('margin:0 0 8px;">Extras</h2>', 'margin:0 0 8px;">Extras</h2>\n          <div data-options-note="1">' + _opt + '</div>')
    _t = _dico(_t, _opt, 'À ajouter maintenant ou plus tard, sur place.', 'Adicione agora ou depois, já no camp.')
    # Suite des retours de Meriem (17/11/2026) : la dernière étape du parcours et la note de prix parlent aussi de devis.
    _av, _ap = 'you get a quote and availability as soon as possible, then decide.', 'you get a quote and availability within the day, then decide.'
    s = s.replace(_av, _ap); _t = _t.replace(_av, _ap)
    _t = re.sub(r'vous recevez une proposition et les disponibilités au plus vite', 'vous recevez un devis et les disponibilités dans la journée', _t)
    _t = _t.replace('você recebe uma proposta e a disponibilidade o quanto antes', 'você recebe um orçamento e a disponibilidade no mesmo dia')
    _t = _t.replace('votre prix exact arrive avec la réponse à votre demande', 'votre prix exact arrive avec votre devis')
    # ═══ Retours de Kévin sur ordinateur (17/11/2026) ═══
    # Repères pour le menu des langues (texte crème sur fond crème quand le menu est sur la vidéo) et le pied du calendrier.
    s = s.replace('<div style="position:absolute;top:calc(100% + 8px);right:0;z-index:80;min-width:150px;', '<div data-menu-langues="1" style="position:absolute;top:calc(100% + 8px);right:0;z-index:80;min-width:150px;')
    s = s.replace('<div style="display:flex;align-items:center;justify-content:space-between;gap:12px;margin-top:12px;padding-top:12px;border-top:1px solid rgba(54,140,175,0.14);">\n      <span style="font-size:13px;font-weight:600;color:#4A6A80;white-space:nowrap;">{{ dpHint }}</span>',
                  '<div data-dp-pied="1" style="display:flex;align-items:center;justify-content:space-between;gap:12px;margin-top:12px;padding-top:12px;border-top:1px solid rgba(54,140,175,0.14);">\n      <span style="font-size:13px;font-weight:600;color:#4A6A80;white-space:nowrap;">{{ dpHint }}</span>')
    # Récapitulatif de la demande (17/11/2026, demande de Kévin) : une seule ligne pour la chambre (la chambre choisie,
    # sans répéter « Chambre privée » au-dessus) et les dates sur une seule ligne avec le nombre de nuits.
    _sa = "Stay: [S.stayRoom || 'To pick'].concat(stayOpt ? [stayOpt.label] : []),"
    if _sa in s:
        s = s.replace(_sa, "Stay: stayOptRaw ? [stayOptRaw.label].concat(stayOptRaw.beds ? [stayOptRaw.beds] : []) : [S.stayRoom || 'To pick'],")
    # Audit du 17/11/2026 : le nom de la chambre et le nombre de couchages sont deux textes séparés, pour que chacun soit traduit
    # (« Private triple room · Sleeps 3 » restait en anglais). La feuille de style les remet sur une seule ligne.
    s = s.replace("Stay: stayOpt ? [stayOpt.label] : [S.stayRoom || 'To pick'],", "Stay: stayOptRaw ? [stayOptRaw.label].concat(stayOptRaw.beds ? [stayOptRaw.beds] : []) : [S.stayRoom || 'To pick'],")
    _ra = '<div data-recap-row="1" style="padding:12px 0;'
    if _ra in s:
        s = s.replace(_ra, '<div data-recap-row="1" data-recap-k="{{ r.k }}" style="padding:12px 0;')
    # ── Corrections sûres de l'audit du 17/11/2026 ──
    import re as _re_v
    # 1. Mots restés en anglais sur les pages Hébergement.
    for _cle, _fr, _pt in (('OUTDOORS', 'EXTÉRIEUR', 'ÁREA EXTERNA'), ('GYM', 'SALLE DE SPORT', 'ACADEMIA'),
                           ('Ensuite', 'Salle de bain privée', 'Banheiro privativo'), ('A/C', 'Climatisation', 'Ar-condicionado'),
                           ('Fan / A/C', 'Ventilateur / climatisation', 'Ventilador / ar-condicionado'), ('1st', '1er', '1º')):
        _t = _dico(_t, _cle, _fr, _pt)
    # Guide surf en anglais : « Feriados » était resté en portugais.
    s = s.replace('>Feriados: {{ s.feriados }}<', '>Holidays: {{ s.feriados }}<')
    _t = _dico(_t, 'Holidays:', 'Jours fériés\u00a0:', 'Feriados:')
    # Guides surf : décimales à la française et à la brésilienne dans les hauteurs de vagues (« 0,5–1,2 m »).
    for _v in sorted(set(_re_v.findall(r"waves: '([^']*\d\.\d[^']*)'", s))):
        _t = _dico(_t, _v, _v.replace('.', ','), _v.replace('.', ','))
    # 2. « répond rapidement » : on parle de devis dans la journée (règle posée avec Meriem), sans répéter la phrase placée sous le bouton.
    for _a, _b in (
        ('un membre de notre équipe vous répond rapidement (gratuit et sans engagement).', 'vous recevez votre devis dans la journée (gratuit et sans engagement).'),
        ('notre équipe locale vous envoie rapidement une proposition.', 'notre équipe locale prépare votre séjour avec vous.'),
        ('Une vraie personne vous répond rapidement.', 'Quelqu’un de l’équipe vous répond dans la journée.'),
        ('Indiquez vos dates, votre niveau et vos envies : notre équipe vous répond rapidement.', 'Indiquez vos dates, votre niveau et vos envies : notre équipe prépare votre séjour avec vous.'),
    ):
        _t = _t.replace(_a, _b)
    # 3. Typographie française : espace insécable devant : ; ? ! et à l'intérieur des guillemets, guillemets droits des avis remplacés.
    import re as _re
    _i = _t.index('  "fr": {\n'); _j = _t.index('\n  }', _i)
    def _typo(_l):
        _k = _l.find('": "')
        if _k < 0 or not _l.rstrip().endswith(('",', '"')):
            return _l
        _cle, _val = _l[:_k + 4], _l[_k + 4:]
        _val = _re.sub(r'(?<=[^\s\\]) ([:;?!»])', ' \\1', _val)
        _val = _val.replace('« ', '« ')
        _val = _re.sub(r'^\\"(.+)\\"(",?)$', '« \\1 »\\2', _val)
        return _cle + _val
    _t = _t[:_i] + '\n'.join(_typo(_l) for _l in _t[_i:_j].split('\n')) + _t[_j:]
    # 4. Pages camp, module du bas : la note Google du camp (comme dans l'en-tête), plus le total des deux camps.
    _n = '★ 4.9/5 · {{ googleTotal }} Google reviews</span>'
    _k = s.find('{{ openFunnelCamp }}" data-coral="1"')
    while _k > 0:
        _m = s.find(_n, _k)
        if 0 < _m - _k < 3000:
            s = s[:_m] + '★ {{ camp.google.rating }}/5 · {{ camp.google.count }} Google reviews</span>' + s[_m + len(_n):]
            break
        _k = s.find('{{ openFunnelCamp }}" data-coral="1"', _k + 1)
    # Avis cités sur « Pour qui » et « Travailler et surfer » : les guillemets droits du gabarit laissent la place à des guillemets
    # posés par la feuille de style selon la langue (« » en français, “ ” ailleurs), comme sur l'accueil et la page Avis.
    for _v in ('tm.quote', 'wb.review.text', 'workReview.text'):
        s = s.replace('>"{{ %s }}"</p>' % _v, '><span data-guil="o"></span>{{ %s }}<span data-guil="f"></span></p>' % _v)
    # Référencement et partage (17/11/2026) : titres, descriptions et balises de partage viennent de seo.js, à la racine,
    # qui sert aussi au serveur (middleware.js). Quand on passe d'une page à l'autre sans recharger, le site les met à jour ici.
    _seo_src = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'seo.js'), encoding='utf-8').read()
    _seo_json = json.dumps(json.loads(_seo_src[len('export default '):].rstrip().rstrip(';')), ensure_ascii=False, separators=(',', ':'))
    _ta = "    const t = this.titrePage(page, tab, l);\n    window.__titre = t;"
    if _ta in s:
        s = s.replace(_ta, "    const __seoPages = " + _seo_json + ";\n"
            "    const __seo = __seoPages[location.pathname] || null;\n"
            "    const t = (__seo && __seo.t) || this.titrePage(page, tab, l);\n"
            "    try { const __m = (sel, cree, val) => { let e = document.head.querySelector(sel); if (!e) { e = cree(); document.head.appendChild(e); } e.setAttribute('content', val); };\n"
            "      const __nm = (n) => () => { const e = document.createElement('meta'); e.setAttribute('name', n); return e; }, __pr = (n) => () => { const e = document.createElement('meta'); e.setAttribute('property', n); return e; };\n"
            "      if (__seo) { const img = location.origin + '/assets/partage-' + __seo.i + '.jpg';\n"
            "        __m('meta[name=\"description\"]', __nm('description'), __seo.d); __m('meta[property=\"og:title\"]', __pr('og:title'), __seo.t); __m('meta[property=\"og:description\"]', __pr('og:description'), __seo.d);\n"
            "        __m('meta[property=\"og:url\"]', __pr('og:url'), location.origin + location.pathname); __m('meta[property=\"og:image\"]', __pr('og:image'), img); __m('meta[name=\"twitter:title\"]', __nm('twitter:title'), __seo.t); __m('meta[name=\"twitter:description\"]', __nm('twitter:description'), __seo.d); __m('meta[name=\"twitter:image\"]', __nm('twitter:image'), img); } } catch (e) {}\n"
            "    window.__titre = t;")
    # Images de partage : une seule image par famille de pages, sans texte qui dépende de la langue (décision de Kévin, 17/11/2026).
    s = s.replace("const img = location.origin + '/assets/partage-' + __seo.i + '-' + (location.pathname.indexOf('/fr/') === 0 ? 'fr' : location.pathname.indexOf('/pt/') === 0 ? 'pt' : 'en') + '.jpg';", "const img = location.origin + '/assets/partage-' + __seo.i + '.jpg';")
    # Textes de partage (17/11/2026, validés par Kévin) : dans l'aperçu d'un lien, titre court sans la marque et description de 80 caractères
    # (champs « st » et « sd » de seo.js). L'onglet et la description lue par Google gardent « t » et « d ». Met à jour le code déjà posé.
    s = re.sub(r'const __seoPages = \{.*?\};\n', lambda _m: 'const __seoPages = ' + _seo_json + ';\n', s)
    for _a, _b in (("__pr('og:title'), __seo.t)", "__pr('og:title'), __seo.st || __seo.t)"), ("__pr('og:description'), __seo.d)", "__pr('og:description'), __seo.sd || __seo.d)"),
                   ("__nm('twitter:title'), __seo.t)", "__nm('twitter:title'), __seo.st || __seo.t)"), ("__nm('twitter:description'), __seo.d)", "__nm('twitter:description'), __seo.sd || __seo.d)"),
                   ("'/assets/partage-' + __seo.i + '.jpg'", "'/assets/partage-' + __seo.i + '-v3.jpg'"), ("'/assets/partage-' + __seo.i + '-v2.jpg'", "'/assets/partage-' + __seo.i + '-v3.jpg'")):
        s = s.replace(_a, _b)
    # « Envoyer à un ami » (17/11/2026, emplacement B choisi par Kévin) : un lien discret dans le module du bas des pages camp,
    # sous le bouton et les avis. Le clic est géré par outils/experience/couche.js (partage du téléphone, sinon WhatsApp).
    _pa = '★ {{ camp.google.rating }}/5 · {{ camp.google.count }} Google reviews</span>'
    if _pa in s and 'data-partager="1"' not in s:
        _i = s.index(_pa); _j = s.index('</div>', _i) + len('</div>')
        s = s[:_j] + ('\n      <a data-partager="1" href="#" style="display:flex;align-items:center;justify-content:center;gap:8px;width:max-content;margin:16px auto 0;'
            'color:#FFF8EF;font-weight:700;font-size:16px;text-decoration:underline;text-underline-offset:4px;text-decoration-thickness:1.5px;cursor:pointer;position:relative;z-index:2;">'
            '<svg aria-hidden="true" width="18" height="18" sc-camel-view-box="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;">'
            '<path d="M4 12v7a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-7"></path><path d="M16 6l-4-4-4 4"></path><path d="M12 2v13"></path></svg>'
            '<span>Send to a friend</span></a>') + s[_j:]
    _t = _dico(_t, 'Send to a friend', 'Envoyer à un ami', 'Enviar para um amigo')
    # Suivi : une demande de séjour venue d'un lien partagé le dit (événement de mesure et champ caché du formulaire).
    _ga = "if (!prev.submitted && s.submitted) dl.push({ event: 'generate_lead', destination: s.dest || '' });"
    if _ga in s:
        s = s.replace(_ga, "if (!prev.submitted && s.submitted) dl.push({ event: 'generate_lead', destination: s.dest || '', via: (window.__via || '') });")
    _ha = '<input type="hidden" name="room_option" value="{{ roomOptionCode }}">'
    if _ha in s and 'name="via"' not in s:
        s = s.replace(_ha, _ha + '\n          <input type="hidden" name="via" data-via="1" value="">')
    # Pages Séjours de Rio et d'Itacaré (18/11/2026, demande de Kévin) : les cartes de package reprennent exactement le dessin de celles
    # du parcours de réservation : nom puis durée dessous, liste, prix en bas, bouton en pilule. La jauge et « Inclus » disparaissent.
    _c0 = s.find('<div sc-camel-on-click="{{ camp.createPack }}" style="cursor:pointer;background:#FFFBF3;border:2px solid #234668;')
    _c1 = s.find('Start from this →</span>', _c0)
    if _c0 > 0 and _c1 > 0:
        _c1 = s.index('</sc-for>', _c1) + len('</sc-for>')
        _carte = 'cursor:pointer;background:#FFFBF3;border:2px solid rgba(54,140,175,0.2);border-radius:20px;overflow:hidden;display:flex;flex-direction:column;box-sizing:border-box;'
        _corps = 'padding:16px 18px 18px;display:flex;flex-direction:column;gap:9px;flex-grow:1;'
        _nom = "font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:18px;color:#234668;"
        _btn = 'background:#DEEBF2;color:#234668;padding:11px;border-radius:999px;font-weight:800;text-align:center;font-size:14.5px;'
        s = s[:_c0] + (
            '<div sc-camel-on-click="{{ camp.createPack }}" data-carte-pack="1" style="' + _carte + '" style-hover="border:2px solid #ED6267;">\n'
            '          <div style="position:relative;aspect-ratio:16/9;background:#DEEBF2;display:flex;align-items:center;justify-content:center;"><span style="width:56px;height:56px;border-radius:50%;background:#234668;color:#FFF8EF;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:30px;line-height:1;">+</span></div>\n'
            '          <div style="' + _corps + '">\n'
            '            <span style="' + _nom + '">Build my own</span>\n'
            '            <p style="margin:0;font-size:14px;line-height:1.4;color:#4A6A80;flex-grow:1;">Start from your room and add what you want.</p>\n'
            '            <span style="' + _btn + '">Select</span>\n'
            '          </div>\n'
            '        </div>\n'
            '        <sc-for list="{{ camp.packages }}" as="pk" hint-placeholder-count="3">\n'
            '          <div data-carte-pack="1" sc-camel-on-click="{{ pk.pick }}" style="' + _carte + '" style-hover="border:2px solid #ED6267;">\n'
            '            <div style="position:relative;aspect-ratio:16/9;background:linear-gradient(160deg,#368CAF,#84C8E7);">\n'
            '              <sc-if value="{{ pk.img }}" hint-placeholder-val="{{ false }}"><img src="{{ pk.img }}" alt="" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{{ pk.pos }};"></sc-if>\n'
            '            </div>\n'
            '            <div style="' + _corps + '">\n'
            '              <div style="display:flex;flex-direction:column;align-items:flex-start;gap:6px;">\n'
            '                <span style="' + _nom + '">{{ pk.name }}</span>\n'
            '                <span style="background:#DEEBF2;color:#234668;font-size:12px;font-weight:800;padding:4px 10px;border-radius:999px;white-space:nowrap;">{{ pk.duration }}</span>\n'
            '              </div>\n'
            '              <ul style="list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:5px;flex-grow:1;">\n'
            '                <sc-for list="{{ pk.bullets }}" as="b" hint-placeholder-count="3">\n'
            '                  <li style="display:flex;align-items:flex-start;gap:9px;font-size:14px;line-height:1.4;color:#234668;font-weight:600;"><span style="width:6px;height:6px;border-radius:50%;background:#ED6267;flex:none;margin-top:7px;"></span><span>{{ b }}</span></li>\n'
            '                </sc-for>\n'
            '              </ul>\n'
            '              <span data-coral-text="1" style="font-family:\'Bricolage Grotesque\',sans-serif;font-weight:800;font-size:16px;color:#ED6267;">{{ pk.price }}</span>\n'
            '              <span data-prix-note="1">per person, lessons included</span>\n'
            '              <span style="' + _btn + '">Select</span>\n'
            '            </div>\n'
            '          </div>\n'
            '        </sc-for>') + s[_c1:]
    # Pages Séjours (20/11/2026, demande de Kévin) : seule la pilule « Choisir » ouvre le parcours, plus toute la carte.
    # La bordure de survol de la carte disparaît aussi : sur téléphone elle restait affichée après un retour du parcours.
    for _clic in ('{{ camp.createPack }}', '{{ pk.pick }}'):
        _m = re.search(r'<div (?:sc-camel-on-click="' + re.escape(_clic) + r'" data-carte-pack="1"|data-carte-pack="1" sc-camel-on-click="' + re.escape(_clic) + r'") style="cursor:pointer;([^"]*)" style-hover="[^"]*">', s)
        if _m:
            s = s[:_m.start()] + '<div data-carte-pack="1" style="' + _m.group(1) + '">' + s[_m.end():]
            _b = re.compile(r'<span style="([^"]*)">Select</span>').search(s, _m.start())
            s = s[:_b.start()] + '<span data-choisir="1" sc-camel-on-click="' + _clic + '" style="cursor:pointer;' + _b.group(1) + '" style-hover="filter:brightness(0.94);">Select</span>' + s[_b.end():]
    # Pages légales (18/11/2026) : informations légales, confidentialité, conditions de réservation. Contenu dans outils/legal.py.
    sys.path.insert(0, ICI)
    import legal as _lg
    _nb = lambda _x: re.sub(r' ([:;?!»])', ' \\1', _x).replace('« ', '« ')
    def _tx3(_t, _e):
        return _dico(_t, _e[0], _nb(_e[1]), _e[2])
    if "legal: { en: 'legal/'" not in s:
        s = s.replace("    contact: { en: 'contact/', fr: 'contact/', pt: 'contato/' },\n",
                      "    contact: { en: 'contact/', fr: 'contact/', pt: 'contato/' },\n" + ''.join("    %s: { en: '%s', fr: '%s', pt: '%s' },\n" % (_k, _v['route']['en'], _v['route']['fr'], _v['route']['pt']) for _k, _v in _lg.PAGES.items()))
        s = s.replace("isContact: page === 'contact',", "isContact: page === 'contact', isLegal: page === 'legal', isPrivacy: page === 'privacy', isTerms: page === 'terms',")
        s = s.replace("linkFaq: this.lienVers('faq'),", "linkFaq: this.lienVers('faq'), linkLegal: this.lienVers('legal'), linkPrivacy: this.lienVers('privacy'), linkTerms: this.lienVers('terms'), hrefLegal: this.adresse('legal', null, this.state.lang), hrefPrivacy: this.adresse('privacy', null, this.state.lang), hrefTerms: this.adresse('terms', null, this.state.lang),")
        _H2 = "font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:22px;color:#234668;margin:34px 0 12px;"
        _H3 = "font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:18px;color:#234668;margin:22px 0 8px;"
        _P = 'font-size:16px;line-height:1.6;color:#33566E;margin:0 0 12px;'
        _html = ''
        for _k, _v in _lg.PAGES.items():
            _flag = {'legal': 'isLegal', 'privacy': 'isPrivacy', 'terms': 'isTerms'}[_k]
            _c = ''; _ul = False
            for _e in _v['corps']:
                if _e[0] == 'li' and not _ul:
                    _c += '      <ul style="margin:0 0 12px;padding:0 0 0 20px;display:flex;flex-direction:column;gap:6px;">\n'; _ul = True
                if _e[0] != 'li' and _ul:
                    _c += '      </ul>\n'; _ul = False
                if _e[0] == 'h2': _c += '      <h2 style="%s">%s</h2>\n' % (_H2, _e[1])
                elif _e[0] == 'h3': _c += '      <h3 style="%s">%s</h3>\n' % (_H3, _e[1])
                elif _e[0] == 'p': _c += '      <p style="%s">%s</p>\n' % (_P, _e[1])
                else: _c += '        <li style="font-size:16px;line-height:1.55;color:#33566E;">%s</li>\n' % _e[1]
            if _ul: _c += '      </ul>\n'
            _html += ('<sc-if value="{{ %s }}" hint-placeholder-val="{{ false }}">\n<main data-screen-label="Legal" data-page-legale="%s">\n'
                      '  <section style="padding:clamp(56px,8vw,90px) clamp(24px,5vw,72px) clamp(64px,9vw,110px);">\n    <div style="max-width:760px;margin:0 auto;">\n'
                      '      <p style="font-weight:700;font-size:14px;letter-spacing:0.14em;text-transform:uppercase;color:{{ camp.accent }};margin:0 0 12px;">%s</p>\n'
                      '      <h1 style="font-family:\'Bricolage Grotesque\',sans-serif;font-weight:800;font-size:clamp(32px,4.6vw,54px);line-height:1.05;color:#234668;margin:0 0 14px;text-wrap:pretty;">%s</h1>\n'
                      '      <p style="font-size:17px;line-height:1.55;color:#4A6A80;margin:0 0 8px;">%s</p>\n'
                      '      <p style="font-size:14px;line-height:1.5;color:#7E97A8;margin:0 0 6px;">%s</p>\n'
                      '      <p data-legal-ref="1" style="font-size:14px;line-height:1.5;color:#7E97A8;margin:0 0 10px;">%s</p>\n%s'
                      '    </div>\n  </section>\n</main>\n</sc-if>\n') % (_flag, _k, _v['sur'][0], _v['titre'][0], _v['intro'][0], _lg.MAJ[0], _lg.REF[0], _c)
        _anc = '<sc-if value="{{ isFaq }}" hint-placeholder-val="{{ false }}">\n<main data-screen-label="FAQ">'
        s = remplace(s, _anc, _html + _anc)
        _ct = '<a href="{{ hrefContact }}" sc-camel-on-click="{{ linkContact }}" style="cursor:pointer;color:#B8CBD4;" style-hover="color:#F7F4EA;">Contact</a>'
        _liens = ''.join('\n    <a href="{{ href%s }}" sc-camel-on-click="{{ link%s }}" style="cursor:pointer;color:#B8CBD4;" style-hover="color:#F7F4EA;">%s</a>' % (_n, _n, _lib) for _n, _lib in (('Legal', 'Legal information'), ('Privacy', 'Privacy policy'), ('Terms', 'Booking terms')))
        if s.count(_ct) == 1:
            s = s.replace(_ct, _ct + _liens)
    for _k, _v in _lg.PAGES.items():
        for _e in (_v['sur'], _v['titre'], _v['intro'], _lg.MAJ, _lg.REF):
            _t = _tx3(_t, _e)
        for _e in _v['corps']:
            _t = _tx3(_t, _e[1:])
    # 18/11/2026, demande de Kévin : à l'arrivée, il ne reste que la fenêtre des cookies.
    # Le bandeau « Ce site existe en français » n'a plus lieu d'être : le site s'ouvre dans la langue de l'appareil (script en tête de index.html).
    s = s.replace("  banniereLangue(courante) {\n    try { if (localStorage.getItem('surfinn.banniere') === 'non') return; } catch (e) {}",
                  "  banniereLangue(courante) {\n    return; // bandeau retiré le 18/11/2026\n    try { if (localStorage.getItem('surfinn.banniere') === 'non') return; } catch (e) {}")
    # La fenêtre « E aí, brasileiro? » réservée aux visiteurs au Brésil ne s'ouvre plus.
    s = s.replace("    if (this.isBrazilian() && !this.brPopupSeen()) this._brPopupTimer = setTimeout(() => this.tryBrPopup(), this.BR_POPUP_DELAY_MS);",
                  "    // Fenêtre brésilienne retirée le 18/11/2026 (demande de Kévin).")
    # Lot anglais (17/11/2026, validé par Kévin) : l'anglais est réaligné sur le français réécrit. Chaque phrase change dans le gabarit
    # ET dans la clé du dictionnaire (les clés sont le texte anglais exact), pour que le français et le portugais suivent.
    def _en(_s, _d, frag, nouv):
        _cles = set()
        for _m in re.finditer(r'\n    ("(?:[^"\\]|\\.)*"):', _d):
            try:
                _k = json.loads(_m.group(1))
            except Exception:
                continue
            if frag in _k:
                _cles.add(_k)
        for _k in _cles:
            _k2 = _k.replace(frag, nouv)
            for _f in (lambda x: x, lambda x: x.replace("'", "\\'"), lambda x: x.replace('&', '&amp;')):
                _s = _s.replace(_f(_k), _f(_k2))
            for _ascii in (False, True):
                _d = _d.replace('\n    ' + json.dumps(_k, ensure_ascii=_ascii) + ':', '\n    ' + json.dumps(_k2, ensure_ascii=_ascii) + ':')
        for _f in (lambda x: x, lambda x: x.replace("'", "\\'")):
            _s = _s.replace(_f(frag), _f(nouv))
        return _s, _d
    for _a, _b in (
        ('Chat with us', 'Message us on WhatsApp'),
        ('Our two houses', 'Rio de Janeiro and Itacaré'),
        ('Home on the beach', 'Lodging by the beach'), ('Like-minded crew', 'No compulsory lessons'),
        ("Recreio, Rio's best-kept secret", "Recreio, Rio's surf neighborhood"),
        ('From beginner to world-class waves', 'From first waves to powerful peaks'),
        ('Heaven for longboards', 'A wave made for longboards'),
        ('We are beyond the surf camp business.', 'A Brazilian surf camp, founded by Brazilians.'),
        ('What our hearts beat for', 'What we care about'),
        ("Here's who thrives here, honestly.", "Here's who it's for."), ('Who Surf Inn is for.', "Here's who it's for."),
        ('Tell us your dates and your level, our local team builds your Rio stay around you.', 'Tell us your dates, your level and what you want: our team builds your Rio stay with you.'),
        ('Tell us your dates and your level, our local team builds your Itacaré stay around you.', 'Tell us your dates, your level and what you want: our team builds your Itacaré stay with you.'),
        ('comes with your request', 'comes with your quote'),
        ('neighbourhood', 'neighborhood'), ('Neighbourhood', 'Neighborhood'), ('organise', 'organize'),
    ):
        s, _t = _en(s, _t, _a, _b)
    # Le bouton principal : on promet un devis gratuit, pas une réservation. L'étiquette technique « Request to book, funnel » ne change pas.
    s = re.sub(r'Request to book(?!, funnel)', 'Build my stay', s)
    _t = re.sub(r'Request to book(?!, funnel)', 'Build my stay', _t)
    # Packages (18/11/2026, demande de Kévin) : la ligne des nuits tient sur une seule ligne et dit que l'hébergement est inclus,
    # sans « en chambre partagée ou privée ». Elle est affichée partout, téléphone compris.
    s, _t = _en(s, _t, ' nights in a shared or private room', ' nights of accommodation')
    _t = _t.replace(' nuits en chambre partagée ou privée', ' nuits d’hébergement').replace(' noites em quarto compartilhado ou privativo', ' noites de hospedagem')
    # Packages, prix et description (18/11/2026, échange avec Kévin) : le prix tient sur une ligne et dit qu'il est par personne ;
    # la note « par personne, cours compris » disparaît en français (les cours sont dans la liste, la durée dans la pastille).
    # En anglais et en portugais, où le prix porte encore deux devises, la note reste, réduite à « per person » / « por pessoa ».
    _t = re.sub(r'"dès (\d+) € les \d nuits"', lambda _m: '"dès %s € par personne"' % _m.group(1), _t)
    s, _t = _en(s, _t, 'per person, lessons included', 'per person')
    _t = _t.replace('"per person": "par personne, cours compris"', '"per person": "par personne"').replace('"per person": "por pessoa, aulas incluídas"', '"per person": "por pessoa"')
    # Copies accumulées par les reconstructions précédentes (18/11/2026) : une seule entrée par langue
    for _l in ('    "per person": "par personne",\n', '    "per person": "por pessoa",\n'):
        _k = _t.find(_l)
        if _k >= 0:
            _t = _t[:_k + len(_l)] + _t[_k + len(_l):].replace(_l, '')
    # Description de la page Séjours : une phrase, qui dit que tout reste ajustable.
    s, _t = _en(s, _t, 'Build it yourself, or start from one of three tried-and-true formulas. Nothing is locked, our local team adjusts everything afterwards.', 'Nothing is locked: you can adjust everything after sending your request.')
    for _a, _b in (('Composez votre séjour vous-même, ou partez de l’un de nos trois packages, de 3 à 7 nuits. Rien n’est figé\u00a0: notre équipe locale ajuste tout ensuite.', 'Rien n’est figé\u00a0: vous ajustez tout après l’envoi de votre demande.'),
                   ('Composez votre séjour vous-même, ou partez de l’un de nos trois packages, de 3 à 7 nuits. Rien n’est figé : notre équipe locale ajuste tout ensuite.', 'Rien n’est figé\u00a0: vous ajustez tout après l’envoi de votre demande.'),
                   ('Monte sua estadia sozinho ou parta de um dos nossos 3 pacotes. Nada fica travado.', 'Nada fica travado: dá para ajustar tudo depois de enviar o pedido.')):
        _t = _t.replace(_a, _b)
    # Anglais et portugais alignés sur le français récent (18/11/2026, demande de Kévin) : devis dans la journée plutôt que « réponse
    # rapide », titre de la page Séjours, petites capitales et heures en anglais, « o Surf Inn » partout en portugais.
    for _a, _b in (
        ('someone from our team replies fast (free, no commitment)', 'you get your quote within the day (free, no commitment)'),
        ('A real person gets back to you fast with a quote.', 'Our local team builds your stay with you.'),
        ('A real person answers fast.', 'Someone from the team replies within the day.'),
        ("✓ Sent, we'll reply fast", "✓ Sent, we'll reply within the day"),
        ('who gets back to you as soon as possible. You decide after the quote.', 'who sends your quote within the day. You decide after that.'),
        ('Our local team will get back to you directly, as soon as possible, with a proposal built around your request.', 'Our local team will send you a quote built around your request within the day.'),
        ('Surf lessons: pick a package. Or create your own.', 'Your stay: pick a package, or build your own.'),
        (' Surf lesson', ' surf lesson'), (' Yoga lesson', ' yoga lesson'), ('1 Surf guidance', '1 surf guiding session'), ('1 Surfskate', '1 surfskate session'),
        ('until 4 pm', 'until 16:00'),
    ):
        s, _t = _en(s, _t, _a, _b)
    for _a, _b in (
        ('✓ Message envoyé, réponse rapide', '✓ Message envoyé, réponse dans la journée'),
        ('qui vous répond au plus vite. Vous décidez après avoir reçu la proposition.', 'qui vous envoie votre devis dans la journée. Vous décidez ensuite.'),
        ('Notre équipe locale va vous répondre directement, au plus vite, avec une proposition construite sur votre demande.', 'Notre équipe locale vous envoie dans la journée un devis construit sur votre demande.'),
        ('alguém da nossa equipe responde rápido (', 'você recebe seu orçamento no mesmo dia ('), ('alguém da nossa equipe responde rapidinho (', 'você recebe seu orçamento no mesmo dia ('),
        ('A gente responde rapidinho com uma proposta.', 'A nossa equipe local monta a sua estadia com você.'),
        ('A nossa equipe responde rapidinho.', 'A nossa equipe monta a sua estadia com você.'),
        ('Uma pessoa de verdade responde rapidinho.', 'Alguém da equipe responde no mesmo dia.'),
        ('✓ Enviado, a gente responde rápido', '✓ Enviado, a gente responde no mesmo dia'),
        ('que responde o quanto antes. Você decide depois de receber a proposta.', 'que manda seu orçamento no mesmo dia. Você decide depois.'),
        ('Nossa equipe local vai te responder diretamente, o quanto antes, com uma proposta montada a partir do seu pedido.', 'Nossa equipe local envia no mesmo dia um orçamento montado a partir do seu pedido.'),
        ('é confirmado na nossa proposta', 'é confirmado no seu orçamento'), ('junto com a proposta', 'junto com o orçamento'), ('a equipe prepara a proposta', 'a equipe prepara o orçamento'),
        ('Muito além de aulas de surf. Escolha um pacote ou crie o seu.', 'Sua estadia: escolha um pacote ou monte o seu.'),
    ):
        _t = _t.replace(_a, _b)
    _pi = _t.index('  "pt": {\n'); _pj = _t.index('\n  }', _pi)
    _pt = _t[_pi:_pj]
    for _a, _b in ((' na Surf Inn', ' no Surf Inn'), (' da Surf Inn', ' do Surf Inn'), (' à Surf Inn', ' ao Surf Inn'), (' é a Surf Inn', ' é o Surf Inn'), ('Com a Surf Inn', 'Com o Surf Inn'), (' pela Surf Inn', ' pelo Surf Inn')):
        _pt = re.sub(r'(": "(?:[^"\\]|\\.)*?)' + re.escape(_a), lambda _m: _m.group(1) + _b, _pt)
        while re.search(r'": "(?:[^"\\]|\\.)*?' + re.escape(_a), _pt):
            _pt = re.sub(r'(": "(?:[^"\\]|\\.)*?)' + re.escape(_a), lambda _m: _m.group(1) + _b, _pt)
    _t = _t[:_pi] + _pt + _t[_pj:]
    # Activités (18/11/2026, demande de Kévin) : cartes sans sous-description, introduction en une phrase, descriptions courtes et
    # factuelles dans la fenêtre de photos (outils/activites.py), sans formule du type « ici, on comprend ce que veut dire ginga ».
    sys.path.insert(0, ICI)
    import activites as _ac
    for _titre, _anc, _n_en, _n_fr, _n_pt in _ac.ACTIVITES:
        for _vieux in _anc:
            if _vieux == _n_en:
                continue
            for _f in (lambda x: x, lambda x: x.replace("'", "\\'")):
                s = s.replace("'" + _f(_vieux) + "'", "'" + _f(_n_en) + "'")
        _t = _dico(_t, _n_en, re.sub(r' ([:;?!»])', ' \\1', _n_fr), _n_pt)
    for _v in ('ex', 'dc'):
        s = s.replace('\n              <span style="font-size:13px;line-height:1.35;color:#F7F4EA;">{{ %s.line }}</span>' % _v, '')
        s = s.replace('\n              <span style="font-size:13px;line-height:1.35;color:#FFF8EF;">{{ %s.line }}</span>' % _v, '')
    _gs = s.find('<sc-if value="{{ galSub }}"')
    if _gs > 0:
        _ge = s.index('</sc-if>', _gs) + len('</sc-if>')
        s = s[:_gs] + s[_ge:]
    s, _t = _en(s, _t, 'Core experiences are what we run at the camp. Discovery is what you can add to your trip, with people from here.', 'Capoeira, percussion, hikes, days out with people from here: surfing is only the starting point.')
    s, _t = _en(s, _t, 'days out with people from here: surfing is only the starting point.', 'days out with locals: surfing is only the starting point.')
    _t = _t.replace('sorties avec des gens d’ici\u00a0: le surf', 'sorties avec des habitants\u00a0: le surf').replace('passeios com gente daqui: o surf', 'passeios com moradores: o surf')
    # Même vocabulaire partout (18/11/2026) : plus de « vagues vertes » ni de « d'ici », dans les trois langues.
    s, _t = _en(s, _t, 'Easy paddling, first green waves.', 'Easy paddling, to catch more waves.')
    _t = _t.replace('Une rame facile pour les premières vagues vertes.', 'Une rame facile pour prendre plus de vagues.').replace('Remada fácil para as primeiras ondas.', 'Remada fácil para pegar mais ondas.')
    s, _t = _en(s, _t, 'Gentle starts at Concha and Itacarezinho, warm water, soft boards, and green waves sooner than you think.', 'Start gently at Concha and Itacarezinho, on a soft board, in warm water, with your coach always beside you.')
    s, _t = _en(s, _t, 'Tell us what you want to add, we organize it with people from here.', 'Each of these experiences can be added to your stay, à la carte.')
    s, _t = _en(s, _t, 'the music, the people from here and local activities.', 'the music, local life and its activities.')
    _t = _t.replace('a música, as pessoas daqui e as atividades locais.', 'a música, a vida local e suas atividades.')
    _t = _t.replace('com um guia daqui', 'com um guia local').replace('Um guia daqui lê', 'Um guia local lê').replace('com gente daqui"', 'com moradores"')
    _t = _t.replace('Entre deux sessions, le séjour continue, du côté que peu de touristes connaissent : rodas de capoeira, percussions, randonnées, sorties avec des locaux. Le surf n’est que le point de départ.', 'Capoeira, percussions, randonnées, sorties avec des gens d’ici : le surf n’est que le point de départ.')
    _t = re.sub(r'("Capoeira, percussion, hikes, days out with people from here: surfing is only the starting point\.": ")(?!Capoeira, percussions)[^"]*(",?\n)(?=(?:.|\n)*?"pt": \{)', lambda _m: _m.group(1) + 'Capoeira, percussions, randonnées, sorties avec des gens d’ici : le surf n’est que le point de départ.' + _m.group(2), _t, count=1)
    _pi2 = _t.index('  "pt": {\n')
    _t = _t[:_pi2] + re.sub(r'("Capoeira, percussion, hikes, days out with people from here: surfing is only the starting point\.": ")[^"]*(")', lambda _m: _m.group(1) + 'Capoeira, percussão, trilhas, passeios com gente daqui: o surf é só o ponto de partida.' + _m.group(2), _t[_pi2:], count=1)
    # Fenêtre des activités (18/11/2026, demande de Kévin) : arrivé à la dernière activité d'une catégorie,
    # on passe à la première de l'autre catégorie (et l'inverse en reculant), au lieu de revenir au début.
    if 'alt: _galAlt' not in s:
        _a = "    const coreCards = coreList.map("
        s = remplace(s, _a, "    const _galIt = (x) => ({ title: x.title, desc: x.desc || null, img: x.img || null, shot: x.shot || null, extra: x.extra || null, sub: x.line || null });\n    const _galAlt = (lequel) => { const d = camp.discovery || []; if (!d.length || !coreList.length) return null; return lequel === 'core' ? { section: 'Core experiences', items: coreList.map(_galIt) } : { section: camp.discoveryTitle || 'Discovery', items: d.map(_galIt) }; };\n" + _a)
        s = remplace(s, "sub: x.line })), i, dest: this.state.page } }) }));\n    const discoveryList", "sub: x.line })), i, alt: _galAlt('discovery'), dest: this.state.page } }) }));\n    const discoveryList")
        s = remplace(s, "extra: null, sub: x.line || null })), i, dest: this.state.page } }) }));", "extra: null, sub: x.line || null })), i, alt: _galAlt('core'), dest: this.state.page } }) }));")
        s = remplace(s, "const g = s.gallery, n = g.kind === 'exp' ? g.items.length : g.slides.length; return {", "const g = s.gallery, n = g.kind === 'exp' ? g.items.length : g.slides.length; if (g.kind === 'exp' && g.alt && (g.i + d >= n || g.i + d < 0)) return { gallery: Object.assign({}, g, { section: g.alt.section, items: g.alt.items, alt: { section: g.section, items: g.items }, i: d > 0 ? 0 : g.alt.items.length - 1, __pre: 0 }) }; return {")

    # Menu principal sur ordinateur (18/11/2026, demande de Kévin) : « Nos surf camps » reçoit le même petit motif que
    # « Notre concept », affiché quand on est sur une page de camp.
    s = re.sub(r'<svg data-wave="1" data-vague-camps="1".*?</svg>', '', s)
    if 'data-motif-camps' not in s:
        _m = re.search(r'Our concept.*?((?:<svg data-motif=.*?</svg>)+)', s, re.S)
        if not _m:
            sys.exit('Motif du menu introuvable')
        _i = s.index('data-on="{{ navCampsOn }}" sc-camel-on-click="{{ toggleCampsMenu }}"')
        _j = s.index('</button>', _i)
        s = s[:_j] + _m.group(1).replace('<svg data-motif=', '<svg data-motif-camps="1" data-motif=') + s[_j:]

    # « Que faire à… » (18/11/2026, demande de Kévin) : chaque activité de la seconde catégorie reçoit une description
    # dans la fenêtre, écrite comme celles de « L'essentiel » (une phrase qui commence par un verbe d'action).
    _DECOUVERTES = (
        # Rio
        {'Hikes & viewpoints': ('Hike up to Pedra do Telégrafo and along the wild coast west of the city.', 'Montez à la Pedra do Telégrafo et longez la côte sauvage à l’ouest de la ville.', 'Suba até a Pedra do Telégrafo e percorra o litoral selvagem a oeste da cidade.'),
         'Samba nights in Lapa': ('Spend an evening at a roda de samba in Lapa.', None, None),
         'Fishing with locals': ('Head out at dawn with local fishermen, when the sea is calm.', None, None),
         'A day in Rio': ('Visit Rio in a day with a local guide: Christ the Redeemer, the Selarón Steps and Sugarloaf Mountain.', None, None),
         'Favela tour with a local guide': ('Visit a favela in Rio, such as Rocinha or Vidigal, with a local guide.', None, None),
         'Footvolley & altinha': ('Try footvolley and altinha, the favourite beach sports of Rio’s locals.', None, None)},
        # Itacaré
        {'Whale watching': ('Watch humpback whales from a boat, from July to October, when the sea allows it.', None, None),
         'Rafting with locals': ('Raft down the Rio de Contas, through the Atlantic forest, with a local crew.', None, None),
         'Waterfall hikes': ('Hike through the jungle to the waterfalls around Itacaré, and swim there.', None, None),
         'Fishing with locals': ('Head out at dawn with the fishermen of Itacaré, when the sea is calm.', None, None),
         'Cacao farm': ('Visit a cacao farm and its cooperative, from the pod to the chocolate.', None, None),
         'Moqueca & Bahian cooking': ('Taste moqueca, the Bahian fish stew with dendê oil and coconut milk, cooked in a clay pot.', 'Goûtez la moqueca, le ragoût de poisson bahianais à l’huile de dendê et au lait de coco, cuit dans un plat en terre.', 'Prove a moqueca, o ensopado de peixe baiano com dendê e leite de coco, feito na panela de barro.')},
    )
    _pos = [m.start() for m in re.finditer(r'discovery: \[', s)]
    if len(_pos) != 2:
        sys.exit('Listes « Que faire à… » introuvables')
    for _k in (1, 0):
        _a = _pos[_k]; _b = s.index('\n      ],', _a)
        _bl = s[_a:_b]
        for _titre, (_d_en, _d_fr, _d_pt) in _DECOUVERTES[_k].items():
            _rep = "{ title: '" + _titre + "', "
            if _bl.count(_rep) != 1:
                sys.exit('Activité introuvable : ' + _titre)
            if _rep + 'desc: ' not in _bl:
                _bl = _bl.replace(_rep, _rep + "desc: '" + _d_en + "', ")
            if _d_fr:
                _t = _dico(_t, _d_en, re.sub(r' ([:;?!»])', ' \\1', _d_fr), _d_pt)
        s = s[:_a] + _bl + s[_b:]

    _t = _t.replace('avec un guide d’ici"', 'avec un guide local"')
    # Carte « Travailler » de « Pour qui » (18/11/2026, demande de Kévin) : texte raccourci, sans le fuseau horaire.
    _trav = ('Surf Inn is an ideal place to work: everything is set up for remote workers. High-speed internet (Starlink), a quiet coworking corner for calls, rooms with a desk on request, and a timezone (GMT-3) that leaves your afternoons free on European hours, and your mornings on North American ones.',
             'Everything is set up for remote work: high-speed internet (Starlink), a quiet coworking corner for calls, and rooms with a desk on request.')
    s, _t = _en(s, _t, _trav[0], _trav[1])
    _t = _t.replace('Surf Inn est un lieu idéal pour travailler : tout est prévu pour ceux qui travaillent à distance. Internet haut débit (Starlink), un coin coworking au calme pour les appels, des chambres avec bureau sur demande, et un fuseau horaire (GMT-3) qui laisse les après-midi libres quand on travaille aux horaires européens, et les matinées aux horaires nord-américains.', 'Tout est prévu pour travailler à distance : internet haut débit (Starlink), un coin coworking au calme pour les appels et des chambres avec bureau sur demande.')
    _t = _t.replace('O Surf Inn é um lugar ideal para trabalhar: tudo é pensado para quem trabalha remoto. Internet de alta velocidade (Starlink), um canto de coworking tranquilo para as calls, quartos com mesa sob pedido e um fuso (GMT-3) que deixa as tardes livres para quem trabalha no horário europeu, e as manhãs no horário norte-americano.', 'Tudo é pensado para quem trabalha remoto: internet de alta velocidade (Starlink), um canto de coworking tranquilo para as calls e quartos com mesa sob pedido.')

    # Intitulés d'ouverture (18/11/2026, demande de Kévin) : la page Activités s'ouvre sur « Activités » (et non « Expériences »),
    # la page Hébergement de Rio sur « Hébergement » (« Votre séjour » prêtait à confusion avec la page Séjours).
    s = s.replace('margin:0 0 12px;">Experiences</p>\n      <h2 style="font-family:\'Bricolage Grotesque\',sans-serif;font-weight:800;font-size:clamp(30px,4vw,48px);line-height:1.08;margin:0 0 14px;color:#234668;text-wrap:pretty;max-width:820px;">{{ camp.expTitle }}', 'margin:0 0 12px;">Activities</p>\n      <h2 style="font-family:\'Bricolage Grotesque\',sans-serif;font-weight:800;font-size:clamp(30px,4vw,48px);line-height:1.08;margin:0 0 14px;color:#234668;text-wrap:pretty;max-width:820px;">{{ camp.expTitle }}')
    s = s.replace("overline: 'Your stay', title: 'Surf Inn Rio", "overline: 'Accommodation', title: 'Surf Inn Rio")
    # Conditions de réservation (18/11/2026, demande de Kévin) : la phrase sur la place gardée 24 heures est retirée
    # (délai non confirmé). Elle est aussi retirée de outils/legal.py ; cette ligne l'enlève d'un gabarit déjà construit.
    s = re.sub(r'[ \t]*<p[^>]*>Once we send you the payment link, your place is held for 24 hours\.[^<]*</p>\n?', '', s)
    # Titre de l'activité pêche (18/11/2026, demande de Kévin) : « Sortie pêche », plus simple.
    _t = _t.replace('": "Pêche avec les pêcheurs du quartier"', '": "Sortie pêche"').replace('": "Pesca com os pescadores do bairro"', '": "Passeio de pesca"')
    # Sous les cartes d'activités (18/11/2026) : « activités » et non « expériences », comme le reste de la page.
    s, _t = _en(s, _t, 'Each of these experiences can be added to your stay, à la carte.', 'Each of these activities can be added to your stay, à la carte.')
    _t = _t.replace('Chacune de ces expériences s’ajoute à votre séjour, à la carte.', 'Chacune de ces activités s’ajoute à votre séjour, à la carte.').replace('Cada uma dessas experiências se acrescenta à sua estadia, à la carte.', 'Cada uma dessas atividades se acrescenta à sua estadia, à la carte.')
    # Rio en portugais (18/11/2026) : « os melhores picos da cidade a pé » contredisait le guide (Prainha est à 10 minutes en voiture).
    _t = _t.replace('Aulas de surf com 3 alunos por professor e os melhores picos da cidade a pé.', 'Aulas de surf com 3 alunos por professor e alguns dos picos mais conhecidos da cidade a poucos minutos.')
    # Yoga à Itacaré (18/11/2026, décision de Kévin) : « Yoga tous les jours », sans « inclus », puisque les packages comptent les cours.
    s, _t = _en(s, _t, 'Yoga every day, included, and a gym', 'Yoga every day, and a gym')
    _t = _t.replace('"Yoga inclus tous les jours, et une salle de sport"', '"Yoga tous les jours, et une salle de sport"').replace('"Yoga incluído todo dia, e uma academia"', '"Yoga todo dia, e uma academia"')
    # Parcours de réservation (18/11/2026) : les repères de sélection de Bahia (contour, petite vague, dates) passent de
    # l'orange vif à l'orange de la charte.
    s = s.replace("'#E3711C'", "'#B8520F'")
    # Parcours de réservation (18/11/2026, demande de Kévin) : quand on est amené vers un bloc à remplir, son haut reste visible.
    # Avant, le bloc était centré dans l'écran : sur téléphone, un bloc plus haut que l'écran (les réglages de « Composer mon
    # séjour ») se retrouvait avec son début caché sous l'en-tête du parcours. Désormais, un bloc trop haut est calé par le haut.
    s = s.replace("      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });\n    }, 80);",
                  "      if (!el) return;\n      const grand = el.getBoundingClientRect().height > root.clientHeight - 96;\n      el.scrollIntoView({ behavior: 'smooth', block: grand ? 'start' : 'center' });\n    }, 80);")
    # Onglets des pages camp (18/11/2026) : au changement d'onglet, on arrive avec la barre d'onglets collée tout en haut et le
    # début de la page juste dessous. Avant, le calcul retirait 81 px pour le menu principal, alors que ce menu s'efface
    # dès que la barre d'onglets arrive en haut : il restait une bande de la photo d'ouverture au-dessus de la barre
    # (81 px sur ordinateur, 23 px sur téléphone). On mesure la position naturelle de la barre, sans son effet collant.
    s = s.replace("      const a = document.getElementById('camp-tabbar-anchor');\n      if (a) window.scrollTo({ top: Math.max(0, a.getBoundingClientRect().top + window.scrollY - 81) });",
                  "      const a = document.getElementById('camp-tabbar-anchor'), b = document.getElementById('camp-tabbar');\n      if (b) { const p0 = b.style.position; b.style.position = 'static'; const y = b.getBoundingClientRect().top + window.scrollY; b.style.position = p0; window.scrollTo({ top: Math.max(0, Math.round(y)) }); }\n      else if (a) window.scrollTo({ top: Math.max(0, a.getBoundingClientRect().top + window.scrollY - 81) });")
    # Cookiebot désactivé (18/11/2026, décision de Kévin : commercialisation au Brésil pour l'instant). Le code de Cookiebot reste
    # en place derrière l'interrupteur COOKIEBOT_ACTIF ; pour rallumer le bandeau, remettre « true » ci-dessous et relancer ce script.
    # Tant qu'il est éteint : pas de bandeau, mesure d'audience autorisée par défaut, lien « Gérer mes cookies » masqué.
    COOKIEBOT_ACTIF = False
    _etat = 'true' if COOKIEBOT_ACTIF else 'false'
    _refus = "gtag('consent','default',{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied',functionality_storage:'granted',security_storage:'granted',wait_for_update:500});\ngtag('set','ads_data_redaction',true);\n"
    _choix = ("window.__cookiebotActif=__ETAT__;\ndocument.documentElement.setAttribute('data-cookiebot',window.__cookiebotActif?'1':'0');\n"
              "if(window.__cookiebotActif){gtag('consent','default',{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied',functionality_storage:'granted',security_storage:'granted',wait_for_update:500});gtag('set','ads_data_redaction',true);}\n"
              "else{gtag('consent','default',{ad_storage:'granted',ad_user_data:'granted',ad_personalization:'granted',analytics_storage:'granted',functionality_storage:'granted',security_storage:'granted'});}\n")
    if _refus in s:
        s = s.replace(_refus, _choix.replace('__ETAT__', _etat))
    s = re.sub(r'window\.__cookiebotActif=(?:true|false);', 'window.__cookiebotActif=' + _etat + ';', s)
    if "<script>(function(){if(!window.__cookiebotActif)return;var s=document.createElement('script');s.id='Cookiebot';" not in s:
        s = remplace(s, "<script>(function(){var s=document.createElement('script');s.id='Cookiebot';", "<script>(function(){if(!window.__cookiebotActif)return;var s=document.createElement('script');s.id='Cookiebot';")
    if 'data-lien-cookies="1"' not in s:
        s = remplace(s, '<a href="#" sc-camel-on-click="{{ openCookies }}"', '<a href="#" data-lien-cookies="1" sc-camel-on-click="{{ openCookies }}"')
    # Page de confidentialité : les deux phrases qui parlaient du bandeau (textes validés par Kévin le 18/11/2026).
    s, _t = _en(s, _t, 'When you browse the website: audience measurement cookies, only if you accept them.', 'When you browse the website: audience measurement cookies (Google Analytics and Microsoft Clarity).')
    _t = _t.replace('des cookies de mesure d’audience, seulement si vous les acceptez.', 'des cookies de mesure d’audience (Google Analytics et Microsoft Clarity).').replace('cookies de medição de audiência, só se você aceitar.', 'cookies de medição de audiência (Google Analytics e Microsoft Clarity).')
    s, _t = _en(s, _t, 'A banner asks for your choice on your first visit. You can change it at any time with the Cookie settings link at the bottom of every page.', 'The website uses audience measurement cookies to understand how it is used. You can block them in your browser settings.')
    _t = _t.replace('Un bandeau vous demande votre choix à votre première visite. Vous pouvez le modifier à tout moment avec le lien Gérer mes cookies, en bas de chaque page.', 'Le site utilise des cookies de mesure d’audience pour comprendre comment il est utilisé. Vous pouvez les bloquer dans les réglages de votre navigateur.').replace('Um aviso pede sua escolha na primeira visita. Você pode mudar a qualquer momento pelo link Preferências de cookies, no fim de cada página.', 'O site usa cookies de medição de audiência para entender como ele é usado. Você pode bloqueá-los nas configurações do seu navegador.')

    # Planches (18/11/2026, demande de Kévin) : « Avec la location illimitée, profitez de toutes les planches disponibles. »
    s, _t = _en(s, _t, 'With unlimited rental you pick the board of the day and swap whenever the sea changes.', 'With unlimited rental, enjoy every board available.')
    s, _t = _en(s, _t, 'The rack at the camp in Itacaré. Pick the board of the day and swap whenever the sea changes.', 'The rack at the camp in Itacaré. With unlimited rental, enjoy every board available.')
    _t = _t.replace('Avec la location illimitée, on choisit sa planche du jour et on en change dès que la mer change.', 'Avec la location illimitée, profitez de toutes les planches disponibles.').replace('Le rack du camp d’Itacaré. On choisit sa planche du jour et on en change dès que la mer change.', 'Le rack du camp d’Itacaré. Avec la location illimitée, profitez de toutes les planches disponibles.')
    _t = _t.replace('Com o aluguel ilimitado, você escolhe a prancha do dia e troca sempre que o mar muda.', 'Com o aluguel ilimitado, aproveite todas as pranchas disponíveis.').replace('O rack do camp em Itacaré. Você escolhe a prancha do dia e troca sempre que o mar muda.', 'O rack do camp em Itacaré. Com o aluguel ilimitado, aproveite todas as pranchas disponíveis.')

    # Introduction de la page Activités (18/11/2026, demande de Kévin) : une phrase par camp, avec les activités réellement
    # proposées sur place (plus de « sorties avec des habitants » ; le surfskate n'existe qu'à Rio).
    _intro_rio = 'Capoeira, percussion, hikes, yoga, massage, surfskate: surfing is only the starting point.'
    _intro_ita = 'Capoeira, yoga, massage, rafting, waterfalls, whale watching: surfing is only the starting point.'
    # (le nom « expIntro » existe déjà dans les données des camps pour un autre texte : on utilise « actIntro »)
    s = s.replace('>{{ camp.expIntro }}</p>', '>{{ camp.actIntro }}</p>').replace("expIntro: '" + _intro_rio + "', ", "actIntro: '" + _intro_rio + "', ").replace("expIntro: '" + _intro_ita + "', ", "actIntro: '" + _intro_ita + "', ")
    if '{{ camp.actIntro }}' not in s:
        s = remplace(s, '>Capoeira, percussion, hikes, days out with locals: surfing is only the starting point.</p>', '>{{ camp.actIntro }}</p>')
        _pos = [m.start() for m in re.finditer(r"expTitle: '", s)]
        if len(_pos) != 2:
            sys.exit('expTitle : deux camps attendus, trouvé ' + str(len(_pos)))
        s = s[:_pos[1]] + "actIntro: '" + _intro_ita + "', " + s[_pos[1]:]
        s = s[:_pos[0]] + "actIntro: '" + _intro_rio + "', " + s[_pos[0]:]
    _t = _dico(_t, _intro_rio, 'Capoeira, percussions, randonnées, yoga, massage, surfskate : le surf n’est que le point de départ.', 'Capoeira, percussão, trilhas, yoga, massagem, surfskate: o surf é só o ponto de partida.')
    _t = _dico(_t, _intro_ita, 'Capoeira, yoga, massage, rafting, cascades, observation des baleines : le surf n’est que le point de départ.', 'Capoeira, yoga, massagem, rafting, cachoeiras, observação de baleias: o surf é só o ponto de partida.')

    # Logo des modules Instagram (18/11/2026, demande de Kévin) : la version verte du logo (celle de l'icône du site)
    # à la place de l'ancienne version bleue.
    s = s.replace('/assets/65a25d62cccfe72f.png', '/assets/favicon-192.png')
    # ═══ Demande de Kévin du 20/11/2026 : mentions de devis plus courtes ═══
    # Parcours de réservation, sur téléphone : « Gratuit, sans engagement. Devis dans la journée. », sur une ligne (sans « par quelqu'un de l'équipe »).
    _m = re.search(r'(<b style="[^"]*">Free, no commitment\.</b>) Your quote within the day, from a real \(sandy\) person\.</span>', s)
    if _m:
        s = s[:_m.start()] + _m.group(1) + ' <span data-long="1">Your quote within the day, from a real (sandy) person.</span><span data-court="1">Quote within the day.</span></span>' + s[_m.end():]
    _t = _dico(_t, 'Quote within the day.', 'Devis dans la journée.', 'Orçamento no mesmo dia.')
    # Pages Rio et Itacaré : « Devis gratuit dans la journée » remplace « Gratuit, sans engagement » et la phrase qui suivait.
    _m = re.search(r'(\{\{ camp\.google\.count \}\} Google reviews</span>)\s*(<span style="[^"]*">)Free, no commitment</span>\s*<span style="[^"]*">Your quote within the day, from a real \(and probably sandy\) person\.</span>', s)
    if _m:
        s = s[:_m.start()] + _m.group(1) + '\n        ' + _m.group(2) + 'Free quote within the day</span>' + s[_m.end():]
    _m = re.search(r'Google reviews · Free, no commitment</span>\s*<span style="[^"]*">Your quote within the day, from a real \(and probably sandy\) person\.</span>', s)
    if _m:
        s = s[:_m.start()] + 'Google reviews · Free quote within the day</span>' + s[_m.end():]
    _t = _dico(_t, 'Free quote within the day', 'Devis gratuit dans la journée', 'Orçamento grátis no mesmo dia')
    _t = _dico(_t, 'Google reviews · Free quote within the day', 'avis Google · Devis gratuit dans la journée', 'avaliações no Google · Orçamento grátis no mesmo dia')
    # Lot vocabulaire (17/11/2026, option A validée par Kévin) : les onglets des pages camp portent le nom de la page où ils mènent.
    for _a, _b in (("{ label: 'The camp', id: 'camp' }", "{ label: 'Accommodation', id: 'camp' }"), ("{ label: 'Experiences', id: 'experiences' }", "{ label: 'Activities', id: 'experiences' }"),
                   ("camp: 'The camp', experiences: 'Experiences', lessons: 'Surf packages'", "camp: 'Accommodation', experiences: 'Activities', lessons: 'Surf packages'")):
        s = s.replace(_a, _b)
    _t = _dico(_t, 'Accommodation', 'Hébergement', 'Hospedagem')
    _t = _dico(_t, 'Activities', 'Activités', 'Atividades')
    _t = _t.replace('"Surf packages": "Packages surf"', '"Surf packages": "Séjours"').replace('"Surf packages": "Pacotes de surf"', '"Surf packages": "Pacotes"')
    # Un mot par chose, en français : « séjour » pour le voyage entier, « package » pour les trois offres toutes faites,
    # « hébergement » et plus « logement », « cours » pour une leçon avec moniteur.
    for _a, _b in (
        ('Composez votre stage de surf vous-même', 'Composez votre séjour vous-même'),
        ('"Logement en bord de plage"', '"Hébergement en bord de plage"'),
        ('de votre logement', 'de votre hébergement'), ('devant votre logement', 'devant votre hébergement'), ('Depuis votre logement', 'Depuis votre hébergement'),
        ('à côté de votre logement', 'à côté de votre hébergement'), ('voisin de votre logement', 'voisin de votre hébergement'),
        ('"Mon package sur mesure"', '"Mon séjour sur mesure"'), ('"Masquer le package sur mesure"', '"Masquer le séjour sur mesure"'),
        ('"Composer mon package sur mesure →"', '"Composer mon séjour sur mesure →"'), ('"Composer mon package"', '"Composer mon séjour"'),
        ('"Le déroulé d’une session"', '"Le déroulé d’un cours"'),
        ('notre stage de surf Surf Intensive', 'notre package Surf Intensive'),
        ('"Cours de surf : choisissez un package, ou créez le vôtre."', '"Votre séjour : choisissez un package, ou composez le vôtre."'),
        ('"Cours de surf\u00a0: choisissez un package, ou créez le vôtre."', '"Votre séjour\u00a0: choisissez un package, ou composez le vôtre."'), ('les courants et le déroulé de la séance', 'les courants et le déroulé du cours'),
    ):
        _t = _t.replace(_a, _b)
    # Lot technique (17/11/2026) : les trois photos d'Itacaré chargées depuis Google Drive (qui refusait parfois de les servir)
    # sont rangées avec les autres photos du site.
    for _id, _f in (('1wEyto15W0YYJMQ3ClOq9xnAMdkLbD41o', 'drive-cascade.jpg'), ('1lg63dJnijtYOGv40_kUwmqunasQqP_Yt', 'drive-coworking-a.jpg'), ('1krI9mgFpoLHZC-tA04kUqokBLGss6h2_', 'drive-coworking-b.jpg')):
        s = s.replace('https://lh3.googleusercontent.com/d/%s=w1600' % _id, '/assets/' + _f)
    # Lot technique (17/11/2026) : le gabarit est d'abord lu tel quel par le navigateur, qui essayait de charger les adresses d'images
    # encore vides (« /{{ camp.heroImg }} », environ 40 erreurs par page). Le préfixe « sc-camel- » du moteur rend l'attribut invisible
    # pour le navigateur jusqu'au rendu, où il redevient un « src » ou un « poster » normal. À FAIRE EN DERNIER : les repères plus haut
    # dans ce fichier cherchent encore « src="{{ ».
    s = re.sub(r'(<(?:img|video|source|iframe)\b[^>]*?\s)(src|poster)="\{\{', lambda _m: _m.group(1) + 'sc-camel-' + _m.group(2) + '="{{', s)
    s = re.sub(r'(<(?:img|video|source|iframe)\b[^>]*?\s)(src|poster)="\{\{', lambda _m: _m.group(1) + 'sc-camel-' + _m.group(2) + '="{{', s)
    open(_tx, 'w', encoding='utf-8').write(_t)
# ═══ Lot Lighthouse (18/11/2026) : accessibilité, polices hébergées sur le site, dimensions des images ═══
# 1. Noms accessibles. Les aria-label ne passent pas par i18n.js (qui ne traduit que les nœuds de texte et les placeholders) :
#    ils sont calculés dans les données du rendu, selon la langue.
#    Les noms « a11y_… » sont réécrits à chaque passage (tout ce qui suit langMenuOpen jusqu'à « 'Language'), »).
_a11y = re.compile(r"langMenuOpen: !!this\.state\.langMenuOpen,(?: a11y_[^\n]*?\|\| 'Language'\),)?")
if len(_a11y.findall(s)) != 1:
    sys.exit('Repère langMenuOpen introuvable ou ambigu')
s = _a11y.sub(lambda _m: "langMenuOpen: !!this.state.langMenuOpen, a11y_menu_ouvert: this.state.menuOpen ? 'true' : 'false', "
             "a11y_photos: this.state.lang === 'en' || !this.state.lang ? 'See the photos' : (((window.__i18n || {})[this.state.lang] || {})['See photos'] || 'See the photos'), "
             "a11y_wa: ((window.__i18n || {})[this.state.lang] || {})['Message us on WhatsApp'] || 'Message us on WhatsApp', "
             "a11y_langue: (this.LANGS.find(l => l.id === (this.state.lang || 'en')) || this.LANGS[0]).code + ', ' + (({ fr: 'Langue', pt: 'Idioma' })[this.state.lang] || 'Language'),", s)
s = remplace(s, '<div data-nav-burger="1" sc-camel-on-click="{{ toggleMenu }}" style="display:none;',
             '<div data-nav-burger="1" sc-camel-on-click="{{ toggleMenu }}" aria-label="Menu" aria-expanded="{{ a11y_menu_ouvert }}" style="display:none;')
s = remplace(s, '<div data-stay-photos="1" sc-camel-on-click="{{ goTabCamp }}" style="cursor:pointer;',
             '<div data-stay-photos="1" sc-camel-on-click="{{ goTabCamp }}" aria-label="{{ a11y_photos }}" style="cursor:pointer;')
# Bulle WhatsApp : nom accessible = texte affiché, dans la langue de la page (il était en anglais et doublait « on WhatsApp »)
s = s.replace('role="button" aria-label="Message us on WhatsApp on WhatsApp"', 'role="button" aria-label="{{ a11y_wa }}"')
# Sélecteur de langue : le nom accessible commence par le texte visible (« EN, Language »)
s = s.replace('title="Language" aria-label="Language"', 'title="Language" aria-label="{{ a11y_langue }}"')
# 2. Polices hébergées sur le site (assets/fonts/, cache immuable) au lieu de Google Fonts. Mêmes fichiers, mêmes graisses,
#    mêmes plages Unicode que la feuille de Google (latin et latin-ext), « font-display: swap » comme avant.
_LATIN = 'U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD'
_LATIN_EXT = 'U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF'
# Relevé du 18/11/2026 sur toutes les pages (ordinateur et téléphone, tunnel compris) : Gabarito 600 et Londrina Solid 400
# n'étaient jamais utilisées, elles ne sont pas reprises. Chivo et Gabarito sont des polices variables : un fichier pour toutes les graisses.
_POLICES = (
    # (famille, graisse, fichier, plage)
    ('Chivo', 400, 'chivo-latin-ext', _LATIN_EXT), ('Chivo', 400, 'chivo-latin', _LATIN),
    ('Chivo', 600, 'chivo-latin-ext', _LATIN_EXT), ('Chivo', 600, 'chivo-latin', _LATIN),
    ('Chivo', 700, 'chivo-latin-ext', _LATIN_EXT), ('Chivo', 700, 'chivo-latin', _LATIN),
    ('Gabarito', 700, 'gabarito-latin-ext', _LATIN_EXT), ('Gabarito', 700, 'gabarito-latin', _LATIN),
    ('Londrina Solid', 900, 'londrina-solid-900-latin', _LATIN),
    ('Permanent Marker', 400, 'permanent-marker-latin', _LATIN),
)
for _f in sorted({p[2] for p in _POLICES}):
    if not os.path.exists(os.path.join(os.path.dirname(ICI), 'assets', 'fonts', _f + '.woff2')):
        sys.exit('Police manquante : assets/fonts/%s.woff2' % _f)
_ff = '<style data-polices-locales="1">\n' + ''.join(
    "@font-face{font-family:'%s';font-style:normal;font-weight:%d;font-display:swap;src:url(/assets/fonts/%s.woff2) format('woff2');unicode-range:%s;}\n" % p
    for p in _POLICES) + '</style>\n'
_lien = re.search(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?[^"]*">\n', s)
if _lien:
    s = s[:_lien.start()] + _ff + s[_lien.end():]
elif 'data-polices-locales' in s:
    _i = s.index('<style data-polices-locales="1">'); _j = s.index('</style>\n', _i) + len('</style>\n')
    s = s[:_i] + _ff + s[_j:]
else:
    sys.exit('Feuille Google Fonts introuvable')
s = s.replace('<link rel="preconnect" href="https://fonts.googleapis.com">\n', '').replace('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="">\n', '')
# 3. Images fixes : largeur et hauteur du fichier (le CSS fixe déjà la taille affichée : width et height en ligne ou dans
#    les feuilles), pour réserver la place avant le chargement. Chargement différé hors du premier écran ; jamais pour
#    les images de hero (« Pour qui », « À propos »), qui sont l'élément LCP de leur page.
_idx = open(os.path.join(os.path.dirname(ICI), 'index.html'), encoding='utf-8').read()
_m = re.search(r'<script type="__bundler/external">', _idx)
_ext = json.loads(_idx[_m.end():_idx.index('</script>', _m.end())])


def _dims(chemin):
    # Dimensions lues dans l'en-tête du fichier (PNG, JPEG, WebP), en Python pur, pour que la reconstruction
    # tourne aussi hors d'un Mac (18/11/2026 ; auparavant avec `sips`, propre à macOS).
    import struct
    d = open(chemin, 'rb').read()
    if d[:8] == b'\x89PNG\r\n\x1a\n':
        return struct.unpack('>II', d[16:24])
    if d[:4] == b'RIFF' and d[8:12] == b'WEBP':
        t = d[12:16]
        if t == b'VP8 ':
            return struct.unpack('<H', d[26:28])[0] & 0x3FFF, struct.unpack('<H', d[28:30])[0] & 0x3FFF
        if t == b'VP8L':
            b = int.from_bytes(d[21:25], 'little')
            return (b & 0x3FFF) + 1, ((b >> 14) & 0x3FFF) + 1
        if t == b'VP8X':
            return int.from_bytes(d[24:27], 'little') + 1, int.from_bytes(d[27:30], 'little') + 1
    if d[:2] == b'\xff\xd8':
        i = 2
        while i + 9 < len(d):
            if d[i] != 0xFF:
                i += 1; continue
            m = d[i + 1]
            if m in (0xD8, 0x01) or 0xD0 <= m <= 0xD7:
                i += 2; continue
            n = struct.unpack('>H', d[i + 2:i + 4])[0]
            if m in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                h, w = struct.unpack('>HH', d[i + 5:i + 9])
                return w, h
            i += 2 + n
    sys.exit('Dimensions illisibles : ' + chemin)


_HEROS = ('85e6ce0f-b360-4119-b5fc-604dd19d1af5', '735c9c46-c82b-41f4-827b-c2738eedb1ed')


def _img(m):
    t = m.group(0)
    if 'sc-camel-src' in t or 'src="{{' in t or re.search(r'\swidth="', t):
        return t
    src = re.search(r'\ssrc="([^"]+)"', t)
    if not src:
        return t
    chemin = _ext.get(src.group(1), src.group(1))
    if not chemin.startswith('/assets/'):
        return t
    # La taille affichée doit venir du CSS : style en ligne avec width et height, ou carte « Choisissez votre camp » (mobile.css)
    st = re.search(r'\sstyle="([^"]*)"', t)
    if not ((st and re.search(r'(^|;)width:', st.group(1)) and re.search(r'(^|;)height:', st.group(1))) or 'data-suite-carte' in s[max(0, m.start() - 160):m.start()]):
        return t
    w, h = _dims(os.path.join(os.path.dirname(ICI), chemin.lstrip('/')))
    ajout = ' width="%d" height="%d"' % (w, h)
    if src.group(1) not in _HEROS:
        if 'loading=' not in t:
            ajout += ' loading="lazy"'
        if 'decoding=' not in t:
            ajout += ' decoding="async"'
    return t[:-1] + ajout + '>'  # en fin de balise : les repères plus haut cherchent « <img src="… »


s = re.sub(r'<img\b[^>]*>', _img, s)
# Échelle typographique : neuf tailles sur tout le site (voir outils/echelle.py)
sys.path.insert(0, ICI)
import echelle
css = echelle.applique(css, s)
for nom, txt in (('couche.css', css), ('couche.js', js), ('stickers', variables)):
    if '{{' in txt:
        sys.exit(f'« {{{{ » interdit dans {nom} (moteur de gabarit)')
m = re.search(r'\b[a-z]+[A-Z]\w* =[^=]', js)
if m:
    sys.exit(f'camelCase avant « = » dans couche.js : {m.group(0)}')
couche = f'{DEBUT}\n<style>\n{variables}{css}</style>\n<script>\n{js}</script>\n{FIN}\n'

# La couche se pose au niveau des autres couches du gabarit, juste après le script de la marée.
ancre = "  installe();\n})();\n</script>\n"
if s.count(ancre) != 1:
    sys.exit(f'Ancre de la marée introuvable ou ambiguë ({s.count(ancre)}×)')
i = s.index(ancre) + len(ancre)
s = s[:i] + couche + s[i:]

# Palette resserrée (17/11/2026, lot couleurs validé par Kévin). Le relevé comptait 55 couleurs de fond et 63 de texte, dont beaucoup
# de quasi-doublons et des restes de l'ancienne charte bleue. On regroupe ici, tout à la fin, sur le gabarit complet (feuilles de style
# comprises) : c'est le seul endroit où toutes les couches sont réunies. Les couleurs de la fiche Google et d'Instagram ne sont pas touchées.
PALETTE = (
    ('#FFF1E6', '#FFFBF3'),  # fond des messages d'alerte du parcours (18/11/2026)
    ('#F7F5F0', '#F7F4EA'), ('#FFFDF8', '#FFFBF3'),                                  # crèmes : un fond de page, un fond de carte
    ('#DCE6DB', '#E3EEE5'), ('#E4EEE8', '#E3EEE5'), ('#E7EEE9', '#E3EEE5'),          # verts pâles : un seul
    ('#1E4636', '#0C3B32'), ('#04262D', '#0C3B32'),                                  # verts foncés : celui des titres
    ('#2B5148', '#3F5F56'), ('#1F4D55', '#3F5F56'),                                  # texte courant
    ('#6B8178', '#5C7268'),                                                          # légendes : contraste 4,7 sur crème (3,8 avant)
    ('#128064', '#0F7359'),                                                          # étiquettes et liens : 5,3 sur crème (4,4 avant)
    ('#E9A13B', '#FFC531'),                                                          # étoiles : le jaune de Rio
    ('#FFB3B6', '#F5B98A'),                                                          # pastille « Confirmé » : gamme chaude du site
    ('#8FD0E8', '#9AD9B9'),                                                          # ancien bleu clair
    # Second passage du 18/11/2026 (demande de Kévin : le site applique le design system et n'en sort pas).
    ('#FFF8EF', '#F7F4EA'), ('#FFF3E0', '#F7F4EA'), ('#F2F8F6', '#F7F4EA'), ('#F5F2EB', '#F7F4EA'), ('#EFE8DC', '#F7F4EA'),   # un seul crème clair, en texte comme en fond
    ('#F1E8D5', '#FFFBF3'),                                                          # fond de carte
    ('#8FA39B', '#B9C9C1'),                                                          # texte discret sur fond foncé : une seule valeur
    ('#FFD9A0', '#F5CE8E'),                                                          # sable : étiquettes sur fond foncé, pastille « Intermédiaire »
    ('#A8DCC3', '#9AD9B9'), ('#BFE5CF', '#9AD9B9'),                                  # menthe : pastille « Débutant », accents sur fond foncé
    ('#2A7050', '#0F7359'), ('#06323B', '#0C3B32'),                                  # verts
    ('#9A4A0E', '#B8520F'), ('#C9620F', '#9C440B'),
    ('#10202F', '#0C3B32'),                                                          # fond des photos en grand : le vert du site, pas un bleu nuit                                  # oranges de Bahia : un ton, un survol
)
# Les mêmes valeurs écrites en « rgb(…) » dans des sélecteurs qui lisent les styles en ligne.
for _a, _b in (('rgb(245, 242, 235)', 'rgb(247, 244, 234)'), ('rgb(255, 217, 160)', 'rgb(245, 206, 142)')):
    s = s.replace(_a, _b)
# Et les mêmes teintes écrites avec une transparence.
for _a, _b in (('35,70,104', '12,59,50'), ('18,128,100', '15,115,89'), ('23,42,62', '12,59,50'), ('242,248,246', '247,244,234'), ('245,242,235', '247,244,234'), ('143,208,232', '154,217,185'), ('168,220,195', '154,217,185'), ('6,50,59', '12,59,50')):
    s = s.replace('rgba(' + _a + ',', 'rgba(' + _b + ',').replace('rgba(' + _a.replace(',', ', ') + ',', 'rgba(' + _b.replace(',', ', ') + ',')
for _a, _b in PALETTE:
    s = re.sub(re.escape(_a), _b, s, flags=re.I)
s = s.replace('rgba(54,140,175,', 'rgba(12,59,50,').replace('rgba(54, 140, 175,', 'rgba(12, 59, 50,')
# Images rapatriées de Framer (23/11/2026) : les 12 photos chargées depuis framerusercontent.com disparaîtront avec
# l'abonnement Framer. Copies en webp dans assets/ (2x la taille servie par Framer, 1600 px au plus).
FRAMER = {
    'https://framerusercontent.com/images/5fhciN8Y3RqcDhJI5czGDtnej8.jpeg?scale-down-to=512': '/assets/1d4690fe8b65a61a.webp',
    'https://framerusercontent.com/images/6EABb9KDby79gV0OoeoNV1Sep7E.jpg?scale-down-to=1024': '/assets/df65c90381ae381d.webp',
    'https://framerusercontent.com/images/F2RrutfigpoYWkAWYXusv3J0CE8.jpg?scale-down-to=1024': '/assets/39fc6400d2d5767c.webp',
    'https://framerusercontent.com/images/GPGECtmItJp14e5g5bva2UucQK4.jpeg?scale-down-to=1024': '/assets/740c5f840675c961.webp',
    'https://framerusercontent.com/images/HzNf3fMQyVsX5sfl46s9kdr16x8.jpg?scale-down-to=512': '/assets/af59b8ec117c081a.webp',
    'https://framerusercontent.com/images/J7x5Ty1wvrWkJWc5UkzVlxoNHbQ.jpeg?scale-down-to=1024': '/assets/909463810a1d3952.webp',
    'https://framerusercontent.com/images/WiVSqUg3y5OkrQCpk0lCRxQbaQ.jpg?scale-down-to=1024': '/assets/4b2e67ec54f5d1c7.webp',
    'https://framerusercontent.com/images/kpwkaTBmMBRM2rgPWeKrJ51dTM.jpg?scale-down-to=1024': '/assets/7c90f46f1b2405ee.webp',
    'https://framerusercontent.com/images/mqe0rdtejFm25yBHf4VptYfLzPU.jpeg?scale-down-to=512': '/assets/14211921e79584d0.webp',
    'https://framerusercontent.com/images/ts54ymIC9MbIQbZaQubL9AiEIUQ.jpg?scale-down-to=512': '/assets/a874021346b2ffa0.webp',
    'https://framerusercontent.com/images/wrB5uJ0duhG659xmdy53m6UoEM.jpg?scale-down-to=1024': '/assets/e9143043aafa162e.webp',
    'https://framerusercontent.com/images/yYoCywEj5BDN4E02bZAQxzYbQ.png?scale-down-to=1024': '/assets/8b29181dce63efc9.webp',
}
for _a, _b in FRAMER.items():
    s = s.replace(_a, _b)
if 'framerusercontent.com' in s:
    sys.exit('Une image vient encore de framerusercontent.com : ajouter son adresse à FRAMER')
open(GAB, 'w', encoding='utf-8').write(s)
print('Couche expérientielle posée')
