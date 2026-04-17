#!/usr/bin/env node
// Tiny local dev server that mirrors vercel.json rewrites.
// No dependencies. Run with:  node dev-server.js  (default port 3456)

const http = require('http');
const fs = require('fs');
const path = require('path');

const ROOT = __dirname;
const PORT = Number(process.env.PORT) || 3456;

const vercel = JSON.parse(fs.readFileSync(path.join(ROOT, 'vercel.json'), 'utf8'));
const rewrites = (vercel.rewrites || []).map(r => ({
  source: r.source,
  destination: r.destination,
}));

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.mjs': 'application/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.webp': 'image/webp',
  '.ico': 'image/x-icon',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.map': 'application/json',
  '.txt': 'text/plain; charset=utf-8',
};

function safeJoin(base, reqPath) {
  const decoded = decodeURIComponent(reqPath.split('?')[0].split('#')[0]);
  const resolved = path.normalize(path.join(base, decoded));
  if (!resolved.startsWith(base)) return null;
  return resolved;
}

function tryServe(res, filePath) {
  fs.stat(filePath, (err, stat) => {
    if (err) return send404(res);
    if (stat.isDirectory()) {
      return tryServe(res, path.join(filePath, 'index.html'));
    }
    const ext = path.extname(filePath).toLowerCase();
    res.writeHead(200, {
      'Content-Type': MIME[ext] || 'application/octet-stream',
      'Cache-Control': 'no-cache',
    });
    fs.createReadStream(filePath).pipe(res);
  });
}

function send404(res) {
  res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
  res.end('<h1>404 Not Found</h1>');
}

function applyRewrites(urlPath) {
  for (const r of rewrites) {
    if (r.source === urlPath) return r.destination;
  }
  return urlPath;
}

const server = http.createServer((req, res) => {
  const reqPath = req.url.split('?')[0].split('#')[0];

  // Try direct file first
  const direct = safeJoin(ROOT, reqPath);
  if (direct && fs.existsSync(direct)) {
    return tryServe(res, direct);
  }

  // Apply vercel rewrites
  const rewritten = applyRewrites(reqPath);
  if (rewritten !== reqPath) {
    const target = safeJoin(ROOT, rewritten);
    if (target && fs.existsSync(target)) {
      return tryServe(res, target);
    }
  }

  // Try with .html
  const withHtml = safeJoin(ROOT, reqPath.replace(/\/$/, '') + '.html');
  if (withHtml && fs.existsSync(withHtml)) {
    return tryServe(res, withHtml);
  }

  // index.html fallback for "/"
  if (reqPath === '/' || reqPath === '') {
    return tryServe(res, path.join(ROOT, 'index.html'));
  }

  send404(res);
});

server.listen(PORT, () => {
  console.log(`dev-server listening on http://localhost:${PORT}`);
  console.log(`  rewrites loaded: ${rewrites.length}`);
});
