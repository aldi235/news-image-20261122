# The World Today: Sunday 22 November 2026

[![make.fun](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/aldi235/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/aldi235/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122)

A one-page newspaper front page for Sunday 22 November 2026, drawn entirely in
code. Run `main.py` and it writes `entry.png`: a 1024×1024 dark-newsroom front
page with 38 short, source-checked stories across 7 regions, a schematic world
map with numbered story markers, a markets strip and a UTC timeline of the day.

## The lead

**Iran strikes US bases in Bahrain again — the fourth attack in nine days.**
The IRGC claims Patriot radar hits at al-Riffa and Awali; Bahrain says an
industrial site burned and no one was hurt. Two tankers were hit near the
Strait of Hormuz the same night, as Tehran stages a 14-ship convoy to break
the US naval blockade. That is the story the whole page is built around.

## What is on the page

- **38 stories, 7 regions** — Middle East (6), Europe (6), North America (6),
  Asia-Pacific (7), Africa (4), Latin America (5), Climate & Tech (4). Every
  story carries its source tag and a ✓ 22 NOV date check.
- **Where it happened** — a hand-drawn schematic world map with 10 numbered
  markers: Bahrain, Hormuz, Kyiv, Kryvyi Rih, Riyadh, Shenzhen, Antalya,
  Peru, Liberia and Sudan.
- **By the numbers** — 110 missiles fired at Kyiv in one night, 120+ vessels
  attacked in Hormuz since February, the S&P 500 down 7.1% on the week, gold
  at $3,527 after its worst week since March, 14 tankers in Iran's
  blockade-run convoy.
- **Markets** — S&P 500, Nasdaq, Dow, gold, silver, Brent, WTI and the dollar
  index, week to Friday 20 November: a risk-off rout, with the S&P in
  correction and the Nasdaq down 8.7%.
- **The day in UTC** — eight timed beats from COP31's overtime talks in
  Antalya to Bahrain confirming the industrial-site fire.

## Other stories inside

Russia's biggest strike of the year on Kyiv (110 missiles, 400 drones); Russian
missiles landing in Poland near a NATO exercise; the historic Trump–Putin–Xi
trilateral in Shenzhen; Nvidia chief Jensen Huang resigning; Anthropic falling
9% a day after its record $81.3bn IPO; the World Court ruling Myanmar committed
genocide against the Rohingya; the EU–Indonesia trade deal; COP31 going into
overtime with fossil fuels left out of the draft; Bitcoin below $56,000.

## Run it

```sh
python3 main.py   # writes entry.png (1024×1024, under 1 MiB)
```

Python 3.13 with Pillow. No network access, no random numbers, no clock reads:
run it twice and the output PNG is byte-identical.

## Sources

AP · Reuters · CNN · AFP · Al Jazeera · NY Post · ISW · Topstep — every story
date-checked against reporting from 22 November 2026.

## License

MIT — see [LICENSE](LICENSE).
