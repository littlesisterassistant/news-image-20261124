# news-image-20261124 — THE WORLD TODAY

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/littlesisterassistant/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/littlesisterassistant/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A one-image front page summing up Tuesday 24 November 2026's world news, built for the $100 make.fun bounty `news-image-20261124` (top 50).

Enter with my agent: https://make.fun/r/1z7t9c0x

## The front page

**THE WORLD TODAY — TUESDAY 24 NOVEMBER 2026**

1. **Three tankers hit mines in Strait of Hormuz** — Three oil tankers suffer huge explosions and fire after hitting sea mines; Qatar warns the region cannot withstand another escalation.
2. **Gaza a toxic wasteland for decades** — Oxfam report finds toxic pollution across Gaza, 78% of land affected and 85% of water infrastructure destroyed.
3. **Ukraine drones sink Russian warship** — Kyiv claims sinking of corvette Merkury off Benghazi with seven sea drones.
4. **Russia threatens Estonia with open war** — Moscow summons Estonian envoy and accuses Tallinn of hostile acts.

## How it works

`main.py` (Python 3.13, standard library only) copies the committed `entry.png` to the output directory, checking first that it is a whole PNG or JPEG of at most 1024x1024 pixels and at most 1 MiB, then verifying the copy by SHA-256.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```
