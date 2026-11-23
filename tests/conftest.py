"""Shared fixtures. By default the site is served locally from the repo root;
pass --base-url https://ismail-h01.github.io to run the browser tests against the live site."""
import functools
import http.server
import os
import threading

import pytest
from playwright.sync_api import sync_playwright

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHROME = "/usr/bin/google-chrome"


def pytest_addoption(parser):
    parser.addoption("--base-url", default=None, help="Test this URL instead of a local server")


class _Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


@pytest.fixture(scope="session")
def base_url(request):
    given = request.config.getoption("--base-url")
    if given:
        yield given.rstrip("/") + "/"
        return
    handler = functools.partial(_Quiet, directory=ROOT)
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{srv.server_address[1]}/"
    srv.shutdown()


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        kw = {"headless": True, "args": ["--no-sandbox"]}
        if os.path.exists(CHROME):
            kw["executable_path"] = CHROME
        b = p.chromium.launch(**kw)
        yield b
        b.close()


@pytest.fixture()
def page(browser, base_url):
    ctx = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
    pg = ctx.new_page()
    pg.errors = []
    pg.on("pageerror", lambda e: pg.errors.append(str(e)))
    pg.on("console", lambda m: pg.errors.append(m.text) if m.type == "error" else None)
    pg.goto(base_url, wait_until="load")
    yield pg
    ctx.close()


@pytest.fixture()
def mobile(browser, base_url):
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True, reduced_motion="reduce")
    pg = ctx.new_page()
    pg.errors = []
    pg.on("pageerror", lambda e: pg.errors.append(str(e)))
    pg.goto(base_url, wait_until="load")
    yield pg
    ctx.close()
