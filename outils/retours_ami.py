#!/usr/bin/env python3
"""Retours d'usage du 12/11/2026 (un ami de Kévin), posés dans .travail/ : bandeau cookies discret, croix de sortie
du tunnel, quatre packages visibles, bouton du bas de l'accueil, bloc Instagram sur l'accueil, menu « Nos surf camps »,
clins d'œil en portugais réservés aux Brésiliens. À lancer une fois après `paquet.py extraire`, avant `empaqueter`.
Les styles sont dans retours_ami.css."""
import json, os, sys
ICI = os.path.dirname(os.path.abspath(__file__)); RACINE = os.path.dirname(ICI)
G = os.path.join(RACINE, '.travail', 'gabarit.html')
T = os.path.join(RACINE, '.travail', 'textes', '71cd2ba0-e21d-4eee-9a5b-32dc222146da.js')
g = open(G, encoding='utf-8').read(); t = open(T, encoding='utf-8').read()
DEB, FIN = '<!-- retours-ami:debut -->', '<!-- retours-ami:fin -->'


def un(s, a, b, n=1):
    if s.count(a) != n:
        sys.exit(f'Repère introuvable ou ambigu ({s.count(a)}×) : {a[:80]}')
    return s.replace(a, b)


# Styles et petit script : toujours réécrits (entre deux repères), juste après le chargement de Cookiebot
css = open(os.path.join(ICI, 'retours_ami.css'), encoding='utf-8').read()
js = """(function(){document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('[data-nav-camps-menu] a');if(!a)return;var m=a.closest('[data-nav-camps]');m.setAttribute('data-clos','1');if(document.activeElement&&document.activeElement.blur)document.activeElement.blur();m.addEventListener('mouseleave',function(){m.removeAttribute('data-clos');},{once:true});});
var B='[data-bresil] [data-hscroll]';function dans(e){return e.target&&e.target.closest&&e.target.closest(B);}
['touchstart','pointerdown'].forEach(function(t){document.addEventListener(t,function(e){if(dans(e))window.__bresilArret=1;},{passive:true,capture:true});});
document.addEventListener('wheel',function(e){if(dans(e)&&Math.abs(e.deltaX)>Math.abs(e.deltaY))window.__bresilArret=1;},{passive:true,capture:true});
document.addEventListener('mouseover',function(e){window.__bresilSurvol=dans(e)?1:0;},{passive:true});})();"""
bloc = f'{DEB}\n<style>\n{css}</style>\n<script>{js}</script>\n{FIN}\n'
if DEB in g:
    g = g[:g.index(DEB)] + bloc + g[g.index(FIN) + len(FIN) + 1:]
else:
    a = "document.head.appendChild(s);})();</script>\n"
    g = un(g, a, a + bloc)

if 'data-tunnel-fermer="1"' not in g:
    # 3. Tunnel : croix de sortie
    a = '<div data-screen-label="Request to book, funnel" data-house="{{ funnelHouse }}" style="position:fixed;inset:0;z-index:200;background:#F5F2EB;display:flex;flex-direction:column;">\n  <div style="position:relative;'
    g = un(g, a, a.replace('\n  <div style="position:relative;', '\n  <div data-tunnel-tete="1" style="position:relative;'))
    a = '<a data-tunnel-logo="1" href="{{ hrefHome }}"'
    i = g.index(a); j = g.rindex('<div style="display:flex;align-items:center;gap:12px;">', 0, i)
    g = g[:j] + '<button type="button" data-tunnel-fermer="1" aria-label="Close" sc-camel-on-click="{{ closeFunnel }}" style="position:absolute;top:14px;right:clamp(10px,2vw,22px);width:38px;height:38px;border-radius:50%;border:0;background:transparent;color:#4A6A80;font-size:17px;line-height:1;cursor:pointer;" style-hover="background:rgba(54,140,175,0.14);color:#234668;">✕</button>\n    ' + g[j:]

    # 7. Clins d'œil en portugais : seulement en portugais ou pour un visiteur brésilien
    a = '<p data-bresil-note="1"'
    i = g.index(a); j = g.index('</p>', i) + 4
    g = g[:i] + '<sc-if value="{{ showBr }}" hint-placeholder-val="{{ false }}">' + g[i:j] + '</sc-if>' + g[j:]
    a = '  <!-- BRASILEIROS, em português, de propósito -->\n'
    i = g.index(a); j = g.index('</section>', i) + len('</section>')
    g = g[:i] + a + '  <sc-if value="{{ showBr }}" hint-placeholder-val="{{ false }}">\n' + g[i + len(a):j] + '\n  </sc-if>' + g[j:]

    # 5. Accueil : les comptes Instagram des camps, avant l'appel final
    ig = '''  <!-- INSTAGRAM sur l'accueil : les comptes des deux camps, comme preuve -->
  <section style="background:#F5F2EB;padding:clamp(56px,8vw,90px) clamp(24px,5vw,72px);">
    <div style="max-width:1240px;margin:0 auto;">
      <p style="font-weight:700;font-size:14px;letter-spacing:0.14em;text-transform:uppercase;color:#368CAF;margin:0 0 12px;">On Instagram</p>
      <h2 style="font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:clamp(28px,3.4vw,42px);line-height:1.08;margin:0 0 10px;color:#234668;text-wrap:pretty;">Surf Inn, day by day</h2>
      <p style="font-size:17px;line-height:1.55;color:#4A6A80;margin:0 0 26px;max-width:620px;">See the camps as they are, on their own accounts.</p>
      <div data-ig-accueil="1" style="display:grid;grid-template-columns:repeat(6,1fr);gap:6px;">
        <sc-for list="{{ homeIg }}" as="ig" hint-placeholder-count="6">
          <a href="{{ ig.url }}" target="_blank" rel="noopener" aria-label="{{ ig.label }}" style="position:relative;display:block;aspect-ratio:1;overflow:hidden;border-radius:10px;background:#C9DAE3;">
            <img src="{{ ig.img }}" alt="" loading="lazy" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;">
            <span style="position:absolute;left:8px;bottom:8px;background:rgba(23,42,62,0.62);color:#FFFFFF;font-size:11.5px;font-weight:700;padding:3px 8px;border-radius:999px;">{{ ig.handle }}</span>
          </a>
        </sc-for>
      </div>
      <div style="display:flex;gap:10px 28px;flex-wrap:wrap;margin-top:20px;font-weight:700;font-size:16px;">
        <a href="https://www.instagram.com/surfinnrio/" target="_blank" rel="noopener" style="color:#368CAF;text-decoration:none;">@surfinnrio →</a>
        <a href="https://www.instagram.com/surfinnbahia/" target="_blank" rel="noopener" style="color:#368CAF;text-decoration:none;">@surfinnbahia →</a>
      </div>
    </div>
  </section>

'''
    g = un(g, '  <section id="create-your-package"', ig + '  <section id="create-your-package"')

    # 6. Menu : « Nos surf camps » remplace les deux entrées Rio de Janeiro et Itacaré (menu ordinateur)
    i = g.index('<div data-nav-links="1"'); d = g.index('<a href="{{ hrefRio }}" data-nav-item="1"', i); m = g.index('<a href="{{ hrefItacare }}" data-nav-item="1"', d); f = g.index('</a>', m) + 4
    menu = '''<div data-nav-camps="1" data-open="{{ campsMenuOn }}" style="position:relative;display:flex;align-items:center;">
      <button type="button" data-nav-item="1" data-on="{{ navCampsOn }}" sc-camel-on-click="{{ toggleCampsMenu }}" aria-haspopup="true" style="cursor:pointer;display:inline-flex;align-items:center;gap:8px;background:none;border:0;padding-top:0;padding-left:0;padding-right:0;font:inherit;color:{{ navCampsColor }};">Our surf camps<span data-chevron="1" aria-hidden="true" style="width:6px;height:6px;border-right:2px solid currentColor;border-bottom:2px solid currentColor;transform:rotate(45deg);margin-top:-5px;"></span></button>
      <div data-nav-camps-menu="1" style="position:absolute;top:100%;left:50%;z-index:85;padding-top:10px;">
        <div style="display:flex;gap:10px;background:#FFFBF3;border:1px solid rgba(54,140,175,0.18);border-radius:18px;padding:10px;box-shadow:0 16px 40px rgba(23,42,62,0.2);">
          <sc-for list="{{ navCamps }}" as="nc" hint-placeholder-count="2">
            <a href="{{ nc.href }}" sc-camel-on-click="{{ nc.go }}" style="display:flex;flex-direction:column;width:220px;border-radius:12px;overflow:hidden;text-decoration:none;cursor:pointer;background:#FFFFFF;">
              <span style="position:relative;display:block;height:128px;overflow:hidden;background:#C9DAE3;"><img src="{{ nc.img }}" alt="" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{{ nc.pos }};"></span>
              <span style="padding:12px 14px 2px;font-weight:800;font-size:17px;color:#234668;white-space:nowrap;text-shadow:none;">{{ nc.name }}</span>
              <span style="padding:0 14px 14px;font-weight:600;font-size:13px;color:#4A6A80;white-space:nowrap;text-shadow:none;">{{ nc.sub }}</span>
            </a>
          </sc-for>
        </div>
      </div>
    </div>'''
    g = g[:d] + menu + g[f:]

    # Données
    donnees = '''      showBr: this.state.lang === 'pt' || this.isBrazilian(),
      homeIg: [['rio', 'Rio insta 1-c.webp'], ['bahia', 'Bahia insta 3-c.webp'], ['rio', 'Rio insta 3-c.webp'], ['bahia', 'Bahia insta 6-c.webp'], ['rio', 'Rio insta 5-c.webp'], ['bahia', 'Bahia insta 5-c.webp']].map(x => ({ img: window.__asset('uploads/' + x[1]), handle: '@surfinn' + x[0], label: '@surfinn' + x[0] + ' on Instagram', url: 'https://www.instagram.com/surfinn' + x[0] + '/' })),
      campsMenuOn: this.state.campsMenu ? '1' : '0',
      toggleCampsMenu: (e) => { e.stopPropagation(); this.setState(s => ({ campsMenu: !s.campsMenu, langMenuOpen: false })); },
      navCampsOn: (page === 'rio' || page === 'itacare') ? '1' : '0', navCampsColor: (page === 'rio' || page === 'itacare') ? '#ED6267' : '#234668',
      navCamps: [
        { name: 'Rio de Janeiro', sub: 'Recreio · Praia da Macumba', img: window.__asset('uploads/ph-rio-cta-m.webp'), pos: '50% 60%', href: this.adresse('rio', 'overview', this.state.lang), go: this.lienVers('rio') },
        { name: 'Itacaré', sub: 'Bahia · Mata Atlântica', img: window.__asset('uploads/ph-ita-headland-m.webp'), pos: '50% 50%', href: this.adresse('itacare', 'overview', this.state.lang), go: this.lienVers('itacare') },
      ],
'''
    a = "      isWho: page === 'who', isFaq: page === 'faq',"
    g = un(g, a, donnees + a)
    a = "this._langDoc = () => { if (this.state.langMenuOpen) this.setState({ langMenuOpen: false }); };"
    g = un(g, a, "this._langDoc = () => { if (this.state.langMenuOpen || this.state.campsMenu) this.setState({ langMenuOpen: false, campsMenu: false }); };")

# 7 bis (retour de Kévin) : les clins d'œil en portugais restent visibles par tous, précédés d'une amorce dans la langue du visiteur
SI = '<sc-if value="{{ showBr }}" hint-placeholder-val="{{ false }}">'
if SI in g:
    i = g.index(SI + '<p data-bresil-note="1"'); j = g.index('</p></sc-if>', i)
    g = g[:i] + g[i + len(SI):j] + '</p>' + g[j + len('</p></sc-if>'):]
    i = g.index('  ' + SI + '\n'); j = g.index('\n  </sc-if>', i)
    g = g[:i] + g[i + len('  ' + SI + '\n'):j] + g[j + len('\n  </sc-if>'):]
    g = un(g, "showBr: this.state.lang === 'pt' || this.isBrazilian(),", "showBrLead: this.state.lang !== 'pt',")
if 'data-br-amorce' not in g:
    AM = '<sc-if value="{{ showBrLead }}" hint-placeholder-val="{{ true }}">'
    i = g.index('<p data-bresil-note="1"'); k = g.index('>', i) + 1; j = g.index('</p>', k)
    g = g[:k] + AM + '<span data-br-amorce="1" style="font-style:normal;font-weight:700;">For the Brazilians passing by:</span> </sc-if><span lang="pt-BR">' + g[k:j] + '</span>' + g[j:]
    a = '  <!-- BRASILEIROS, em português, de propósito -->\n'
    i = g.index(a); k = g.index('<p style="font-weight:700;font-size:13px;letter-spacing:0.14em;text-transform:uppercase;color:#C4353B;', i)
    g = g[:k] + AM + '<p data-br-amorce="1" style="font-size:14.5px;font-weight:600;color:#33566E;margin:0 0 12px;">A word in Portuguese, for our Brazilian guests.</p></sc-if>\n        ' + g[k:]

# 7 ter (retour de Kévin) : l'amorce devient le même mot dans la langue du visiteur (« Brésilien ? »), suivi du portugais
g = g.replace('>For the Brazilians passing by:</span>', '>Brazilian?</span>')
AV = '<sc-if value="{{ showBrLead }}" hint-placeholder-val="{{ true }}"><p data-br-amorce="1" style="font-size:14.5px;font-weight:600;color:#33566E;margin:0 0 12px;">A word in Portuguese, for our Brazilian guests.</p></sc-if>\n        '
if AV in g:
    i = g.index(AV); g = g[:i] + g[i + len(AV):]
    k = g.index('>', i) + 1
    g = g[:k] + '<sc-if value="{{ showBrLead }}" hint-placeholder-val="{{ true }}"><span data-br-amorce="1" style="color:#234668;">Brazilian?</span> </sc-if>' + g[k:]

# Aperçu des pages camp (version sans couche expérientielle) : « Voir toutes les expériences » et « Voir les packages et les cours »
# prennent le bouton plein de « Voir le camp ». Sur les refontes, c'est outils/experience.py qui s'en charge.
if not os.path.exists(os.path.join(ICI, 'experience.py')):
    BOUTON = ' data-vers-onglet="1" style="cursor:pointer;display:inline-block;align-self:flex-start;background:#234668;color:#FFF8EF;padding:15px 30px;border-radius:999px;font-weight:800;font-size:16px;" style-hover="background:#368CAF;">'
    for debut in ('<span sc-camel-on-click="{{ goTabExperiences }}" data-coral-text="1" style="cursor:pointer;align-self:flex-start;', '<span sc-camel-on-click="{{ goTabLessons }}" style="cursor:pointer;font-weight:700;color:#368CAF;'):
        if debut in g:
            i = g.index(debut); j = g.index('>', i) + 1
            g = g[:i] + debut[:debut.index('}}"') + 3] + BOUTON + g[j:]

# « Le Brésil, c'est… » : le défilement automatique des mots ne tourne que lorsque la section est à l'écran, et part de « surfer »
AV = """    this._brTimer = setInterval(() => {
      if (!this.state.brazilAuto || this.state.page !== null && this.state.page !== 'home') return;
      const ws = ['surfing', 'playing', 'belonging', 'discovering'];
      this.setState(s => ({ brazilWord: ws[(ws.indexOf(s.brazilWord) + 1) % ws.length] }));
    }, 5000);"""
AP = """    this._brTimer = setInterval(() => {
      const ws = ['surfing', 'playing', 'belonging', 'discovering'];
      if (!this.state.brazilAuto) return;
      if (this.state.page !== null && this.state.page !== 'home') { this._brTic = 0; if (this.state.brazilWord !== ws[0]) this.setState({ brazilWord: ws[0] }); return; }
      const mots = document.querySelector('[data-bresil-mots]'); if (!mots) return;
      const r = mots.getBoundingClientRect();
      if (!(r.top < window.innerHeight * 0.8 && r.bottom > 80)) return;
      this._brTic = (this._brTic || 0) + 1;
      if (this._brTic < 5) return;
      this._brTic = 0;
      this.setState(s => ({ brazilWord: ws[(ws.indexOf(s.brazilWord) + 1) % ws.length] }));
    }, 1000);"""
# … et il s'arrête pour de bon dès que le visiteur touche aux photos (doigt, clic, molette horizontale) ; en pause tant que la souris est dessus
AP2 = AP.replace("      if (!this.state.brazilAuto) return;\n", "      if (!this.state.brazilAuto || window.__bresilArret) return;\n").replace("      const r = mots.getBoundingClientRect();\n", "      if (window.__bresilSurvol) return;\n      const r = mots.getBoundingClientRect();\n")
assert AP2 != AP and '__bresilSurvol' in AP2
if AV in g:
    g = g.replace(AV, AP2)
elif AP in g:
    g = g.replace(AP, AP2)
elif AP2 not in g:
    sys.exit('Minuterie du Brésil introuvable')

# Alignement de « Nos surf camps » avec les autres entrées du menu (le bouton reprend leurs marges)
g = g.replace('background:none;border:0;padding:0 0 9px;margin:0;font:inherit;', 'background:none;border:0;padding-top:0;padding-left:0;padding-right:0;font:inherit;')
open(G, 'w', encoding='utf-8').write(g)

TR = {
    'Our surf camps': ('Nos surf camps', 'Nossos surf camps'),
    'On Instagram': ('Sur Instagram', 'No Instagram'),
    'Surf Inn, day by day': ('Surf Inn, au jour le jour', 'Surf Inn, no dia a dia'),
    'See the camps as they are, on their own accounts.': ('Les camps tels qu’ils sont, sur leurs propres comptes.', 'Os camps como eles são, nas próprias contas.'),
    'For the Brazilians passing by:': ('Pour les Brésiliens de passage :', 'For the Brazilians passing by:'),
    'A word in Portuguese, for our Brazilian guests.': ('Un mot en portugais, pour nos voyageurs brésiliens.', 'A word in Portuguese, for our Brazilian guests.'),
    'Brazilian?': ('Brésilien ?', 'Brazilian?'),
    '@surfinnrio on Instagram': ('@surfinnrio sur Instagram', '@surfinnrio no Instagram'),
    '@surfinnbahia on Instagram': ('@surfinnbahia sur Instagram', '@surfinnbahia no Instagram'),
}
for n, (lang, ancre) in enumerate((('fr', '  "fr": {\n'), ('pt', '  "pt": {\n'))):
    deb = t.index(ancre); fin = t.index('\n  }', deb); blocl = t[deb:fin]
    lignes = ''.join('    %s: %s,\n' % (json.dumps(k, ensure_ascii=False), json.dumps(v[n], ensure_ascii=False)) for k, v in TR.items() if json.dumps(k, ensure_ascii=False) + ':' not in blocl)
    if lignes:
        t = t[:deb + len(ancre)] + '    // Retours d’usage du 12/11/2026\n' + lignes + t[deb + len(ancre):]
open(T, 'w', encoding='utf-8').write(t)
print('Retours posés')
