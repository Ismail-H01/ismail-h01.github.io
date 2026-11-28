"""Sales edition (sales/index.html): content, privacy guards, behaviour and accessibility."""
import html
import os
import re

import pytest
from axe_playwright_python.sync_playwright import Axe

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = open(os.path.join(ROOT, "sales", "index.html"), encoding="utf-8").read()
TEXT = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<(script|style).*?</\1>", "", SRC))))

MUST = [
    "First Class", "MIET", "Amey Consulting", "Renishaw", "Graduate Electrical Engineer",
    "sales and account management", "RESOLUTE", "ATOM and TONiC", "Advanced Diagnostic Tool",
    "negotiated a budget extension", "business case", "2nd of 8", "Team lead", "GEEP",
    "School Representative", "STEM Ambassador", "Open to relocation", "Best-One",
]
# Patterns for internal or personal details that must never reach a public page. Written as general
# patterns so this public file does not itself repeat the details it guards against.
NEVER = [
    r"\bconfidential\b",                 # document classification labels
    r"\b\d+\s+test\s+jigs?\b",          # production equipment counts
    r"\b(best|biggest)[- ]selling\b",     # internal sales rankings
    r"\b07\d{3}\s?\d{3}\s?\d{3}\b",     # UK mobile numbers
]


@pytest.mark.parametrize("needle", MUST)
def test_sales_fact_present(needle):
    assert needle in TEXT, needle


@pytest.mark.parametrize("pattern", NEVER)
def test_internal_detail_absent(pattern):
    assert not re.search(pattern, TEXT, re.I)


def test_unlisted_and_separate():
    assert 'name="robots" content="noindex, nofollow"' in SRC
    assert "/sales" not in open(os.path.join(ROOT, "sitemap.xml")).read()
    main = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    assert "sales/" not in main, "the engineering page must not link to the sales page"
    assert 'href="../"' in SRC                    # sales page does link back to the engineering work


def test_local_refs_and_anchors():
    for r in set(re.findall(r'(?:src|href)="((?!https?:|mailto:|#|data:)[^"]+)"', SRC)):
        path = os.path.normpath(os.path.join(ROOT, "sales", r.split("#")[0]))
        assert os.path.exists(path if not r.endswith("/") else os.path.join(path, "index.html")), r
    ids = re.findall(r'\sid="([^"]+)"', SRC)
    assert len(ids) == len(set(ids))
    for a in re.findall(r'href="#([^"]+)"', SRC):
        assert a in ids, a


def test_sales_cv_pdf():
    from pypdf import PdfReader
    r = PdfReader(os.path.join(ROOT, "assets/docs/Ismail-Hussain-CV-Sales.pdf"))
    assert len(r.pages) == 1
    t = re.sub(r"\s+", " ", r.pages[0].extract_text())
    for n in ["Ismail Hussain", "First Class", "MIET", "budget extension", "RESOLUTE", "Team Lead"]:
        assert n in t, n
    for pat in NEVER:
        assert not re.search(pat, t, re.I), pat


@pytest.fixture()
def sales(browser, base_url):
    ctx = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce", color_scheme="light")
    pg = ctx.new_page(); pg.errors = []
    pg.on("pageerror", lambda e: pg.errors.append(str(e)))
    pg.on("console", lambda m: pg.errors.append(m.text) if m.type == "error" else None)
    pg.goto(base_url + "sales/", wait_until="load")
    yield pg
    ctx.close()


def test_sales_loads_dark_and_clean(sales):
    assert sales.title().startswith("Ismail Hussain")
    assert sales.evaluate("document.documentElement.dataset.theme") == "dark"
    assert sales.errors == [], sales.errors
    assert sales.get_attribute("#hero-title", "aria-label") == "Ismail Hussain"
    accent = sales.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--accent').trim()")
    assert accent == "#f4b740"                       # warm sales palette, not the engineering teal


def test_sales_links_and_cv(sales, base_url):
    assert sales.inner_text("#mailtext") == "ismail.h2589@gmail.com"
    assert sales.request.get(base_url + "assets/docs/Ismail-Hussain-CV-Sales.pdf").status == 200
    assert sales.request.get(base_url + "assets/img/og-sales.png").status == 200
    sales.click('.depth a[href="../"]')
    sales.wait_for_load_state()
    assert sales.url.rstrip("/").endswith(base_url.rstrip("/").split("//")[1]) or sales.url == base_url


@pytest.mark.parametrize("vp", [(1440, 900), (390, 844)])
def test_sales_no_overflow(browser, base_url, vp):
    ctx = browser.new_context(viewport={"width": vp[0], "height": vp[1]})
    p = ctx.new_page(); p.goto(base_url + "sales/")
    h = p.evaluate("document.documentElement.scrollHeight")
    for y in range(0, h, 600):
        p.evaluate(f"scrollTo(0,{y})"); p.wait_for_timeout(40)
        assert p.evaluate("document.documentElement.scrollWidth <= innerWidth + 1"), y
    p.wait_for_timeout(1200)
    assert p.locator(".reveal:not(.in), .split:not(.in)").count() == 0
    ctx.close()


@pytest.mark.parametrize("theme", ["dark", "light"])
def test_sales_axe(sales, theme):
    sales.evaluate(f"document.documentElement.setAttribute('data-theme','{theme}')")
    sales.wait_for_timeout(500)                     # let the theme transition settle
    res = Axe().run(sales, options={"runOnly": {"type": "tag", "values": ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "best-practice"]}})
    msgs = [f"{v['id']}: {[n['target'] for n in v['nodes']][:3]}" for v in res.response["violations"]]
    assert msgs == [], "\n".join(msgs)
