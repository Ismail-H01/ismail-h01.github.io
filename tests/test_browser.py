"""Behaviour tests in a real browser: layout, interactions, accessibility."""
import pytest
from axe_playwright_python.sync_playwright import Axe


def test_loads_clean(page):
    assert page.title().startswith("Ismail Hussain")
    assert page.errors == [], page.errors
    assert page.locator("h1").inner_text().replace("\n", " ").strip() == "Ismail Hussain"


def test_no_horizontal_overflow_desktop_and_mobile(page, mobile):
    for p in (page, mobile):
        for t in ("dark", "light"):
            p.evaluate(f"document.documentElement.setAttribute('data-theme','{t}')")
            assert p.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1"), (p.viewport_size, t)


def test_all_content_visible_with_reduced_motion(page):
    assert page.locator(".reveal:not(.in)").count() == 0


def test_nav_links_scroll_to_sections(page):
    for sid in ["about", "work", "experience", "skills", "leadership", "contact"]:
        page.click(f'.links a[href="#{sid}"]')
        page.wait_for_timeout(150)
        top = page.evaluate(f"document.getElementById('{sid}').getBoundingClientRect().top")
        at_bottom = page.evaluate("window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 2")
        assert (-5 <= top <= 140) or at_bottom, (sid, top)


def test_theme_toggle_persists(page):
    start = page.evaluate("document.documentElement.dataset.theme")
    page.click("#themeBtn")
    now = page.evaluate("document.documentElement.dataset.theme")
    assert now != start
    page.reload()
    assert page.evaluate("document.documentElement.dataset.theme") == now


def test_dropdowns_open_close_and_label(page):
    for btn_sel, panel in (('[aria-controls="drop-maccs"]', "#drop-maccs"), ('[aria-controls="drop-pec"]', "#drop-pec")):
        b = page.locator(btn_sel)
        b.scroll_into_view_if_needed()
        assert b.get_attribute("aria-expanded") == "false"
        b.click()
        page.wait_for_timeout(700)
        assert b.get_attribute("aria-expanded") == "true"
        assert page.locator(panel).evaluate("e => e.getBoundingClientRect().height") > 100
        assert b.inner_text().startswith("Hide")
        b.click()
        page.wait_for_timeout(700)
        assert page.locator(panel).evaluate("e => e.getBoundingClientRect().height") < 5
        assert b.inner_text().startswith("View")


def test_lightbox_open_navigate_close_and_focus_return(page):
    page.click('[aria-controls="drop-pec"]')
    page.wait_for_timeout(700)
    first = page.locator('.shot-open[data-gallery="pec"]').first
    first.click()
    assert page.locator("#lb.open").count() == 1
    cap1 = page.inner_text("#lbCap")
    page.keyboard.press("ArrowRight")
    assert page.inner_text("#lbCap") != cap1
    page.keyboard.press("ArrowLeft")
    assert page.inner_text("#lbCap") == cap1
    assert page.evaluate("document.getElementById('lbImg').naturalWidth") > 100
    page.keyboard.press("Escape")
    assert page.locator("#lb.open").count() == 0
    assert page.evaluate("document.activeElement === document.querySelector('.shot-open[data-gallery=\"pec\"]')")


def test_single_image_gallery_hides_nav(page):
    page.click('[aria-controls="drop-maccs"]')
    page.wait_for_timeout(700)
    page.locator('.shot-open[data-gallery="maccs"]').click()
    assert page.locator("#lbPrev").is_hidden() and page.locator("#lbNext").is_hidden()


def test_skills_filter_links_to_projects(page):
    page.locator('.skill[data-skill="zuken"]').click()
    out = page.inner_text("#skillOut")
    assert "Zuken CR-8000" in out and "Renishaw" in out
    assert page.locator('.skill[aria-pressed="true"]').count() == 1
    page.locator('.skill[data-skill="matter"]').click()
    assert "MACCS+" in page.inner_text("#skillOut")
    assert page.locator('.skill[aria-pressed="true"]').count() == 1
    page.locator('.skill[data-skill="matter"]').click()
    assert page.locator('.skill[aria-pressed="true"]').count() == 0


def test_every_skill_chip_resolves(page):
    for k in page.eval_on_selector_all(".skill", "els => els.map(e => e.dataset.skill)"):
        page.locator(f'.skill[data-skill="{k}"]').click()
        assert "no listed project" not in page.inner_text("#skillOut"), k
        assert page.locator("#skillOut a").count() >= 1, k


def test_email_assembled_and_links_correct(page):
    hrefs = page.eval_on_selector_all("a[data-mail]", "els => els.map(e => e.getAttribute('href'))")
    assert hrefs and all(h == "mailto:ismail.h2589@gmail.com" for h in hrefs)
    assert page.inner_text("#mailtext") == "ismail.h2589@gmail.com"
    li = page.eval_on_selector_all('a[href*="linkedin.com"]', "els => els.map(e => e.href)")
    assert li and all(h == "https://www.linkedin.com/in/ismail-hussain22/" for h in li)
    ext = page.eval_on_selector_all('a[target="_blank"]', "els => els.map(e => e.rel)")
    assert all("noopener" in r for r in ext)


def test_downloads_resolve(page, base_url):
    for href in ("assets/docs/Ismail-Hussain-CV.pdf", "assets/docs/EE3PEC-Ismail-Hussain.pdf", "404.html", "robots.txt", "sitemap.xml"):
        r = page.request.get(base_url + href)
        assert r.status == 200, href
    assert page.request.get(base_url + "assets/docs/Ismail-Hussain-CV.pdf").headers["content-type"].startswith("application/pdf")


def test_counters_reach_targets(page):
    page.wait_for_timeout(200)
    page.locator(".stats").scroll_into_view_if_needed()
    page.wait_for_timeout(300)
    vals = page.eval_on_selector_all("[data-count]", "els => els.map(e => [e.dataset.count, e.textContent])")
    assert all(a == b for a, b in vals), vals


def test_images_load_and_are_not_distorted(page):
    page.click('[aria-controls="drop-maccs"]'); page.click('[aria-controls="drop-pec"]')
    page.wait_for_timeout(800)
    page.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
    page.wait_for_timeout(500)
    bad = page.evaluate("""() => [...document.images].filter(i => i.id !== 'lbImg' && (!i.complete || i.naturalWidth === 0 ||
        Math.abs(i.clientWidth / i.clientHeight - i.naturalWidth / i.naturalHeight) > 0.03)).map(i => i.src)""")
    assert bad == [], bad


def test_mobile_menu(mobile):
    assert mobile.locator("#menu").is_hidden()
    mobile.click("#menuBtn")
    assert mobile.locator("#menu").is_visible()
    mobile.click('#menu a[href="#skills"]')
    mobile.wait_for_timeout(300)
    assert mobile.locator("#menu").is_hidden()


def test_mobile_tap_targets(mobile):
    small = mobile.evaluate("""() => [...document.querySelectorAll('.btn, .icon-btn, .skill, .links a')]
        .filter(e => e.offsetParent !== null).map(e => e.getBoundingClientRect()).filter(r => r.height < 32).length""")
    assert small == 0


def test_no_js_fallback(browser, base_url):
    ctx = browser.new_context(java_script_enabled=False, viewport={"width": 1280, "height": 800})
    p = ctx.new_page(); p.goto(base_url)
    assert p.locator(".reveal").first.is_visible()
    assert p.locator("#drop-pec").evaluate("e => e.getBoundingClientRect().height") > 100
    assert "power electronics" in p.inner_text(".role-static")
    ctx.close()


def test_print_emulation_hides_chrome(page):
    page.emulate_media(media="print")
    assert page.locator(".nav").is_hidden() and page.locator("#traces").is_hidden()


@pytest.mark.parametrize("theme", ["dark", "light"])
def test_axe_wcag(page, theme):
    page.evaluate(f"document.documentElement.setAttribute('data-theme','{theme}')")
    page.click('[aria-controls="drop-maccs"]'); page.click('[aria-controls="drop-pec"]')
    page.wait_for_timeout(800)
    res = Axe().run(page, options={"runOnly": {"type": "tag", "values": ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "best-practice"]}})
    msgs = [f"{v['id']}: {v['help']} -> {[n['target'] for n in v['nodes']][:3]}" for v in res.response["violations"]]
    assert msgs == [], "\n".join(msgs)
