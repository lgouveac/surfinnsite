#!/usr/bin/env python3
"""Extrait et réempaquette index.html (format « bundler » hérité de Claude Design).

    python3 outils/paquet.py extraire     # écrit .travail/ (gabarit et textes décodés)
    python3 outils/paquet.py empaqueter   # réécrit index.html depuis .travail/

.travail/ contient :
  gabarit.html              le gabarit HTML (bloc __bundler/template), où vit le code du site
  textes/<uuid>.<ext>       les ressources texte du manifeste (i18n, runtime, CSS…), décompressées
index.html reste la seule référence : .travail/ est jetable (ignoré par git).

Les images ne sont plus dans le manifeste : elles sont servies depuis assets/ et listées
dans le bloc __bundler/external (uuid -> chemin), lu par le chargeur.
"""
import base64, gzip, json, os, re, sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(RACINE, 'index.html')
TRAVAIL = os.path.join(RACINE, '.travail')
EXT = {'text/javascript': 'js', 'application/javascript': 'js', 'text/css': 'css', 'text/html': 'html', 'image/svg+xml': 'svg'}


def bloc(s, typ):
    m = re.search(r'<script type="' + re.escape(typ) + r'">', s)
    if not m:
        return None
    debut = m.end()
    return debut, s.index('</script>', debut)


def lire():
    return open(INDEX, encoding='utf-8').read()


def encoder_json_script(obj):
    # Même échappement que le bundler : pas de « </ » brut dans un bloc script.
    return json.dumps(obj, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\u002F')


def extraire():
    s = lire()
    d, f = bloc(s, '__bundler/template')
    os.makedirs(os.path.join(TRAVAIL, 'textes'), exist_ok=True)
    open(os.path.join(TRAVAIL, 'gabarit.html'), 'w', encoding='utf-8').write(json.loads(s[d:f]))
    d, f = bloc(s, '__bundler/manifest')
    man = json.loads(s[d:f])
    n = 0
    for uuid, e in man.items():
        if e['mime'] in EXT:
            data = base64.b64decode(e['data'])
            if e['compressed']:
                data = gzip.decompress(data)
            open(os.path.join(TRAVAIL, 'textes', f"{uuid}.{EXT[e['mime']]}"), 'wb').write(data)
            n += 1
    print(f'Extrait : gabarit + {n} textes dans .travail/')


def empaqueter():
    s = lire()
    gab = open(os.path.join(TRAVAIL, 'gabarit.html'), encoding='utf-8').read()
    d, f = bloc(s, '__bundler/manifest')
    man = json.loads(s[d:f])
    for uuid, e in man.items():
        if e['mime'] in EXT:
            p = os.path.join(TRAVAIL, 'textes', f"{uuid}.{EXT[e['mime']]}")
            if os.path.exists(p):
                data = open(p, 'rb').read()
                e['data'] = base64.b64encode(gzip.compress(data, 9, mtime=0) if e['compressed'] else data).decode()
    s = s[:d] + '\n' + encoder_json_script(man) + '\n  ' + s[f:]
    d, f = bloc(s, '__bundler/template')
    s = s[:d] + '\n' + encoder_json_script(gab) + '\n  ' + s[f:]
    open(INDEX, 'w', encoding='utf-8').write(s)
    print(f'index.html réécrit ({len(s.encode()) / 1e6:.2f} Mo)')




def externaliser():
    """Sort les images du manifeste vers assets/<empreinte>.<ext> (opération unique)."""
    import hashlib
    s = lire()
    d, f = bloc(s, '__bundler/manifest')
    man = json.loads(s[d:f])
    ext_img = {'image/webp': 'webp', 'image/png': 'png', 'image/jpeg': 'jpg'}
    os.makedirs(os.path.join(RACINE, 'assets'), exist_ok=True)
    externes = {}
    for uuid in list(man):
        e = man[uuid]
        if e['mime'] in ext_img:
            data = base64.b64decode(e['data'])
            if e['compressed']:
                data = gzip.decompress(data)
            nom = hashlib.sha256(data).hexdigest()[:16] + '.' + ext_img[e['mime']]
            open(os.path.join(RACINE, 'assets', nom), 'wb').write(data)
            externes[uuid] = '/assets/' + nom
            del man[uuid]
    s = s[:d] + '\n' + encoder_json_script(man) + '\n  ' + s[f:]
    blk = bloc(s, '__bundler/external')
    js = '\n' + encoder_json_script(externes) + '\n  '
    if blk:
        old = json.loads(s[blk[0]:blk[1]]); old.update(externes)
        s = s[:blk[0]] + '\n' + encoder_json_script(old) + '\n  ' + s[blk[1]:]
    else:
        i = s.index('<script type="__bundler/ext_resources">')
        s = s[:i] + '<script type="__bundler/external">' + js + '</script>\n\n  ' + s[i:]
    open(INDEX, 'w', encoding='utf-8').write(s)
    print(f'{len(externes)} images sorties dans assets/, index.html = {len(s.encode()) / 1e6:.2f} Mo')


if __name__ == '__main__':
    {'extraire': extraire, 'empaqueter': empaqueter, 'externaliser': externaliser}[sys.argv[1]]()
