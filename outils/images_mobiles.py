#!/usr/bin/env python3
"""Photos plus légères pour les téléphones (19/11/2026).

    python3 outils/images_mobiles.py      # après « empaqueter » ; idempotent

1. Pour chaque photo de assets/ (webp, jpg), fabrique des versions réduites
   assets/m/<nom>-<largeur>.webp (480, 720 et 960 px de large), seulement quand la photo
   d'origine est nettement plus large et que la version réduite pèse vraiment moins.
   Les fichiers déjà présents ne sont pas refaits. Demande Pillow (pip install Pillow).
2. Pose dans la tête de index.html, entre deux repères, un petit script qui, sur les écrans
   de 900 px de large ou moins, ajoute à chaque <img> du site la liste de ces versions (srcset)
   et la taille réellement affichée (sizes). Le téléphone télécharge alors la plus petite version
   assez nette pour son écran ; l'ordinateur n'est pas concerné.

Garde-fous du script : la galerie plein écran garde les photos d'origine (elle les précharge) ;
une image cachée au moment de l'affichage garde la photo d'origine ; une image qui s'agrandit
ensuite (rotation du téléphone…) reçoit une version plus grande ; toute erreur laisse l'image
telle qu'avant.
"""
import json, os, re, sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(RACINE, 'assets')
SORTIE = os.path.join(ASSETS, 'm')
INDEX = os.path.join(RACINE, 'index.html')
LARGEURS = (480, 720, 960)
DEBUT, FIN = '<!-- images-mobiles:debut -->', '<!-- images-mobiles:fin -->'

try:
    from PIL import Image
except ImportError:
    sys.exit('Pillow manque : pip3 install Pillow')

SCRIPT = r"""<script data-images-mobiles="1">
  // Photos plus légères sur téléphone : voir outils/images_mobiles.py (fichier régénéré, ne pas modifier ici).
  (function () {
    try {
      // La largeur se lit au moment où l'image s'affiche : ici, la page n'a pas encore déclaré sa largeur mobile (Safari).
      if (!window.matchMedia) return;
      var MQ = matchMedia('(max-width: 900px)'), P = HTMLImageElement.prototype, D = Object.getOwnPropertyDescriptor(P, 'src'), SA = Element.prototype.setAttribute;
      if (!D || !D.set || !('sizes' in P) || !('srcset' in P)) return;
      var T = __TABLE__, A = '/assets/';
      var RO = window.ResizeObserver ? new ResizeObserver(function (es) {
        es.forEach(function (e) {
          var im = e.target, n = besoin(im, im.__imT);
          if (n > im.__imB * 1.1) { im.__imB = n; SA.call(im, 'sizes', n + 'px'); }
        });
      }) : null;
      function besoin(im, t) {
        var r = im.getBoundingClientRect();
        if (!r.width) return 0;
        return Math.ceil(Math.max(r.width, r.height * t[0] / t[1]));
      }
      function connue(v) {
        var i = typeof v === 'string' ? v.indexOf(A) : -1;
        return i >= 0 && T[v.slice(i + A.length)] ? i : -1;
      }
      function prepare(im, v) {
        if (im.__imS === v) return;
        if (im.__imS) { im.removeAttribute('srcset'); im.removeAttribute('sizes'); im.__imS = null; if (RO) RO.unobserve(im); }
        if (!MQ.matches || !im.isConnected || im.hasAttribute('srcset')) return;
        if (im.hasAttribute('data-gal-img') || im.closest('[data-gal-modal]')) return;
        var i = connue(v); if (i < 0) return;
        var nom = v.slice(i + A.length), t = T[nom];
        var n = besoin(im, t); if (!n) return;
        var base = v.slice(0, i + A.length) + 'm/' + nom.replace(/\.[a-z]+$/, '') + '-';
        var s = t[2].map(function (w) { return base + w + '.webp ' + w + 'w'; }).join(', ') + ', ' + v + ' ' + t[0] + 'w';
        SA.call(im, 'sizes', n + 'px'); SA.call(im, 'srcset', s);
        im.__imS = v; im.__imB = n; im.__imT = t; if (RO) RO.observe(im);
      }
      // Safari télécharge une image dès que son adresse est posée, avant même qu'elle soit dans la page :
      // l'adresse d'une image pas encore placée est gardée de côté, puis posée dès que l'image entre dans la page
      // (à ce moment on connaît sa taille). Filet : posée quoi qu'il arrive au bout de 1,5 s.
      var attente = [];
      function poser(im) {
        var v = im.__imA; if (v === undefined) return;
        im.__imA = undefined;
        try { prepare(im, v); } catch (e) {}
        SA.call(im, 'src', v);
      }
      function vider(tout) {
        var reste = [];
        for (var k = 0; k < attente.length; k++) {
          var im = attente[k];
          if (im.__imA === undefined) continue;
          if (tout || im.isConnected) poser(im); else reste.push(im);
        }
        attente = reste;
      }
      new MutationObserver(function () { if (attente.length) vider(false); })
        .observe(document, { childList: true, subtree: true });
      Object.defineProperty(P, 'src', { configurable: true, enumerable: D.enumerable,
        get: function () { if (this.__imA === undefined) return D.get.call(this); var a = document.createElement('a'); a.href = this.__imA; return a.href; },
        set: function (v) { this.__imA = undefined; try { prepare(this, v); } catch (e) {} D.set.call(this, v); } });
      Element.prototype.setAttribute = function (n, v) {
        if (this instanceof HTMLImageElement && String(n).toLowerCase() === 'src') {
          if (MQ.matches && !this.isConnected && connue(String(v)) >= 0) {
            if (this.__imA === undefined) { attente.push(this); setTimeout(function () { vider(true); }, 1500); }
            this.__imA = String(v);
            return;
          }
          this.__imA = undefined;
          try { prepare(this, String(v)); } catch (e) {}
        }
        return SA.call(this, n, v);
      };
    } catch (e) {}
  })();
  </script>"""


def variantes():
    os.makedirs(SORTIE, exist_ok=True)
    table, faites = {}, 0
    for nom in sorted(os.listdir(ASSETS)):
        if not re.search(r'\.(webp|jpe?g)$', nom, re.I):
            continue
        chemin = os.path.join(ASSETS, nom)
        with Image.open(chemin) as im:
            w0, h0 = im.size
            gardees = []
            for w in LARGEURS:
                if w0 < w * 1.15:
                    continue
                dest = os.path.join(SORTIE, re.sub(r'\.[a-z]+$', '', nom, flags=re.I) + f'-{w}.webp')
                if not os.path.exists(dest):
                    h = round(h0 * w / w0)
                    im.convert('RGB').resize((w, h), Image.LANCZOS).save(dest, 'WEBP', quality=80, method=6)
                    faites += 1
                if os.path.getsize(dest) < os.path.getsize(chemin) * 0.85:
                    gardees.append(w)
                else:
                    os.remove(dest)
            if gardees:
                table[nom] = [w0, h0, gardees]
    return table, faites


def poser(table):
    s = open(INDEX, encoding='utf-8').read()
    js = SCRIPT.replace('__TABLE__', json.dumps(table, separators=(',', ':')))
    bloc = f'{DEBUT}\n  {js}\n  {FIN}'
    if DEBUT in s:
        d, f = s.index(DEBUT), s.index(FIN) + len(FIN)
        s = s[:d] + bloc + s[f:]
    else:
        # Avant tout autre script : le crochet doit être en place avant que le site ne crée ses images.
        i = s.index('<script')
        s = s[:i] + bloc + '\n  ' + s[i:]
    open(INDEX, 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    table, faites = variantes()
    poser(table)
    n = sum(len(v[2]) for v in table.values())
    print(f'{len(table)} photos avec versions réduites ({n} fichiers, {faites} fabriqués maintenant) ; script posé dans index.html')
