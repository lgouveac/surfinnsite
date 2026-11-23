// Couche expérientielle : révélations au défilement, pellicule « Le Brésil, c'est… », texte de « Pourquoi Surf Inn existe ».
// Attention au moteur de gabarit : pas de nom en camelCase juste avant « = ».
(function () {
  if (!('IntersectionObserver' in window) || !window.CSS || !CSS.supports('translate', '0 1px')) return;
  var racine = document.documentElement;
  var calme = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  racine.setAttribute('data-exp', '1');
  var vu = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.setAttribute('data-vu', '1'); vu.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -6% 0px', threshold: 0.06 });
  var joue = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.setAttribute('data-joue', '1'); joue.unobserve(e.target); } });
  }, { threshold: 0.12 });

  function revele() {
    if (calme) return;
    var h = window.innerHeight;
    document.querySelectorAll('section h2:not([data-rev]), [data-piliers] > *:not([data-rev]), [data-verbes] > *:not([data-rev]), [data-profils] > *:not([data-rev]), [data-quotidien] > *:not([data-rev]), [data-equipe] > *:not([data-rev]), [data-hscroll] > *:not([data-rev]), [data-methode] > *:not([data-rev]), [data-lieux] > *:not([data-rev]), [data-tirages] > *:not([data-rev]), [data-inclus] > *:not([data-rev]), [data-saisons] > *:not([data-rev]), [data-spots] > *:not([data-rev])').forEach(function (el) {
      if (el.closest('[data-bresil]') && el.tagName !== 'H2') return;
      if (el.tagName === 'H2' && el.closest('[data-profils]')) return;
      el.setAttribute('data-rev', '1');
      var r = el.getBoundingClientRect();
      if (r.top < h * 0.92 && r.left < window.innerWidth) { el.setAttribute('data-vu', '1'); return; }
      if (el.tagName !== 'H2') { var rang = [].indexOf.call(el.parentNode.children, el) % 6; el.style.setProperty('--rev-d', (rang * 0.07).toFixed(2) + 's'); }
      vu.observe(el);
    });
  }

  function rejoue(bande) {
    bande.removeAttribute('data-joue'); void bande.offsetWidth; bande.setAttribute('data-joue', '1');
    if (bande.scrollTo) bande.scrollTo(0, 0);
  }

  function bresil() {
    var bande = document.querySelector('[data-bresil] [data-hscroll]');
    if (!bande || bande.hasAttribute('data-exp-pret')) return;
    bande.setAttribute('data-exp-pret', '1');
    if (calme) { bande.setAttribute('data-joue', '1'); } else { joue.observe(bande); }
    // Quand le mot change (clic ou rotation automatique), les photos rejouent leur entrée
    var attente = 0;
    new MutationObserver(function () {
      if (calme || !bande.hasAttribute('data-joue')) return;
      clearTimeout(attente); attente = setTimeout(function () { rejoue(bande); }, 30);
    }).observe(bande, { subtree: true, attributes: true, attributeFilter: ['src'] });
    // Glisser à la souris
    var x0 = null, s0 = 0, glisse = false;
    bande.addEventListener('pointerdown', function (e) { if ('mouse' !== e.pointerType) return; x0 = e.clientX; s0 = bande.scrollLeft; glisse = false; });
    window.addEventListener('pointermove', function (e) {
      if (x0 === null) return;
      var d = e.clientX - x0;
      if (Math.abs(d) > 6) { glisse = true; bande.style.setProperty('scroll-snap-type', 'none'); bande.style.setProperty('cursor', 'grabbing'); }
      if (glisse) bande.scrollTo(s0 - d, 0);
    });
    window.addEventListener('pointerup', function () { if (x0 === null) return; x0 = null; bande.style.removeProperty('scroll-snap-type'); bande.style.removeProperty('cursor'); });
    bande.addEventListener('click', function (e) { if (glisse) { e.stopPropagation(); e.preventDefault(); glisse = false; } }, true);
    bande.addEventListener('dragstart', function (e) { e.preventDefault(); });
  }

  function borne(v) { return Math.max(0, Math.min(1, v)); }
  function pourquoi() {
    var sec = document.querySelector('[data-pourquoi]');
    if (!sec || calme) return;
    var h = window.innerHeight, r = sec.getBoundingClientRect();
    if (r.bottom < 0 || r.top > h) return;
    var photo = sec.querySelector('[data-pourquoi-photo]'), texte = sec.querySelector('[data-pourquoi-texte]');
    if (photo) {
      var rp = photo.getBoundingClientRect();
      sec.style.setProperty('--pq', borne((h - rp.top) / (h * 0.6)).toFixed(3));
      sec.style.setProperty('--pq2', borne((h - rp.top) / (h + rp.height)).toFixed(3));
    }
    if (texte) { var rt = texte.getBoundingClientRect(); sec.style.setProperty('--pt', borne((h * 0.94 - rt.top) / (h * 0.5)).toFixed(3)); }
  }

  // La photo glisse dans son cadre : --pp va de 0 (le cadre entre par le bas) à 1 (il sort par le haut)
  function parallaxe() {
    if (calme) return;
    var h = window.innerHeight;
    document.querySelectorAll('[data-m-img], #create-your-package, [data-appel]').forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.bottom < 0 || r.top > h) return;
      el.style.setProperty('--pp', borne((h - r.top) / (h + r.height)).toFixed(3));
    });
  }

  // Les chiffres des pages camp comptent jusqu'à leur valeur ; le texte d'origine est remis tel quel à la fin
  function compte(el) {
    var n = el;                                             // le moteur enveloppe la valeur dans un span : on descend jusqu'au texte
    while (n && n.nodeType !== 3) n = n.firstChild;
    if (!n) return;
    var fin = n.data, m = fin.match(/\d+(?:[.,]\d+)?/);
    if (!m) return;
    var cible = parseFloat(m[0].replace(',', '.')), dec = (m[0].split(/[.,]/)[1] || '').length, sep = m[0].indexOf(',') > -1 ? ',' : '.';
    var t0 = performance.now(), attendu = fin;
    (function pas(t) {
      if (n.data !== attendu) return;                       // le site a réécrit le texte entre-temps : on ne touche plus
      var k = Math.min(1, (t - t0) / 1300);
      if (k >= 1) { n.data = fin; return; }
      attendu = fin.replace(m[0], (cible * (1 - Math.pow(1 - k, 3))).toFixed(dec).replace('.', sep));
      n.data = attendu;
      requestAnimationFrame(pas);
    })(t0);
  }
  var compteur = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { compteur.unobserve(e.target); compte(e.target); } });
  }, { threshold: 0.6 });
  function chiffres() {
    if (calme) return;
    document.querySelectorAll('[data-chiffres] > * > span:first-child:not([data-compte]), [data-faits] > * > span:first-child:not([data-compte])').forEach(function (el) { el.setAttribute('data-compte', '1'); compteur.observe(el); });
  }

  // Guide surf : la houle dessinée au pied de chaque saison monte selon la taille des vagues annoncée
  function houle() {
    document.querySelectorAll('[data-saisons] > *:not([data-houle])').forEach(function (el) {
      var l = el.querySelector(':scope > div:nth-of-type(2) > div:nth-child(3) > span:last-child');
      var n = ((l && l.textContent) || '').replace(/,/g, '.').match(/\d+(\.\d+)?/g);
      if (!n) return;
      var haut = Math.max.apply(null, n.map(Number));
      el.setAttribute('data-houle', '1');
      el.style.setProperty('--houle', borne((haut - 0.6) / 1.9).toFixed(2));
    });
  }

  // Libellé affiché sous la planche : le petit titre au-dessus du titre de section s'il existe (plus court), sinon le titre
  var libelles = { fr: { 'avis': 'Nos avis' } };
  window.surfinn_libelle = function (h) {
    var p = h.previousElementSibling, t = '';
    if (p && p.tagName === 'P') t = ((p.firstElementChild || p).textContent || '').trim();
    if (!t || t.length > 40) t = (h.innerText || '').replace(/\s+/g, ' ').trim();
    var l = (racine.lang || 'en').slice(0, 2), m = libelles[l] && libelles[l][t.toLowerCase()];
    return m || t;
  };

  // Vidéos de fond : l'image d'attente reste affichée tant que la vidéo ne joue pas vraiment (jamais de bouton de lecture du
  // navigateur à l'écran), avec un filet lumineux en bas du cadre pendant le chargement
  function videos() {
    document.querySelectorAll('video[poster]:not([data-vid])').forEach(function (v) {
      v.setAttribute('data-vid', '1');
      var cadre = v.parentNode, grand = v.offsetHeight > 300;
      function pret() { v.setAttribute('data-vid-ok', '1'); cadre.removeAttribute('data-vid-attente'); }
      if (!v.paused && v.readyState > 2 && v.currentTime > 0) { pret(); return; }
      if (v.poster) { cadre.style.setProperty('background-image', 'url("' + v.poster + '")'); cadre.style.setProperty('background-size', 'cover'); cadre.style.setProperty('background-position', '50% 50%'); }
      if (grand) { cadre.setAttribute('data-vid-attente', '1'); setTimeout(function () { cadre.removeAttribute('data-vid-attente'); }, 9000); }
      v.addEventListener('playing', pret);
      v.addEventListener('timeupdate', function () { if (v.currentTime > 0.05) pret(); });
    });
  }

  // Tunnel : après le choix du camp, on amène les dates à l'écran si elles n'y sont pas (sur téléphone, on restait devant les cartes)
  document.addEventListener('click', function (e) {
    var carte = e.target.closest && e.target.closest('[data-trip-dest] > *');
    if (!carte) return;
    setTimeout(function () {
      var d = document.querySelector('[data-trip-dates]'); if (!d) return;
      var r = d.getBoundingClientRect(), bas = window.innerHeight - 130;
      if (r.top >= 70 && r.bottom <= bas) return;
      d.scrollIntoView({ block: 'center', behavior: calme ? 'auto' : 'smooth' });
    }, 260);
  });

  // Tunnel : repère les étapes franchies et l'étape en cours, pour y poser la planche (voir maison.css)
  function etapes() {
    var t = document.querySelector('[data-screen-label="Request to book, funnel"]'); if (!t) return;
    var pas = [].filter.call(t.querySelectorAll('[role="button"]'), function (e) { var b = e.firstElementChild; return b && b.offsetHeight <= 10 && e.children.length === 2; });
    if (!pas.length) return;
    var cadre = pas[0].parentNode; if (!cadre.hasAttribute('data-surf-etapes')) cadre.setAttribute('data-surf-etapes', '1');
    var ici = -1;
    pas.forEach(function (e, i) { var fait = /237, 98, 103/.test(e.firstElementChild.getAttribute('style') || ''); if (fait) ici = i; if (fait !== e.hasAttribute('data-fait')) { if (fait) e.setAttribute('data-fait', '1'); else e.removeAttribute('data-fait'); } });
    pas.forEach(function (e, i) { if ((i === ici) !== e.hasAttribute('data-ici')) { if (i === ici) e.setAttribute('data-ici', '1'); else e.removeAttribute('data-ici'); } });
    // La planche : un seul élément, déplacé en douceur jusqu'au bout de l'étape en cours
    if (ici < 0) return;
    var pl = cadre.querySelector('[data-surf-planche]');
    if (!pl) {
      var NS = 'http://www.w3.org/2000/svg', mk = function (n, at) { var x = document.createElementNS(NS, n); for (var k in at) x.setAttribute(k, at[k]); return x; };
      pl = mk('svg', { 'data-surf-planche': '1', 'aria-hidden': 'true' }); pl.setAttribute('viewBox', '-36 -9 64 18');
      var g = mk('g', {});
      g.appendChild(mk('path', { 'class': 's-sillage', d: 'M-27-3.5q-5 3.5 0 7M-34-2.3q-3.4 2.3 0 4.6' }));
      g.appendChild(mk('path', { d: 'M-21 0C-21-4.8-13-6.8-3-6.8C9-6.8 19-3.8 25 0C19 3.8 9 6.8-3 6.8C-13 6.8-21 4.8-21 0Z', fill: '#F7F4EA', stroke: '#0C3B32', 'stroke-width': '1.4' }));
      g.appendChild(mk('rect', { x: '-14', y: '-6.2', width: '4.4', height: '12.4', fill: '#FFC531' }));
      g.appendChild(mk('path', { d: 'M15 -4.6C19.5 -3 22.6 -1.5 25 0C22.6 1.5 19.5 3 15 4.6Z', fill: '#F2542D' }));
      pl.appendChild(g); cadre.appendChild(pl);
      pl.addEventListener('transitionend', function (ev) { if (ev.propertyName === 'translate') pl.removeAttribute('data-file'); });
    }
    var x = Math.round(pas[ici].offsetLeft + pas[ici].offsetWidth), avant = pl.getAttribute('data-x');
    if (avant !== String(x)) {
      if (avant !== null && !calme) { pl.setAttribute('data-file', '1'); clearTimeout(pl.__t); pl.__t = setTimeout(function () { pl.removeAttribute('data-file'); }, 1900); }
      pl.setAttribute('data-x', x); pl.style.setProperty('--px', x + 'px');
    }
  }
  // Survols : les règles générées gardent le rouge de l'ancienne charte ; on les fait pointer vers la couleur d'accent du camp
  var feuilles = 0;
  function survols() {
    var total = 0, i, j, ss = document.styleSheets;
    for (i = 0; i < ss.length; i++) { try { total += ss[i].cssRules.length; } catch (e) {} }
    if (total === feuilles) return; feuilles = total;
    for (i = 0; i < ss.length; i++) {
      var rs; try { rs = ss[i].cssRules; } catch (e) { continue; }
      for (j = 0; j < rs.length; j++) {
        var r = rs[j]; if (!r.selectorText || r.selectorText.indexOf(':hover') < 0 || !/^\.scp/.test(r.selectorText)) continue;
        var t = r.style.cssText; if (!/237, 98, 103|224, 75, 81/.test(t)) continue;
        r.style.setProperty('--x', '1'); r.style['cssText']=t.replace(/rgb\((237, 98, 103|224, 75, 81)\)/g, 'var(--accent)');
      }
    }
  }
  setInterval(survols, 900);

  setInterval(etapes, 350);
  // Fenêtres ouvertes : la page derrière ne défile pas. On bloque le geste, sauf dans une zone de la fenêtre qui défile elle-même.
  // (Bloquer par overflow:hidden faisait sauter la page en haut à l'ouverture.)
  function retiens(e) {
    var t = e.target; if (!t || !t.closest) return;
    var calque = t.closest('div[style*="position: fixed"][style*="inset: 0px"]'); if (!calque) return;
    for (var n = t; n && n !== calque.parentNode; n = n.parentNode) {
      if (n.nodeType !== 1) continue; var c = getComputedStyle(n);
      if ((/auto|scroll/.test(c.overflowY) && n.scrollHeight > n.clientHeight + 2) || (/auto|scroll/.test(c.overflowX) && n.scrollWidth > n.clientWidth + 2)) return;
    }
    if (e.cancelable) e.preventDefault();
  }
  document.addEventListener('touchmove', retiens, { passive: false });
  document.addEventListener('wheel', retiens, { passive: false });

  // Emplacement des pages camp, sur téléphone : « Le quartier », « Venir », « Pourquoi cet endroit » sont repliés ; un toucher les déroule
  // Accessibilité (18/11/2026) : le titre reste un simple <h3> ; le rôle de bouton est porté par un <span> à l'intérieur.
  // React peut réécrire le texte du titre (et faire disparaître ce <span>) : il est alors remis au passage suivant.
  function emplacement() {
    document.querySelectorAll('[data-emplacement] > *').forEach(function (bloc) {
      var titre = bloc.querySelector('h3'); if (!titre) return;
      if (!bloc.hasAttribute('data-pli')) {
        bloc.setAttribute('data-pli', '0');
        bloc.addEventListener('click', function () {
          var o = bloc.getAttribute('data-pli') === '1'; bloc.setAttribute('data-pli', o ? '0' : '1');
          var b = bloc.querySelector('[data-pli-bouton]'); if (b) b.setAttribute('aria-expanded', o ? 'false' : 'true');
        });
      }
      var bouton = titre.querySelector('[data-pli-bouton]');
      if (!bouton) {
        bouton = document.createElement('span'); bouton.setAttribute('data-pli-bouton', '1');
        bouton.setAttribute('role', 'button'); bouton.setAttribute('tabindex', '0');
        while (titre.firstChild) bouton.appendChild(titre.firstChild);
        titre.appendChild(bouton);
        bouton.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); e.stopPropagation(); bouton.click(); } });
      }
      var etat = bloc.getAttribute('data-pli') === '1' ? 'true' : 'false';
      if (bouton.getAttribute('aria-expanded') !== etat) bouton.setAttribute('aria-expanded', etat);
      ['role', 'tabindex', 'aria-expanded'].forEach(function (a) { if (titre.hasAttribute(a)) titre.removeAttribute(a); });
    });
  }

  var prevu = false;
  function tout() { prevu = false; revele(); bresil(); pourquoi(); parallaxe(); chiffres(); houle(); videos(); etapes(); emplacement(); }
  function planifie() { if (prevu) return; prevu = true; requestAnimationFrame(tout); }
  var image = false;
  window.addEventListener('scroll', function () { if (image) return; image = true; requestAnimationFrame(function () { image = false; pourquoi(); parallaxe(); }); }, { passive: true });
  window.addEventListener('resize', planifie);
  new MutationObserver(planifie).observe(racine, { childList: true, subtree: true });
  planifie();
})();

// « Envoyer à un ami » et suivi des partages (17/11/2026).
// Le lien partagé porte l'étiquette ?via=ami : elle ne contient aucune donnée personnelle, elle dit seulement que la visite vient d'un partage.
// Attention au moteur de gabarit : pas de nom en camelCase juste avant « = ».
(function () {
  var mesure = function (evt) { try { (window['dataLayer'] || (window['dataLayer'] = [])).push(evt); } catch (e) {} };
  var via = '';
  try {
    var m = /[?&]via=([a-z]{1,12})(?:&|$)/.exec(location.search);
    if (m) { via = m[1]; sessionStorage.setItem('surfinn.via', via); mesure({ event: 'share_visit', via: via, page_path: location.pathname }); }
    else { via = sessionStorage.getItem('surfinn.via') || ''; }
  } catch (e) {}
  window['__via'] = via;
  var textes = {
    fr: { rio: 'Regarde ce surf camp à Rio, ça te dirait ?', itacare: 'Regarde ce surf camp à Itacaré, au Brésil, ça te dirait ?', autre: 'Regarde ces surf camps au Brésil, ça te dirait ?' },
    pt: { rio: 'Olha esse surf camp no Rio, bora?', itacare: 'Olha esse surf camp em Itacaré, bora?', autre: 'Olha esses surf camps no Brasil, bora?' },
    en: { rio: 'Look at this surf camp in Rio, are you in?', itacare: 'Look at this surf camp in Itacaré, Brazil, are you in?', autre: 'Look at these surf camps in Brazil, are you in?' }
  };
  document.addEventListener('click', function (e) {
    var lien = e.target && e.target.closest ? e.target.closest('[data-partager]') : null;
    if (!lien) return;
    e.preventDefault();
    var langue = (document.documentElement.lang || 'en').slice(0, 2); if (!textes[langue]) langue = 'en';
    var hote = document.querySelector('[data-house]'); var camp = hote ? hote.getAttribute('data-house') : '';
    var message = textes[langue][camp] || textes[langue].autre;
    var adresse = location.origin + location.pathname + '?via=ami';
    mesure({ event: 'share_click', page_path: location.pathname });
    // Sur téléphone ou tablette : le menu de partage de l'appareil. Sur ordinateur : WhatsApp directement, parce que le menu de partage
    // des navigateurs d'ordinateur échoue souvent sans rien afficher (constaté par Kévin le 18/11/2026).
    var wa = 'https://wa.me/?text=' + encodeURIComponent(message + ' ' + adresse);
    var tactile = window.matchMedia && window.matchMedia('(hover: none) and (pointer: coarse)').matches;
    if (tactile && navigator.share) {
      navigator.share({ title: document.title, text: message, url: adresse }).catch(function (err) { if (!err || err.name !== 'AbortError') location.href = wa; });
      return;
    }
    var fen = window.open(wa, '_blank');
    if (!fen) location.href = wa;
  });
  // Le champ caché du formulaire de demande reçoit l'étiquette dès qu'il apparaît.
  var pose = function () { if (!via) return; document.querySelectorAll('input[data-via]').forEach(function (c) { if (c.value !== via) c.value = via; }); };
  new MutationObserver(pose).observe(document.documentElement, { childList: true, subtree: true });
  pose();
})();

// Pages camp sur téléphone : mesure la hauteur du bloc vert sous la vidéo, pour que la vidéo occupe exactement le reste du premier écran.
// Attention au moteur de gabarit : pas de nom en camelCase juste avant « = ».
(function () {
  if (!('ResizeObserver' in window)) return;
  var vu = null, obs = new ResizeObserver(function (es) {
    // La variable est posée à l'image suivante, et seulement si la hauteur a changé : sinon le navigateur signale une boucle de mesure.
    es.forEach(function (e) { var bloc = e.target, h = Math.round(bloc.getBoundingClientRect().height); if (h <= 0 || !bloc.parentNode || bloc.__h === h) return; bloc.__h = h; requestAnimationFrame(function () { if (bloc.parentNode) bloc.parentNode.style.setProperty('--encart-h', h + 'px'); }); });
  });
  function cherche() {
    var bloc = document.querySelector('main > [data-camp-hero] > [data-camp-encart]');
    if (bloc === vu) return;
    if (vu) obs.unobserve(vu);
    vu = bloc; if (bloc) obs.observe(bloc);
  }
  new MutationObserver(cherche).observe(document.documentElement, { childList: true, subtree: true });
  cherche();
})();

/* Fenêtre de photos (18/11/2026) : pendant qu'elle est ouverte, la couleur de l'interface du navigateur (bandeau de l'heure sur
   iPhone, barre d'adresse sur Android) passe au vert du site, puis revient à sa valeur d'origine à la fermeture. */
(function () {
  var meta = document.querySelector('meta[name="theme-color"]');
  var origine = meta ? meta.getAttribute('content') : null;
  var etat = false, attente = false;
  function regler() {
    attente = false;
    var ouvert = !!document.querySelector('[data-gal-modal]');
    if (ouvert === etat) return;
    etat = ouvert;
    if (ouvert) {
      if (!meta) { meta = document.createElement('meta'); meta.setAttribute('name', 'theme-color'); document.head.appendChild(meta); }
      meta.setAttribute('content', '#0C3B32');
    } else if (meta) {
      if (origine) meta.setAttribute('content', origine); else { meta.remove(); meta = null; }
    }
  }
  new MutationObserver(function () { if (!attente) { attente = true; requestAnimationFrame(regler); } }).observe(document.documentElement, { childList: true, subtree: true });
})();
