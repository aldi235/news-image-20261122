# The World Today: Sunday 22 November 2026

[![news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/aldi235/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/aldi235/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122)

A single-image world news digest for Sunday 22 November 2026: 38
source-checked stories across 7 regions, each with a source tag and a
date check, plus a world map and a UTC timeline strip.

## Run

Render the image (build step, requires Python 3 with PIL — local only,
not the entrypoint):

```sh
python3 draw_news.py
```

This writes `entry.png` in the repo directory.

Copy the pre-rendered image to the output directory (the entrypoint,
Node 22 standard library only — no npm packages):

```sh
node main.ts
```

This copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`
(default `/output/entry.png`).
