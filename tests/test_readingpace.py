"""ReadingPace self-test — headless Chromium assertions.

Run:  python3 tests/test_readingpace.py
Exit code 0 = all assertions pass.
"""

import datetime
import functools
import http.server
import threading

HERE = __import__("os").path.dirname(__import__("os").path.abspath(__file__))
ROOT = __import__("os").path.dirname(HERE)


def main():
    handler = functools.partial(http.server.SimpleHTTPRequestHandler,
                                directory=ROOT)
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    port = server.server_address[1]
    threading.Thread(target=server.serve_forever, daemon=True).start()

    from playwright.sync_api import sync_playwright

    deadline = (datetime.date.today() +
                datetime.timedelta(days=10)).isoformat()
    # Inclusive count: today .. deadline = 11 days.
    assert 300 % 11 != 0  # keeps the ceil/remainder math meaningful

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.on("dialog", lambda d: d.accept())
        page.goto("http://127.0.0.1:{}/index.html".format(port))

        page.fill("#title", "Dune")
        page.fill("#total", "300")
        page.fill("#read", "0")
        page.fill("#deadline", deadline)
        page.click("#addBtn")

        book = page.inner_text(".book")
        # 300 pages / 11 days -> 28 pages/day (ceil).
        assert "28 pages/day for 11 days" in book, book
        rows = page.query_selector_all(".book table tr")
        assert len(rows) == 12, len(rows)  # header + 11 plan rows
        first = rows[1].query_selector_all("td")
        assert first[1].inner_text() == "28", first[1].inner_text()
        assert first[2].inner_text() == "28", first[2].inner_text()

        # Log 45 pages: 255 left / 11 days -> 24 pages/day.
        page.fill("[data-log='0']", "45")
        page.click("[data-logbtn='0']")
        book = page.inner_text(".book")
        assert "45 / 300 pages" in book, book
        assert "24 pages/day for 11 days" in book, book

        # Reload: the book must persist.
        page.reload()
        assert "Dune" in page.inner_text(".book")
        assert "45 / 300 pages" in page.inner_text(".book")

        # Invalid input: pages read beyond total must be refused.
        page.fill("#title", "Bad Book")
        page.fill("#total", "100")
        page.fill("#read", "150")
        page.fill("#deadline", deadline)
        page.click("#addBtn")
        assert "Bad Book" not in page.inner_text("body"), "bad book accepted"

        # Delete the book.
        page.click("[data-del='0']")
        assert "No books yet" in page.inner_text("#books")

        browser.close()
    server.shutdown()
    print("ALL READINGPACE TESTS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
