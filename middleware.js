// Le cookie de pays (surfinn_country) n'est plus posé depuis le 18/11/2026 : il servait à la fenêtre réservée aux visiteurs
// au Brésil, retirée du site, et Cookiebot le signalait comme posé avant le consentement.
// Pose dans la page, avant qu'elle parte vers le visiteur, le titre, la description et les balises de partage
//    propres à l'adresse demandée (17/11/2026). Sans cela, un lien collé dans WhatsApp, Instagram ou iMessage
//    s'affiche sans image ni résumé, parce que ces services ne font pas tourner le site : ils lisent le fichier brut.
//    Les textes viennent de seo.js, le même fichier que celui lu par le site (outils/experience.py).
// Depuis le 18/11/2026, la page brute porte aussi l'adresse de référence (canonical), les versions dans les autres langues
//    (hreflang) et, sur les pages des camps, le fil d'Ariane en données structurées (JSON-LD). Jusque-là, seul le
//    JavaScript du site les posait, et un robot qui ne le fait pas tourner ne les voyait pas.
//    Pas de doublon possible : au chargement, le site remplace toute la page (document.documentElement.replaceWith),
//    donc ces balises disparaissent avec l'en-tête d'origine avant que le JavaScript pose les siennes. Elles portent de
//    toute façon les mêmes attributs que ceux que le JavaScript cherche (link[rel="canonical"],
//    link[rel="alternate"][hreflang="…"], script#fil-ariane) : s'il les trouvait, il les mettrait à jour sans en ajouter.
import { next } from '@vercel/functions';
import SEO from './seo.js';

// Toutes les adresses de page (pas les images, vidéos ni fichiers).
// blog/ : pages statiques écrites par outils/blog.py, avec leurs propres balises (23/11/2026).
export const config = { matcher: ['/((?!assets/|videos/|blog/|.*\\..*).*)'] };

const REPERE = '<title>Surf Inn</title>';
const esc = (t) => String(t).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

// Domaine écrit dans les adresses absolues (canonical, hreflang, og:url, images de partage, fil d'Ariane) (18/11/2026).
// Pour l'instant, c'est le domaine par lequel la page est demandée (aperçu Vercel compris).
// Au lancement, le prestataire Flowcode remplacera cette ligne par : return 'https://www.visitsurfinn.com';
// Le JavaScript du site, lui, réécrit ces balises avec location.origin une fois la page affichée.
function domaine(url) {
  return url.origin;
}

// En-têtes de sécurité, posés aussi par vercel.json (18/11/2026). On les répète ici parce que la documentation de Vercel
// ne dit pas que les en-têtes de vercel.json s'ajoutent à une réponse fabriquée par le middleware.
// Garder les deux listes identiques.
const SECURITE = {
  'X-Content-Type-Options': 'nosniff',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'Permissions-Policy': 'camera=(), microphone=(), geolocation=(), payment=(), usb=()',
  'X-Frame-Options': 'SAMEORIGIN',
};

// Description de chaque image de partage, pour les lecteurs d'écran (recommandée par le standard Open Graph).
const ALT = {
  accueil: { en: 'High five in the water after a surf lesson, Surf Inn', fr: 'On se tape dans la main, dans l’eau, après un cours de surf, Surf Inn', pt: 'Toca aqui dentro d’água depois de uma aula de surf, Surf Inn' },
  rio: { en: 'Recreio beach seen from above, Rio de Janeiro', fr: 'La plage de Recreio vue d’en haut, Rio de Janeiro', pt: 'A praia do Recreio vista de cima, Rio de Janeiro' },
  bahia: { en: 'The coast of Itacaré, between rainforest and ocean, Bahia', fr: 'La côte d’Itacaré, entre forêt et océan, Bahia', pt: 'A costa de Itacaré, entre a mata e o mar, Bahia' },
};

// Correspondance des adresses entre langues (18/11/2026), recopiée des tables ROUTES et ONGLETS du site et du script de
// redirection par langue en tête de index.html : [anglais, français, portugais]. À tenir à jour avec eux.
const PAGES = [
  ['', '', ''],
  ['who-is-it-for/', 'pour-qui/', 'para-quem/'],
  ['work-and-surf/', 'travailler-et-surfer/', 'trabalhar-e-surfar/'],
  ['about-us/', 'a-propos/', 'sobre-nos/'],
  ['reviews/', 'avis/', 'avaliacoes/'],
  ['faq/', 'faq/', 'perguntas-frequentes/'],
  ['contact/', 'contact/', 'contato/'],
  ['legal/', 'informations-legales/', 'informacoes-legais/'],
  ['privacy/', 'confidentialite/', 'privacidade/'],
  ['booking-terms/', 'conditions-de-reservation/', 'condicoes-de-reserva/'],
];
const CAMPS = { 'rio-de-janeiro': 'Rio de Janeiro', itacare: 'Itacaré' };
// Onglets des pages camp, avec le nom utilisé dans le fil d'Ariane (le même que celui du JavaScript du site).
const ONGLETS = [
  { slug: ['', '', ''], nom: null },
  { slug: ['accommodation/', 'hebergement/', 'hospedagem/'], nom: ['Accommodation', 'Hébergement', 'Hospedagem'] },
  { slug: ['activities/', 'activites/', 'atividades/'], nom: ['Activities', 'Activités', 'Atividades'] },
  { slug: ['packages/', 'sejours/', 'pacotes/'], nom: ['Surf packages', 'Séjours surf', 'Pacotes de surf'] },
  { slug: ['surf-guide/', 'guide-surf/', 'guia-de-surf/'], nom: ['Surf guide', 'Guide du surf', 'Guia de surf'] },
];
const LANGUES = ['en', 'fr', 'pt'];
const ACCUEIL = ['Home', 'Accueil', 'Início'];
const prefixe = (k) => (k === 0 ? '/' : '/' + LANGUES[k] + '/');

// Retrouve, pour une adresse connue de seo.js, la même page dans les trois langues, et le fil d'Ariane des pages camp.
// Renvoie null si l'adresse n'est pas reconnue : on ne pose alors ni canonical ni hreflang.
function versions(chemin) {
  const k = chemin.startsWith('/fr/') ? 1 : chemin.startsWith('/pt/') ? 2 : 0;
  const reste = chemin.slice(prefixe(k).length);
  const m = /^surf-camp\/(rio-de-janeiro|itacare)\/(.*)$/.exec(reste);
  if (m) {
    const onglet = ONGLETS.find((o) => o.slug[k] === m[2]);
    if (!onglet) return null;
    const adresse = (x, o) => prefixe(x) + 'surf-camp/' + m[1] + '/' + o.slug[x];
    const fil = [[ACCUEIL[k], prefixe(k)], [CAMPS[m[1]], adresse(k, ONGLETS[0])]];
    if (onglet.nom) fil.push([onglet.nom[k], adresse(k, onglet)]);
    return { langue: k, adresses: LANGUES.map((_, x) => adresse(x, onglet)), fil };
  }
  const page = PAGES.find((p) => p[k] === reste);
  if (!page) return null;
  return { langue: k, adresses: LANGUES.map((_, x) => prefixe(x) + page[x]), fil: null };
}

function tete(chemin, origine) {
  const s = SEO[chemin];
  if (!s) return null;
  const langue = chemin.startsWith('/fr/') ? 'fr' : chemin.startsWith('/pt/') ? 'pt' : 'en';
  const local = { en: 'en_US', fr: 'fr_FR', pt: 'pt_BR' }[langue];
  const url = origine + chemin;
  const image = origine + '/assets/partage-' + s.i + '-v3.jpg';
  // Dans un aperçu de partage, le titre est court et sans le nom de la marque (déjà sur la photo), la description tient en 80 caractères.
  const titre = s.st || s.t, resume = s.sd || s.d;
  const alt = ALT[s.i] ? ALT[s.i][langue] : 'Surf Inn';
  const lignes = [
    '<title>' + esc(s.t) + '</title>',
    '<meta name="description" content="' + esc(s.d) + '">',
    '<meta property="og:type" content="website">',
    '<meta property="og:site_name" content="Surf Inn">',
    '<meta property="og:locale" content="' + local + '">',
    '<meta property="og:title" content="' + esc(titre) + '">',
    '<meta property="og:description" content="' + esc(resume) + '">',
    '<meta property="og:url" content="' + esc(url) + '">',
    '<meta property="og:image" content="' + esc(image) + '">',
    '<meta property="og:image:width" content="1200">',
    '<meta property="og:image:height" content="630">',
    '<meta property="og:image:alt" content="' + esc(alt) + '">',
    '<meta name="twitter:card" content="summary_large_image">',
    '<meta name="twitter:title" content="' + esc(titre) + '">',
    '<meta name="twitter:description" content="' + esc(resume) + '">',
    '<meta name="twitter:image" content="' + esc(image) + '">',
  ];
  // Canonical, hreflang (x-default = version anglaise) et fil d'Ariane, dans le même ordre et la même forme que le JavaScript du site.
  const v = versions(chemin);
  if (v) {
    lignes.push('<link rel="canonical" href="' + esc(origine + v.adresses[v.langue]) + '">');
    LANGUES.forEach((x, i) => lignes.push('<link rel="alternate" hreflang="' + x + '" href="' + esc(origine + v.adresses[i]) + '">'));
    lignes.push('<link rel="alternate" hreflang="x-default" href="' + esc(origine + v.adresses[0]) + '">');
    if (v.fil) {
      const donnees = { '@context': 'https://schema.org', '@type': 'BreadcrumbList', itemListElement: v.fil.map((e, i) => ({ '@type': 'ListItem', position: i + 1, name: e[0], item: origine + e[1] })) };
      // « < » est écrit < pour qu'aucun texte ne puisse fermer la balise script avant l'heure.
      lignes.push('<script type="application/ld+json" id="fil-ariane">' + JSON.stringify(donnees).replace(/</g, '\\u003c') + '</script>');
    }
  }
  return lignes.join('\n  ');
}

// Empreinte de la page servie (18/11/2026) : elle change si index.html change (son ETag chez Vercel) ou si ce qu'on injecte
// change (textes de seo.js, domaine, code de ce fichier). Faible (W/) parce que Vercel peut recompresser la réponse.
async function empreinte(etagIndex, balises) {
  const octets = new TextEncoder().encode(etagIndex + '\n' + balises);
  const h = new Uint8Array(await crypto.subtle.digest('SHA-256', octets));
  return 'W/"si-' + Array.from(h.slice(0, 16), (b) => b.toString(16).padStart(2, '0')).join('') + '"';
}

// Comparaison faible d'If-None-Match, comme le prévoit HTTP : on ignore le préfixe W/ des deux côtés.
function correspond(entete, etag) {
  if (!entete) return false;
  const nu = (x) => x.trim().replace(/^W\//, '');
  return entete.split(',').some((x) => x.trim() === '*' || nu(x) === nu(etag));
}

function entetes(etag) {
  const h = new Headers();
  h.set('Content-Type', 'text/html; charset=utf-8');
  // Le navigateur garde la page mais redemande à chaque visite si elle a changé : une réponse 304, sans corps, s'il n'y a rien de neuf.
  // Pas de s-maxage : la documentation de Vercel ne dit pas que le cache du réseau Vercel garde une réponse fabriquée par un middleware.
  h.set('Cache-Control', 'public, max-age=0, must-revalidate');
  if (etag) h.set('ETag', etag);
  for (const k in SECURITE) h.set(k, SECURITE[k]);
  // Bêta : le site reste masqué aux moteurs de recherche. À retirer ici ET dans vercel.json au lancement.
  h.set('X-Robots-Tag', 'noindex, nofollow');
  return h;
}

export default async function middleware(request) {
  const suite = () => next();
  try {
    if (request.method !== 'GET') return suite();
    const url = new URL(request.url);
    // Une adresse sans barre finale est d'abord redirigée par Vercel : on la laisse passer.
    const chemin = url.pathname;
    const balises = chemin.endsWith('/') ? tete(chemin, domaine(url)) : null;
    if (!balises) return suite();

    // On va chercher le fichier du site tel quel, avec les en-têtes du visiteur (aperçus protégés compris).
    // Sans les en-têtes conditionnels : ceux du visiteur portent notre empreinte, pas celle de index.html.
    const en = new Headers(request.headers);
    for (const k of ['accept-encoding', 'if-none-match', 'if-modified-since', 'if-match', 'if-unmodified-since', 'range', 'if-range']) en.delete(k);
    const brut = await fetch(new URL('/index.html', url.origin), { headers: en, redirect: 'manual' });
    const type = brut.headers.get('content-type') || '';
    if (!brut.ok || !brut.body || !type.includes('text/html')) return suite();

    // Sans ETag de Vercel pour index.html, on sert la page comme avant, sans empreinte.
    const etagIndex = brut.headers.get('etag');
    const etag = etagIndex ? await empreinte(etagIndex, balises) : null;
    if (etag && correspond(request.headers.get('if-none-match'), etag)) {
      try { await brut.body.cancel(); } catch (e) {}
      return new Response(null, { status: 304, headers: entetes(etag) });
    }

    // Le titre est dans les premiers octets : on remplace le repère au passage, puis le reste du fichier défile sans être touché.
    const dec = new TextDecoder(), enc = new TextEncoder();
    let debut = '', fait = false;
    const flux = brut.body.pipeThrough(new TransformStream({
      transform(morceau, sortie) {
        if (fait) { sortie.enqueue(morceau); return; }
        debut += dec.decode(morceau, { stream: true });
        const i = debut.indexOf(REPERE);
        if (i >= 0) {
          sortie.enqueue(enc.encode(debut.slice(0, i) + balises + debut.slice(i + REPERE.length)));
          fait = true; debut = '';
        } else if (debut.length > 65536) {
          sortie.enqueue(enc.encode(debut)); fait = true; debut = '';
        }
      },
      flush(sortie) { if (!fait && debut) sortie.enqueue(enc.encode(debut)); },
    }));

    return new Response(flux, { status: 200, headers: entetes(etag) });
  } catch (e) {
    // Au moindre doute, le site est servi comme avant.
    return suite();
  }
}
