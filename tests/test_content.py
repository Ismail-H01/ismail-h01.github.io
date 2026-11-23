"""Static checks on the source files: facts that must be present, things that must never appear, and file integrity."""
import json
import os
import re

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HTML = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
TEXT = re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<(script|style).*?</\1>", "", HTML))
TEXT = re.sub(r"\s+", " ", TEXT)

MUST_HAVE = [
    "First Class", "BEng (Hons)", "MIET", "Aston University",
    "School Rep", "Engineering and Physical Sciences", "Student Rep", "Electrical and Electronic Engineering",
    "GEEP", "Royal Academy of Engineering", "STEM Ambassador", "Early Careers Network Challenge",
    "Amey Consulting", "Renishaw", "MACCS+", "EE3PEC", "92", "83 passed",
    "5.02 V", "12 kV", "2nd of 8",
]
SECTIONS = ["about", "work", "approach", "experience", "skills", "leadership", "contact"]
# Confidential or unverified material that must not reach the public page.
FORBIDDEN = ["confidential", "password", "TODO", "lorem", "ipsum", "undefined", "NaN"]


@pytest.mark.parametrize("needle", MUST_HAVE)
def test_required_fact_present(needle):
    assert needle in TEXT, f"missing: {needle}"


@pytest.mark.parametrize("needle", FORBIDDEN)
def test_forbidden_absent(needle):
    if needle == "confidential":
        # allowed only in the single explanatory note about keeping details general
        assert TEXT.lower().count("confidential") <= 1
    else:
        assert needle.lower() not in TEXT.lower()


def test_no_em_dashes_or_placeholders():
    assert "—" not in HTML and "–" not in HTML
    assert "href=\"#\"" not in HTML


@pytest.mark.parametrize("sid", SECTIONS)
def test_section_exists_and_in_nav_or_flow(sid):
    assert f'id="{sid}"' in HTML


def test_section_order_is_a_story():
    order = [HTML.index(f'id="{s}"') for s in ["about", "work", "approach", "experience", "skills", "leadership", "contact"]]
    assert order == sorted(order)
    assert HTML.index('id="hero"') < order[0]


def test_local_references_exist():
    refs = re.findall(r'(?:src|href)="((?!https?:|mailto:|#|data:)[^"]+)"', HTML)
    refs += re.findall(r'data-full="([^"]+)"', HTML)
    assert refs
    for r in set(refs):
        assert os.path.exists(os.path.join(ROOT, r.split("#")[0])), f"missing file: {r}"


def test_ids_unique_and_anchors_resolve():
    ids = re.findall(r'\sid="([^"]+)"', HTML)
    assert len(ids) == len(set(ids)), [i for i in ids if ids.count(i) > 1]
    for a in re.findall(r'href="#([^"]+)"', HTML):
        assert a in ids, f"dead anchor #{a}"


def test_aria_controls_targets_exist():
    ids = set(re.findall(r'\sid="([^"]+)"', HTML))
    for c in re.findall(r'aria-controls="([^"]+)"', HTML):
        assert c in ids


def test_every_image_has_alt_and_size():
    for tag in re.findall(r"<img\b[^>]*>", HTML):
        if 'id="lbImg"' in tag:
            continue
        assert "alt=" in tag and "width=" in tag and "height=" in tag, tag


def test_skill_keys_all_have_a_source():
    keys = set(re.findall(r'data-skill="([^"]+)"', HTML))
    used = set()
    for m in re.findall(r'data-skills="([^"]+)"', HTML):
        used.update(m.split())
    assert keys - used == set(), f"skills with no project: {keys - used}"
    assert used - keys == set(), f"project tags with no skill chip: {used - keys}"


def test_email_not_in_source_in_plain_text():
    # assembled by JS to reduce scraping; CV PDF and mailto at runtime carry it
    assert "ismail.h2589@gmail.com" not in HTML


def test_json_ld_valid():
    blob = re.search(r'<script type="application/ld\+json">(.*?)</script>', HTML, re.S).group(1)
    d = json.loads(blob)
    assert d["@type"] == "Person" and d["name"] == "Ismail Hussain"
    assert d["sameAs"] == ["https://www.linkedin.com/in/ismail-hussain22/"]


def test_meta_and_seo_files():
    for needle in ['rel="canonical"', 'property="og:image"', 'name="twitter:card"', 'name="description"', 'lang="en-GB"']:
        assert needle in HTML
    assert "Sitemap: https://ismail-h01.github.io/sitemap.xml" in open(os.path.join(ROOT, "robots.txt")).read()
    assert os.path.exists(os.path.join(ROOT, ".nojekyll"))
    assert os.path.exists(os.path.join(ROOT, "404.html"))
    from PIL import Image
    assert Image.open(os.path.join(ROOT, "assets/img/og-image.png")).size == (1200, 630)


def test_cv_pdf_one_page_and_has_key_facts():
    from pypdf import PdfReader
    r = PdfReader(os.path.join(ROOT, "assets/docs/Ismail-Hussain-CV.pdf"))
    assert len(r.pages) == 1
    t = r.pages[0].extract_text()
    for n in ["Ismail Hussain", "First Class", "MIET", "GEEP", "School Rep", "Student Rep", "Renishaw", "Amey"]:
        assert n in t, n


def test_paper_pdf_present():
    from pypdf import PdfReader
    assert len(PdfReader(os.path.join(ROOT, "assets/docs/EE3PEC-Ismail-Hussain.pdf")).pages) >= 10
