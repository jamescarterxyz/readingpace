# ReadingPace 📖

**Finish the book on time.**

A book with no plan becomes a bookmark that never moves. ReadingPace
turns "I want to finish this by the 30th" into a concrete daily plan:
how many pages a day, a day-by-day table of what to read and which
page to reach, and progress tracking as you go.

## Try it

Open `index.html` — one file, no build step, no install. (GitHub
Pages demo link goes here once published.)

## What it does

- **Daily pace** — total pages, pages already read, finish date in;
  pages-per-day out (rounded up, so the last day never overflows).
- **Day-by-day plan** — a table for every remaining day: date, pages
  that day, and the page you should reach. Extra pages spread over the
  first days, so the plan always lands exactly on the total.
- **Log progress** — add pages read; the pace recomputes instantly.
- **Multiple books** — each with its own progress bar and plan, saved
  in your browser; delete when done.
- **Finished state** — a book at 100% gets a 🎉 banner instead of a
  pace.

## Privacy

No account, no server, no tracking. Everything lives in your browser's
localStorage and works offline.

## Honest limits (v1)

- Books live in one browser — no sync between devices yet.
- Days are counted inclusively (today through the finish date).
- Clearing browser data deletes your books — there is no export yet
  (planned: JSON export like ScoreKeeper's).

## Test it

```bash
python3 tests/test_readingpace.py
```

Headless Chromium drives the real page: a 300-page book over 11 days
(28/day), logging 45 pages (pace recomputes to 24/day), reload
persistence, rejection of impossible input, and delete.

## License

MIT — free for everyone, forever.
