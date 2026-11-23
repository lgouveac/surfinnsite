"""Échelle typographique du site : neuf tailles, chacune avec un rôle (14/11/2026).

Les feuilles de style de la couche et les styles en ligne du gabarit déclarent plus de soixante tailles différentes.
Ce module les ramène à l'échelle au moment où la couche est posée, sans toucher au gabarit lui-même
(les repères de experience.py contiennent des « font-size » et doivent rester intacts).
  - feuilles de la couche : chaque « font-size » est remplacé par la taille de l'échelle la plus proche ;
  - styles en ligne : une règle par valeur rencontrée, de faible priorité, pour que les règles de la couche gardent la main.
Non touchés : le nom « SURF INN » (le logo), les tailles liées à la largeur d'un bloc (cqi), les unités autres que px.
"""
import re

# nom, taille sur téléphone (390 px), taille sur ordinateur (1440 px), valeur CSS
ECHELLE = [
    ('legende', 12, 12, '12px'), ('petit', 14, 14, '14px'), ('texte', 16, 16, '16px'), ('avant', 18, 18, '18px'),
    ('carte', 21, 24, 'var(--t-carte)'), ('sous', 24, 30, 'var(--t-sous)'), ('section', 29, 40, 'var(--t-section)'),
    ('page', 33, 56, 'var(--t-page)'), ('chiffre', 48, 72, 'var(--t-chiffre)'),
]
VARIABLES = ('  :root{--t-carte:clamp(21px,1.9vw,24px);--t-sous:clamp(24px,2.4vw,30px);--t-section:clamp(29px,3.4vw,40px);'
             '--t-page:clamp(33px,4.6vw,56px);--t-chiffre:clamp(48px,6vw,72px);}\n')
PX = re.compile(r'^(\d+(?:\.\d+)?)px$')
CLAMP = re.compile(r'^clamp\(\s*(\d+(?:\.\d+)?)px\s*,\s*(\d+(?:\.\d+)?)vw\s*,\s*(\d+(?:\.\d+)?)px\s*\)$')


def jeton(valeur, contexte='tout'):
    """Taille de l'échelle la plus proche de « valeur », ou None s'il ne faut pas y toucher."""
    v = valeur.strip()
    m = PX.match(v)
    if m:
        tel = ordi = float(m.group(1))
    else:
        m = CLAMP.match(v)
        if not m:
            return None
        a, vw, b = (float(x) for x in m.groups())
        if vw >= 14 or b >= 200:      # le nom « SURF INN », qui suit la largeur de l'écran
            return None
        tel, ordi = min(max(a, vw * 3.9), b), min(max(a, vw * 14.4), b)
        if contexte != 'tel':         # un clamp est un titre : on le classe par sa taille sur ordinateur
            for seuil, nom in ((21, 'avant'), (30, 'carte'), (36, 'sous'), (50, 'section'), (70, 'page'), (1e9, 'chiffre')):
                if ordi <= seuil:
                    return next(e[3] for e in ECHELLE if e[0] == nom)
    def ecart(e):
        d_tel, d_ordi = abs(tel - e[1]) / e[1], abs(ordi - e[2]) / e[2]
        return d_tel if contexte == 'tel' else d_ordi if contexte == 'ordi' else d_tel + d_ordi
    return min(ECHELLE, key=lambda e: (round(ecart(e), 4), e[1]))[3]


ROLES = [  # (motif sur le dernier sélecteur de la règle, taille imposée) : le premier qui correspond l'emporte
    (r'\[data-bresil\] > h2$', 'chiffre'), (r'\[data-(profils|coral-bg)\] h2$', 'sous'), (r'(\[data-experiences\]|#camp-guide) h3$', 'sous'),
    (r'\bh1$', 'page'), (r'\bh2$', 'section'), (r'\bh3$', 'carte'),
]


def role(selecteur):
    dernier = selecteur.split(',')[-1].strip()
    for motif, nom in ROLES:
        if re.search(motif, dernier):
            return next(e[3] for e in ECHELLE if e[0] == nom)
    return None


def feuille(css):
    """Remplace les « font-size » d'une feuille de style, en tenant compte du bloc @media où ils se trouvent."""
    sortie, pile, i, selecteur = [], [], 0, ''
    motif = re.compile(r'@media[^{]*\{|\{|\}|font-size\s*:\s*([^;}!]+)')
    for m in motif.finditer(css):
        avant = css[i:m.start()]
        sortie.append(avant); i = m.end(); t = m.group(0)
        if t == '{':
            selecteur = avant.split(';')[-1].split('*/')[-1]
        if t.startswith('@media'):
            pile.append('tel' if 'max-width' in t else 'ordi' if 'min-width' in t else 'tout')
        elif t == '{':
            pile.append(None)
        elif t == '}':
            if pile:
                pile.pop()
        else:
            ctx = next((c for c in reversed(pile) if c), 'tout')
            j = jeton(m.group(1), ctx)
            if j and (PX.match(m.group(1).strip()) is None or float(PX.match(m.group(1).strip()).group(1)) >= 19):
                j = role(selecteur) or j
            if j:
                esp = m.group(1)[len(m.group(1).rstrip()):]
                t = 'font-size:' + j + esp
        sortie.append(t)
    sortie.append(css[i:])
    return ''.join(sortie)


def en_ligne(gabarit):
    """Règles pour les tailles écrites dans les attributs style du gabarit (le navigateur les réécrit « font-size: 14px »)."""
    valeurs = set()
    for st in re.findall(r'style="([^"]*)"', gabarit):
        for v in re.findall(r'font-size:\s*([^;]+)', st):
            valeurs.add(v.strip())
    regles = []
    for v in sorted(valeurs):
        j = jeton(v)
        if not j or j == v:
            continue
        ecrit = re.sub(r'\s*,\s*', ', ', v)
        regles.append(f'  html[data-exp] [style*="font-size: {ecrit}"],html[data-exp] [style*="font-size:{v}"]{{font-size:{j} !important;}}\n')
    # Chivo n'est chargée qu'en 400, 600 et 700 : le 800 était simulé par le navigateur
    regles.append('  html[data-exp] [style*="font-weight: 800"],html[data-exp] [style*="font-weight:800"]{font-weight:700 !important;}\n')
    return ''.join(regles)


# Rôles qui ne se déduisent pas de la taille d'origine : posés en dernier, avec la priorité la plus haute de la couche
H = 'html[data-exp]:not(#z):not(#y):not(#x):not(#w):not(#v)'
FINITIONS = (
    f'  {H} h1{{font-size:var(--t-page) !important;text-wrap:balance;}}\n'
    # « Le Brésil, c'est… » reste un titre d'affiche : il prend la plus grande taille de l'échelle
    f'  {H} [data-bresil] > h2{{font-size:var(--t-chiffre) !important;}}\n'
    # un bouton, une taille : « Créer mon séjour » et les boutons secondaires étaient en 15, 16, 17 ou 18 px selon l'endroit
    f'  {H} :is([data-primary-cta],[data-vers-onglet]){{font-size:16px !important;font-weight:700 !important;}}\n'
    f'  {H} :is([data-camp-eyebrow],[data-camp-eyebrow] > span,[data-fusion-marque] b){{font-size:12px !important;}}\n'
    f'  {H} [data-tab-arrow]{{font-weight:700 !important;}}\n'
)


def applique(css, gabarit):
    css = feuille(css).replace('font-weight:800', 'font-weight:700')   # Chivo 800 n'est pas chargée
    return ('  /* ═══ Échelle typographique : neuf tailles (voir outils/echelle.py) ═══ */\n' + VARIABLES + en_ligne(gabarit) + css + FINITIONS)


if __name__ == '__main__':
    for v in ('9.5px', '12.5px', '13px', '15px', '15.5px', '17px', '20px', '22px', '24px', '26px', '30px', '42px', '64px',
              'clamp(17px,1.6vw,21px)', 'clamp(28px,3.6vw,44px)', 'clamp(30px,4vw,48px)', 'clamp(38px,5.6vw,68px)',
              'clamp(27px,7.6vw,33px)', 'clamp(44px,7vw,104px)', 'clamp(84px,17vw,280px)'):
        print(v.ljust(26), jeton(v), '| tel :', jeton(v, 'tel'))
