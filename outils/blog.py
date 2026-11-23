#!/usr/bin/env python3
"""Blog en pages statiques (23/11/2026).

    python3 outils/blog.py      # réécrit blog/ ; idempotent

Les deux articles de l'ancien site Framer, repris aux mêmes adresses pour garder leur référencement
(sauf le second, dont l'adresse contenait un tiret long : redirection 308 dans vercel.json).

Le blog ne passe pas par index.html (le site React) : ce sont de vraies pages HTML, lisibles par Google
sans JavaScript, au même habillage que le site (couleurs, polices, logo). Sources :
- outils/blog/articles.json : titre, date, description, image de couverture, destination de chaque article ;
- outils/blog/<slug>.html : le corps de l'article (p, h2, h3, ul, strong, a).
Pour ajouter un article : une entrée dans articles.json, son corps dans <slug>.html, l'image dans assets/,
relancer ce script, ajouter l'adresse au sitemap.xml.

vercel.json exclut blog/ de la réécriture vers index.html, et middleware.js ne s'applique pas à blog/.
"""
import html, json, os

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(RACINE, 'outils', 'blog')
SORTIE = os.path.join(RACINE, 'blog')
DOMAINE = 'https://www.visitsurfinn.com'
GTM = 'GTM-WH4MTLKG'
MOIS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
DEST = {
    'rio': ('Surf Inn Rio', '/surf-camp/rio-de-janeiro/', '/surf-camp/rio-de-janeiro/packages/', 'https://wa.me/5521999231992'),
    'itacare': ('Surf Inn Bahia', '/surf-camp/itacare/', '/surf-camp/itacare/packages/', 'https://wa.me/5573998257683'),
}
e = lambda t: html.escape(str(t), quote=True)


def date_longue(d):
    a, m, j = d.split('-')
    return f'{MOIS[int(m) - 1]} {int(j)}, {a}'


CSS = """
@font-face{font-family:'Chivo';font-weight:400 700;font-display:swap;src:url(/assets/fonts/chivo-latin.woff2) format('woff2')}
@font-face{font-family:'Gabarito';font-weight:700;font-display:swap;src:url(/assets/fonts/gabarito-latin.woff2) format('woff2')}
:root{--creme:#F7F4EA;--carte:#FFFBF3;--encre:#0C3B32;--vert:#0F7359;--doux:#4A6A80;--soleil:#FFC531;--pied:#0F4A3E;--trait:rgba(12,59,50,.14)}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--creme);color:var(--encre);font:400 17px/1.65 Chivo,system-ui,sans-serif}
a{color:var(--vert)}
img{max-width:100%;height:auto;display:block}
.nav{position:sticky;top:0;z-index:5;display:flex;align-items:center;justify-content:space-between;gap:16px;padding:12px clamp(16px,4vw,48px);background:rgba(247,244,234,.94);backdrop-filter:blur(10px);border-bottom:1px solid var(--trait)}
.nav img{height:52px;width:auto}
.nav nav{display:flex;align-items:center;gap:clamp(12px,2vw,28px);font-weight:600;font-size:16px}
.nav nav a{color:var(--encre);text-decoration:none}
.nav nav a:hover{color:var(--vert)}
.cta{display:inline-block;background:var(--soleil);color:var(--encre)!important;text-decoration:none;font-weight:700;padding:11px 22px;border-radius:999px;white-space:nowrap}
.cta:hover{filter:brightness(.95)}
main{max-width:760px;margin:0 auto;padding:clamp(32px,6vw,72px) 16px 72px}
.sur{font-weight:700;font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--vert);margin:0 0 12px}
.sur a{color:inherit;text-decoration:none}
h1,h2,h3{font-family:Gabarito,Chivo,system-ui,sans-serif;font-weight:700;line-height:1.1;letter-spacing:-.015em;text-wrap:pretty}
h1{font-size:clamp(34px,5.4vw,52px);margin:0 0 14px}
h2{font-size:clamp(26px,3.4vw,34px);margin:44px 0 12px}
h3{font-size:clamp(20px,2.4vw,23px);margin:28px 0 8px}
.date{color:var(--doux);font-size:15px;margin:0 0 28px}
.couv{border-radius:20px;overflow:hidden;margin:0 0 36px;background:#C9DAE3}
.couv img{width:100%;max-height:520px;object-fit:cover}
article p{margin:0 0 16px}
article ul{margin:0 0 18px;padding-left:22px}
article li{margin:0 0 6px}
.encart{margin:48px 0 0;padding:28px;border-radius:20px;background:var(--carte);border:1px solid var(--trait)}
.encart h2{margin:0 0 8px;font-size:clamp(24px,3vw,30px)}
.encart p{margin:0 0 18px}
.encart .lien{margin-left:16px;font-weight:700}
.autres{margin:56px 0 0;padding-top:28px;border-top:1px solid var(--trait)}
.liste{display:grid;gap:22px;margin-top:8px}
.carte{display:grid;grid-template-columns:minmax(0,220px) 1fr;gap:20px;align-items:center;padding:14px;border-radius:20px;background:var(--carte);border:1px solid var(--trait);color:var(--encre);text-decoration:none}
.carte:hover{border-color:var(--vert)}
.carte img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:14px}
.carte h2,.carte h3{margin:0 0 6px;font-size:clamp(20px,2.6vw,24px)}
.carte p{margin:0;color:var(--doux);font-size:15px;line-height:1.5}
.carte .date{margin:0 0 6px;font-size:13px}
footer{background:var(--pied);color:#F7F4EA;padding:40px clamp(16px,4vw,64px)}
footer .haut{display:flex;flex-wrap:wrap;align-items:center;gap:16px 28px}
footer img{height:64px;width:auto}
footer a{color:#DDE8E2;text-decoration:none;font-weight:600;font-size:15px}
footer a:hover{color:#fff}
footer .bas{margin-top:24px;padding-top:20px;border-top:1px solid rgba(247,244,234,.15);font-size:14px;color:#B9C9C1}
@media (max-width:720px){
  .nav nav a:not(.cta){display:none}
  .nav img{height:44px}
  .cta{padding:10px 16px;font-size:15px}
  .carte{grid-template-columns:1fr}
  .encart .lien{display:block;margin:14px 0 0}
}
"""


def tete(titre, description, chemin, image, extra_ld):
    url = DOMAINE + chemin
    ld = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in extra_ld)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titre)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{e(url)}">
<link rel="icon" type="image/png" href="/assets/favicon-64.png">
<link rel="apple-touch-icon" href="/assets/favicon-192.png">
<link rel="preload" href="/assets/fonts/gabarito-latin.woff2" as="font" type="font/woff2" crossorigin>
<meta property="og:type" content="article">
<meta property="og:site_name" content="Surf Inn">
<meta property="og:title" content="{e(titre)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{e(url)}">
<meta property="og:image" content="{e(DOMAINE + image)}">
<meta name="twitter:card" content="summary_large_image">
<script>
window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}
gtag('consent','default',{{ad_storage:'granted',ad_user_data:'granted',ad_personalization:'granted',analytics_storage:'granted',functionality_storage:'granted',security_storage:'granted'}});
(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','{GTM}');
</script>
{ld}<style>{CSS}</style>
</head>
<body>
<header class="nav">
  <a href="/" aria-label="Surf Inn, home"><img src="/assets/logo-surf-inn-vert.png" alt="Surf Inn" width="56" height="52"></a>
  <nav>
    <a href="/surf-camp/rio-de-janeiro/">Rio de Janeiro</a>
    <a href="/surf-camp/itacare/">Itacaré</a>
    <a href="/blog/">Blog</a>
    <a href="/contact/">Contact</a>
    <a class="cta" href="/surf-camp/rio-de-janeiro/packages/">Build my stay</a>
  </nav>
</header>
"""


PIED = """<footer>
  <div class="haut">
    <a href="/" aria-label="Surf Inn, home"><img src="/assets/6616ca5f5d23c5a1.png" alt="Surf Inn" width="69" height="64"></a>
    <a href="/surf-camp/rio-de-janeiro/">Surf Inn Rio</a>
    <a href="/surf-camp/itacare/">Surf Inn Bahia</a>
    <a href="/who-is-it-for/">Who it's for</a>
    <a href="/about-us/">About us</a>
    <a href="/faq/">FAQ</a>
    <a href="/reviews/">Reviews</a>
    <a href="/blog/">Blog</a>
    <a href="/contact/">Contact</a>
  </div>
  <div class="bas">Surf camps in Rio de Janeiro and Itacaré, Brazil · <a href="/privacy/">Privacy policy</a> · <a href="/legal/">Legal information</a></div>
</footer>
</body>
</html>
"""


def fil(*etapes):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': DOMAINE + c} for i, (n, c) in enumerate(etapes)]}


def carte(a, niveau='h2'):
    w, h = a['cover_size']
    return f"""  <a class="carte" href="/blog/{e(a['slug'])}/">
    <img src="{e(a['cover'])}" alt="" width="{w}" height="{h}" loading="lazy">
    <div><p class="date">{date_longue(a['date'])}</p><{niveau}>{e(a['title'])}</{niveau}><p>{e(a['excerpt'])}</p></div>
  </a>
"""


def ecrire(chemin, contenu):
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    open(chemin, 'w', encoding='utf-8').write(contenu)


articles = sorted(json.load(open(os.path.join(SRC, 'articles.json'), encoding='utf-8')), key=lambda a: a['date'], reverse=True)

for a in articles:
    corps = open(os.path.join(SRC, a['slug'] + '.html'), encoding='utf-8').read().strip()
    nom, page, paquets, wa = DEST[a['dest']]
    chemin = f"/blog/{a['slug']}/"
    w, h = a['cover_size']
    ld = [{'@context': 'https://schema.org', '@type': 'BlogPosting', 'headline': a['title'], 'description': a['description'],
           'image': DOMAINE + a['cover'], 'datePublished': a['date'], 'mainEntityOfPage': DOMAINE + chemin,
           'author': {'@type': 'Organization', 'name': 'Surf Inn', 'url': DOMAINE + '/'},
           'publisher': {'@type': 'Organization', 'name': 'Surf Inn', 'logo': {'@type': 'ImageObject', 'url': DOMAINE + '/assets/favicon-192.png'}}},
          fil(('Surf Inn', '/'), ('Blog', '/blog/'), (a['title'], chemin))]
    autres = [x for x in articles if x is not a]
    page_html = tete(a['title'] + ' | Surf Inn', a['description'], chemin, a['cover'], ld) + f"""<main>
<p class="sur"><a href="/blog/">Blog</a></p>
<h1>{e(a['title'])}</h1>
<p class="date"><time datetime="{a['date']}">{date_longue(a['date'])}</time></p>
<div class="couv"><img src="{e(a['cover'])}" alt="" width="{w}" height="{h}" fetchpriority="high"></div>
<article>
{corps}
</article>
<aside class="encart">
  <h2>Surf with us at {e(nom)}</h2>
  <p>Small groups, three surfers per instructor, rooms by the beach. Tell us your dates and get a free quote within the day.</p>
  <a class="cta" href="{paquets}">See the surf packages</a><a class="lien" href="{wa}" target="_blank" rel="noopener">WhatsApp us</a>
</aside>
""" + (f"""<section class="autres">
<p class="sur">Keep reading</p>
<div class="liste">
{''.join(carte(x, 'h3') for x in autres)}</div>
</section>
""" if autres else '') + "</main>\n" + PIED
    ecrire(os.path.join(SORTIE, a['slug'], 'index.html'), page_html)

titre_liste = 'Surf trip guides and tips | Surf Inn blog'
desc_liste = 'Guides and tips from the Surf Inn team for your surf trip to Brazil: surf spots, seasons and how to progress faster in Rio de Janeiro and Itacaré.'
liste = tete(titre_liste, desc_liste, '/blog/', articles[0]['cover'], [fil(('Surf Inn', '/'), ('Blog', '/blog/'))]) + f"""<main>
<p class="sur">Blog</p>
<h1>Surf trip guides and tips</h1>
<p class="date">From the Surf Inn team in Rio de Janeiro and Itacaré.</p>
<div class="liste">
{''.join(carte(a) for a in articles)}</div>
</main>
""" + PIED
ecrire(os.path.join(SORTIE, 'index.html'), liste)
print(f'Blog écrit : {len(articles)} articles dans blog/')
