/* Ismail Hussain portfolio: progressive enhancement only.
   The page is fully readable without this file (see .no-js rules in css/site.css). */
(function () {
  'use strict';

  var doc = document, root = doc.documentElement;
  var $ = function (s, c) { return (c || doc).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || doc).querySelectorAll(s)); };
  var reduced = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- theme ---------- */
  var themeBtn = $('#themeBtn');
  function setThemeLabel() {
    var dark = root.getAttribute('data-theme') === 'dark';
    themeBtn.setAttribute('aria-label', dark ? 'Switch to light theme' : 'Switch to dark theme');
    var meta = $('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', dark ? '#0a1120' : '#f6f8fc');
  }
  themeBtn.addEventListener('click', function () {
    var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
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

  /* ---------- scroll: progress bar, nav border, back-to-top ---------- */
  var bar = $('#progress'), nav = $('#nav'), toTop = $('#toTop');
  var ticking = false;
  function onScroll() {
    var h = root.scrollHeight - root.clientHeight;
    bar.style.width = (h > 0 ? (root.scrollTop / h) * 100 : 0) + '%';
    nav.classList.toggle('scrolled', root.scrollTop > 8);
    toTop.hidden = root.scrollTop < 700;
    ticking = false;
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();
  toTop.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: reduced ? 'auto' : 'smooth' }); });

  /* ---------- active nav link ---------- */
  var links = $$('.links a');
  if ('IntersectionObserver' in window) {
    var secIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        links.forEach(function (a) { a.classList.toggle('active', a.getAttribute('href') === '#' + en.target.id); });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    links.forEach(function (a) { var s = $(a.getAttribute('href')); if (s) secIO.observe(s); });
  }

  /* ---------- reveal on scroll ---------- */
  var reveals = $$('.reveal');
  if ('IntersectionObserver' in window && !reduced) {
    var io = new IntersectionObserver(function (entries, o) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); o.unobserve(en.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }

  /* ---------- counters ---------- */
  var counters = $$('[data-count]');
  function runCounter(el) {
    var target = +el.getAttribute('data-count');
    if (reduced) { el.textContent = target; return; }
    var t0 = null, dur = 1200;
    function step(t) {
      if (t0 === null) t0 = t;
      var p = Math.min((t - t0) / dur, 1), eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(target * eased);
      if (p < 1) requestAnimationFrame(step); else el.textContent = target;
    }
    requestAnimationFrame(step);
  }
  if ('IntersectionObserver' in window) {
    var cio = new IntersectionObserver(function (entries, o) {
      entries.forEach(function (en) { if (en.isIntersecting) { runCounter(en.target); o.unobserve(en.target); } });
    }, { threshold: 0.6 });
    counters.forEach(function (c) { cio.observe(c); });
  }

  /* ---------- typed role words ---------- */
  var word = $('#word');
  var words = ['power electronics', 'embedded systems', 'PCB design', 'testing and validation'];
  if (word) {
    if (reduced) { word.textContent = words[0]; }
    else {
      var wi = 0, ci = 0, del = false;
      (function tick() {
        var w = words[wi];
        word.textContent = w.slice(0, ci);
        var wait = del ? 35 : 75;
        if (!del && ci === w.length) { del = true; wait = 1600; }
        else if (del && ci === 0) { del = false; wi = (wi + 1) % words.length; wait = 350; }
        else { ci += del ? -1 : 1; }
        setTimeout(tick, wait);
      })();
    }
  }

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
      }, 260);
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
    var name = btn.getAttribute('data-gallery');
    group = $$('.shot-open[data-gallery="' + name + '"]');
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
  var skillOut = $('#skillOut'), skillBtns = $$('.skill');
  var sources = $$('[data-skills]');
  function titleOf(el) { var h = $('h3', el); return h ? h.textContent.trim() : ''; }
  function flash(el) {
    el.classList.add('highlight');
    setTimeout(function () { el.classList.remove('highlight'); }, 2600);
  }
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
  var u = 'ismail.h2589', d = 'gmail.com', addr = u + '@' + d;
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
  var cv = $('#traces');
  if (cv && cv.getContext) {
    var ctx = cv.getContext('2d'), W = 0, H = 0, dpr = 1, routes = [], pulses = [], raf = 0, visible = true, col = {};
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
      /* chamfer the corners (45 degree cut), as on a real board */
      var out = [pts[0]], c = G * .6;
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
      dpr = Math.min(window.devicePixelRatio || 1, 2);
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
    var last = 0;
    function loop(t) {
      var dt = Math.min((t - last) / 1000, .05); last = t;
      if (visible && !doc.hidden) draw(dt);
      raf = requestAnimationFrame(loop);
    }
    var rt;
    window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(layout, 200); });
    window.addEventListener('themechange', function () { readColours(); if (reduced) draw(0); });
    layout();
    if (!reduced) {
      raf = requestAnimationFrame(function (t) { last = t; loop(t); });
      if ('IntersectionObserver' in window) new IntersectionObserver(function (e) { visible = e[0].isIntersecting; }).observe($('#hero'));
    }
  }
})();
