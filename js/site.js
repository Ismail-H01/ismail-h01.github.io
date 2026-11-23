/* Ismail Hussain portfolio: progressive enhancement only.
   The page is fully readable without this file (see .no-js rules in css/site.css).
   All motion is skipped when the visitor prefers reduced motion. */
(function () {
  'use strict';

  var doc = document, root = doc.documentElement;
  var $ = function (s, c) { return (c || doc).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || doc).querySelectorAll(s)); };
  var reduced = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasIO = 'IntersectionObserver' in window;
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }

  /* ---------- theme (dark by default) ---------- */
  var themeBtn = $('#themeBtn');
  function setThemeLabel() {
    var dark = root.getAttribute('data-theme') !== 'light';
    themeBtn.setAttribute('aria-label', dark ? 'Switch to light theme' : 'Switch to dark theme');
    var meta = $('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', dark ? '#0a1120' : '#f6f8fc');
  }
  themeBtn.addEventListener('click', function () {
    var next = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('theme', next); } catch (e) {}
    setThemeLabel();
    window.dispatchEvent(new Event('themechange'));
  });
  setThemeLabel();

  /* ---------- mobile menu ---------- */
  var menu = $('#menu'), menuBtn = $('#menuBtn');
  function setMenu(open) {
    menu.classList.toggle('open', open);
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  }
  menuBtn.addEventListener('click', function () { setMenu(!menu.classList.contains('open')); });
  $$('a', menu).forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
  doc.addEventListener('keydown', function (e) { if (e.key === 'Escape' && menu.classList.contains('open')) { setMenu(false); menuBtn.focus(); } });

  /* ---------- text splitting ---------- */
  // Hero name: one span per letter, rising out of a mask on load.
  var h1 = $('#hero-title');
  if (h1) {
    h1.setAttribute('aria-label', $$('[data-letters]', h1).map(function (l) { return l.textContent.trim(); }).join(' '));
    var li = 0;
    $$('[data-letters]', h1).forEach(function (line) {
      var txt = line.textContent; line.textContent = '';
      line.setAttribute('aria-hidden', 'true');
      for (var k = 0; k < txt.length; k++) {
        var s = doc.createElement('span');
        s.className = 'ch'; s.textContent = txt[k]; s.style.setProperty('--i', li++);
        line.appendChild(s);
      }
      if (line.classList.contains('grad')) line.classList.add('chars');
    });
  }
  // Keep the gradient continuous across the separately animated letters.
  function placeGradient() {
    $$('.hero-name .grad').forEach(function (line) {
      var chars = $$('.ch', line), w = 0;
      chars.forEach(function (c) { w = Math.max(w, c.offsetLeft + c.offsetWidth); });
      chars.forEach(function (c) { c.style.setProperty('--x', c.offsetLeft + 'px'); c.style.setProperty('--w', w + 'px'); });
    });
  }
  placeGradient();
  if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(placeGradient);

  // Section headings: words rise out of a mask when scrolled into view.
  $$('.split').forEach(function (el) {
    var words = el.textContent.trim().split(/\s+/);
    el.textContent = '';
    words.forEach(function (w, i) {
      var o = doc.createElement('span'), inner = doc.createElement('span');
      o.className = 'w'; inner.className = 'wi'; inner.textContent = w; inner.style.setProperty('--i', i);
      o.appendChild(inner); el.appendChild(o);
      if (i < words.length - 1) el.appendChild(doc.createTextNode(' '));
    });
  });

  // Statement paragraph: words light up with scroll position.
  var scrubs = $$('.scrub').map(function (el) {
    var words = el.textContent.trim().split(/\s+/);
    el.textContent = '';
    var spans = words.map(function (w, i) {
      var s = doc.createElement('span'); s.className = 'sw'; s.textContent = w;
      el.appendChild(s); if (i < words.length - 1) el.appendChild(doc.createTextNode(' '));
      return s;
    });
    return { el: el, spans: spans };
  });

  /* ---------- reveal on scroll ---------- */
  var reveals = $$('.reveal, .split');
  if (hasIO && !reduced) {
    var io = new IntersectionObserver(function (entries, o) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); o.unobserve(en.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }

  /* ---------- scroll-linked effects ---------- */
  var bar = $('#progress'), nav = $('#nav'), toTop = $('#toTop');
  var heroInner = $('#heroInner'), canvasEl = $('#traces');
  var timeline = $('#timeline'), tProg = $('#tProgress'), tItems = $$('.t-item');
  var ticking = false, lastY = window.pageYOffset, velocity = 0;

  function onScroll() {
    var y = window.pageYOffset, vh = window.innerHeight;
    var h = root.scrollHeight - root.clientHeight;
    velocity = y - lastY; lastY = y;
    bar.style.width = (h > 0 ? (y / h) * 100 : 0) + '%';
    nav.classList.toggle('scrolled', y > 8);
    toTop.hidden = y < 700;

    if (!reduced) {
      // Hero drifts up and fades as the page scrolls away from it.
      if (y < vh * 1.2) {
        heroInner.style.transform = 'translate3d(0,' + (y * 0.32).toFixed(1) + 'px,0)';
        heroInner.style.opacity = clamp(1 - y / (vh * 0.85), 0, 1).toFixed(3);
        canvasEl.style.transform = 'translate3d(0,' + (y * 0.15).toFixed(1) + 'px,0)';
      }
      // Statement words light up in reading order.
      scrubs.forEach(function (s) {
        var r = s.el.getBoundingClientRect();
        var p = clamp((vh * 0.85 - r.top) / (r.height + vh * 0.35), 0, 1);
        var n = Math.round(p * s.spans.length);
        s.spans.forEach(function (sp, i) { sp.classList.toggle('lit', i < n); });
      });
      // Timeline line draws downwards; each dot lights when the line reaches it.
      if (timeline) {
        var tr = timeline.getBoundingClientRect(), mark = vh * 0.6;
        tProg.style.setProperty('--p', (clamp((mark - tr.top) / tr.height, 0, 1) * 100).toFixed(1) + '%');
        tItems.forEach(function (it) { it.classList.toggle('lit', $('.t-dot', it).getBoundingClientRect().top < mark); });
      }
    }
    ticking = false;
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener('resize', function () { placeGradient(); onScroll(); });
  if (reduced) {
    scrubs.forEach(function (s) { s.spans.forEach(function (sp) { sp.classList.add('lit'); }); });
    tItems.forEach(function (it) { it.classList.add('lit'); });
  }
  onScroll();
  toTop.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: reduced ? 'auto' : 'smooth' }); });

  /* ---------- active nav link ---------- */
  var links = $$('.links a');
  if (hasIO) {
    var secIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        links.forEach(function (a) { a.classList.toggle('active', a.getAttribute('href') === '#' + en.target.id); });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    links.forEach(function (a) { var s = $(a.getAttribute('href')); if (s) secIO.observe(s); });
  }

  /* ---------- counters ---------- */
  var counters = $$('[data-count]');
  function runCounter(el) {
    var target = +el.getAttribute('data-count');
    if (reduced) { el.textContent = target; return; }
    var t0 = null, dur = 1200;
    function step(t) {
      if (t0 === null) t0 = t;
      var p = Math.min((t - t0) / dur, 1);
      el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(step); else el.textContent = target;
    }
    requestAnimationFrame(step);
  }
  if (hasIO) {
    var cio = new IntersectionObserver(function (entries, o) {
      entries.forEach(function (en) { if (en.isIntersecting) { runCounter(en.target); o.unobserve(en.target); } });
    }, { threshold: 0.6 });
    counters.forEach(function (c) { cio.observe(c); });
  }

  /* ---------- marquee: drifts, and speeds up with scrolling ---------- */
  var track = $('.marquee-track'), mPos = 0, mVisible = true;
  if (track && hasIO) new IntersectionObserver(function (e) { mVisible = e[0].isIntersecting; }).observe(track);

  /* ---------- spotlight on cards ---------- */
  $$('.card').forEach(function (c) {
    c.addEventListener('pointermove', function (e) {
      var r = c.getBoundingClientRect();
      c.style.setProperty('--mx', (e.clientX - r.left) + 'px');
      c.style.setProperty('--my', (e.clientY - r.top) + 'px');
    });
  });

  /* ---------- drop-downs ---------- */
  $$('.toggle').forEach(function (btn) {
    var panel = doc.getElementById(btn.getAttribute('aria-controls'));
    var base = btn.firstChild.textContent.trim();
    btn.addEventListener('click', function () {
      var open = !panel.classList.contains('open');
      panel.classList.toggle('open', open);
      btn.setAttribute('aria-expanded', String(open));
      btn.firstChild.textContent = (open ? 'Hide ' + (btn.getAttribute('data-label') || '') : base) + ' ';
      if (open && !reduced) setTimeout(function () {
        var r = panel.getBoundingClientRect();
        if (r.bottom > innerHeight) window.scrollBy({ top: Math.min(r.bottom - innerHeight + 24, 320), behavior: 'smooth' });
      }, 300);
    });
  });

  /* ---------- lightbox ---------- */
  var lb = $('#lb'), lbImg = $('#lbImg'), lbCap = $('#lbCap'), lbPrev = $('#lbPrev'), lbNext = $('#lbNext'), lbClose = $('#lbClose');
  var group = [], gi = 0, opener = null;
  function showLb() {
    var b = group[gi];
    lbImg.src = b.getAttribute('data-full');
    lbImg.alt = $('img', b).getAttribute('alt') || '';
    lbCap.textContent = b.getAttribute('data-caption') || '';
    lbPrev.hidden = lbNext.hidden = group.length < 2;
  }
  function openLb(btn) {
    group = $$('.shot-open[data-gallery="' + btn.getAttribute('data-gallery') + '"]');
    gi = group.indexOf(btn); opener = btn;
    showLb();
    lb.classList.add('open'); lb.setAttribute('aria-hidden', 'false');
    doc.body.style.overflow = 'hidden';
    lbClose.focus();
  }
  function closeLb() {
    lb.classList.remove('open'); lb.setAttribute('aria-hidden', 'true');
    doc.body.style.overflow = '';
    if (opener) opener.focus();
  }
  function step(d) { gi = (gi + d + group.length) % group.length; showLb(); }
  $$('.shot-open').forEach(function (b) { b.addEventListener('click', function () { openLb(b); }); });
  lbClose.addEventListener('click', closeLb);
  lbPrev.addEventListener('click', function () { step(-1); });
  lbNext.addEventListener('click', function () { step(1); });
  lb.addEventListener('click', function (e) { if (e.target === lb) closeLb(); });
  doc.addEventListener('keydown', function (e) {
    if (!lb.classList.contains('open')) return;
    if (e.key === 'Escape') closeLb();
    else if (e.key === 'ArrowLeft' && group.length > 1) step(-1);
    else if (e.key === 'ArrowRight' && group.length > 1) step(1);
    else if (e.key === 'Tab') {
      var f = [lbClose, lbPrev, lbNext].filter(function (x) { return !x.hidden; });
      var i = f.indexOf(doc.activeElement);
      e.preventDefault();
      f[(i + (e.shiftKey ? -1 : 1) + f.length) % f.length].focus();
    }
  });

  /* ---------- skills: show where each was used ---------- */
  var skillOut = $('#skillOut'), skillBtns = $$('.skill'), sources = $$('[data-skills]');
  function titleOf(el) { var h = $('h3', el); return h ? h.textContent.trim() : ''; }
  function flash(el) { el.classList.add('highlight'); setTimeout(function () { el.classList.remove('highlight'); }, 2600); }
  skillBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var on = btn.getAttribute('aria-pressed') !== 'true';
      skillBtns.forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
      sources.forEach(function (s) { s.classList.remove('highlight'); });
      if (!on) { skillOut.textContent = 'Select a skill above.'; return; }
      btn.setAttribute('aria-pressed', 'true');
      var key = btn.getAttribute('data-skill');
      var hits = sources.filter(function (s) { return s.getAttribute('data-skills').split(/\s+/).indexOf(key) > -1; });
      skillOut.textContent = '';
      var lead = doc.createElement('span');
      lead.textContent = btn.textContent + ' was used in: ';
      skillOut.appendChild(lead);
      if (!hits.length) { skillOut.appendChild(doc.createTextNode('no listed project yet.')); return; }
      hits.forEach(function (h, i) {
        var a = doc.createElement('a');
        a.href = '#' + h.id; a.textContent = titleOf(h);
        a.addEventListener('click', function () { flash(h); });
        skillOut.appendChild(a);
        if (i < hits.length - 1) skillOut.appendChild(doc.createTextNode('; '));
      });
      hits.forEach(flash);
    });
  });

  /* ---------- email: assembled in the browser, not written in the page source ---------- */
  var addr = 'ismail.h2589' + '@' + 'gmail.com';
  $$('[data-mail]').forEach(function (a) { a.setAttribute('href', 'mailto:' + addr); });
  var mt = $('#mailtext'); if (mt) mt.textContent = addr;
  var copy = $('#copyMail'), toast = $('#toast'), toastT;
  function say(msg) { toast.textContent = msg; toast.classList.add('show'); clearTimeout(toastT); toastT = setTimeout(function () { toast.classList.remove('show'); }, 2200); }
  if (copy) {
    copy.hidden = false;
    copy.addEventListener('click', function () {
      function fallback() {
        var t = doc.createElement('textarea'); t.value = addr; t.setAttribute('readonly', ''); t.style.position = 'fixed'; t.style.opacity = '0';
        doc.body.appendChild(t); t.select();
        var ok = false; try { ok = doc.execCommand('copy'); } catch (e) {}
        doc.body.removeChild(t); say(ok ? 'Email address copied' : addr);
      }
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(addr).then(function () { say('Email address copied'); }, fallback);
      else fallback();
    });
  }

  var yr = $('#yr'); if (yr) yr.textContent = new Date().getFullYear();

  /* ---------- hero: animated PCB traces ---------- */
  var cv = canvasEl, ctx = null, W = 0, H = 0, routes = [], pulses = [], heroVisible = true, col = {};
  var G = 28;
  function readColours() {
    var cs = getComputedStyle(root);
    col.line = cs.getPropertyValue('--line').trim() || 'rgba(255,255,255,.1)';
    col.a = cs.getPropertyValue('--accent').trim() || '#35d0c0';
    col.b = cs.getPropertyValue('--accent-2').trim() || '#5b9dff';
  }
  function rnd(a, b) { return a + Math.random() * (b - a); }
  function makeRoute() {
    var x = Math.round(rnd(0, W) / G) * G, y = Math.round(rnd(0, H) / G) * G, horiz = Math.random() < .5;
    var pts = [[x, y]], n = 3 + Math.floor(Math.random() * 3);
    for (var i = 0; i < n; i++) {
      var len = G * Math.round(rnd(3, 9)) * (Math.random() < .5 ? -1 : 1);
      if (horiz) x += len; else y += len;
      pts.push([x, y]); horiz = !horiz;
    }
    var out = [pts[0]], c = G * .6;   // chamfer the corners at 45 degrees, as on a real board
    for (var k = 1; k < pts.length - 1; k++) {
      var p0 = pts[k - 1], p1 = pts[k], p2 = pts[k + 1];
      var d1 = Math.hypot(p1[0] - p0[0], p1[1] - p0[1]), d2 = Math.hypot(p2[0] - p1[0], p2[1] - p1[1]);
      var cc = Math.min(c, d1 / 2, d2 / 2);
      out.push([p1[0] - (p1[0] - p0[0]) / d1 * cc, p1[1] - (p1[1] - p0[1]) / d1 * cc]);
      out.push([p1[0] + (p2[0] - p1[0]) / d2 * cc, p1[1] + (p2[1] - p1[1]) / d2 * cc]);
    }
    out.push(pts[pts.length - 1]);
    var cum = [0];
    for (var j = 1; j < out.length; j++) cum.push(cum[j - 1] + Math.hypot(out[j][0] - out[j - 1][0], out[j][1] - out[j - 1][1]));
    return { pts: out, cum: cum, total: cum[cum.length - 1] };
  }
  function at(r, s) {
    var i = 1; while (i < r.cum.length - 1 && r.cum[i] < s) i++;
    var t = (s - r.cum[i - 1]) / ((r.cum[i] - r.cum[i - 1]) || 1);
    return [r.pts[i - 1][0] + (r.pts[i][0] - r.pts[i - 1][0]) * t, r.pts[i - 1][1] + (r.pts[i][1] - r.pts[i - 1][1]) * t];
  }
  function layout() {
    var r = cv.getBoundingClientRect(); W = r.width; H = r.height;
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    var count = Math.max(8, Math.min(26, Math.round(W * H / 45000)));
    routes = []; pulses = [];
    for (var i = 0; i < count; i++) routes.push(makeRoute());
    routes.forEach(function (rt, i) { if (i % 2 === 0) pulses.push({ r: rt, s: Math.random() * rt.total, v: rnd(60, 130) }); });
    readColours(); draw(0);
  }
  function path(rt) { ctx.beginPath(); ctx.moveTo(rt.pts[0][0], rt.pts[0][1]); for (var i = 1; i < rt.pts.length; i++) ctx.lineTo(rt.pts[i][0], rt.pts[i][1]); }
  function draw(dt) {
    ctx.clearRect(0, 0, W, H);
    ctx.lineWidth = 2; ctx.lineJoin = 'round'; ctx.strokeStyle = col.line;
    routes.forEach(function (rt) {
      path(rt); ctx.stroke();
      [rt.pts[0], rt.pts[rt.pts.length - 1]].forEach(function (p) { ctx.beginPath(); ctx.arc(p[0], p[1], 4, 0, 6.2832); ctx.stroke(); });
    });
    pulses.forEach(function (p) {
      p.s += p.v * dt; if (p.s > p.r.total) p.s = 0;
      for (var k = 0; k < 14; k++) {
        var s = p.s - k * 6; if (s < 0) break;
        var pt = at(p.r, s);
        ctx.globalAlpha = (1 - k / 14) * .9;
        ctx.fillStyle = k % 2 ? col.b : col.a;
        ctx.beginPath(); ctx.arc(pt[0], pt[1], 3.2 - k * .15, 0, 6.2832); ctx.fill();
      }
      ctx.globalAlpha = 1;
    });
  }
  if (cv && cv.getContext) {
    ctx = cv.getContext('2d');
    var rt;
    window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(layout, 200); });
    window.addEventListener('themechange', function () { readColours(); if (reduced) draw(0); });
    layout();
    if (hasIO) new IntersectionObserver(function (e) { heroVisible = e[0].isIntersecting; }).observe($('#hero'));
  }

  /* ---------- one animation loop for the traces and the marquee ---------- */
  if (!reduced) {
    var last = performance.now(), smoothV = 0;
    (function loop(t) {
      var dt = Math.min((t - last) / 1000, .05); last = t;
      if (!doc.hidden) {
        if (ctx && heroVisible) draw(dt);
        if (track && mVisible) {
          smoothV += (velocity - smoothV) * 0.1; velocity *= 0.9;
          mPos -= (40 + Math.min(Math.abs(smoothV) * 18, 900)) * dt;
          var half = track.scrollWidth / 2;
          if (half > 0 && -mPos >= half) mPos += half;
          track.style.transform = 'translate3d(' + mPos.toFixed(1) + 'px,0,0)';
        }
      }
      requestAnimationFrame(loop);
    })(last);
  }
})();
