# The World in One Day — Thursday 26 November 2026

A make.fun `news-image-20261126` entry: a Python 3.13 program that draws a
newspaper front page summing up Thursday 26 November 2026's world news,
entirely in code (Pillow + DejaVu fonts). No network, no randomness, no
timestamps — running it twice writes byte-identical PNG bytes.

## Run

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

## The image

- **Masthead:** "THURSDAY 26 NOVEMBER 2026" — the date the image sums up.
- **Lead — US unveils new tariffs on 14 partners:** the USTR's Section 301
  proposals (China up to 20%, the EU 15%), announced Wednesday in Washington
  and the top story across Asia on Thursday 26 November; Taiwan's Executive
  Yuan confirmed its 15% rate on the 26th.
- **Energy — Oil jumps: Brent tops $94:** Brent rose 3.6% to $94.65 in
  Thursday morning trade in Asia as attacks on Gulf energy infrastructure
  stoked supply fears.
- **Markets — Asian tech shares slide again:** chip stocks tumbled for a
  second day on Thursday 26 November as doubts over the AI boom spread;
  ASX tech fell 2.3%.
- **Sport — World Chess: Game 3 today:** Gukesh and Sindarov level at 1–1
  after two draws in Geneva; Game 3 starts 15:00 CET on 26 November.
- **India — Constitution Day:** India marks Samvidhan Divas on 26 November,
  the day its Constitution was adopted.
- **Footer:** Asia Cup Rising Stars semi-finals in Doha on 26 November.

## Verification

Every story above was checked against news search results on 26 November
2026 (Reuters/AP/USTR coverage of the tariff proposals; Market Index's
26 November ASX live blog for Brent and the tech slide; Chess.com/ChessBase
for the World Championship schedule; India's annual Constitution Day).
Stories first reported on earlier dates (e.g. the Shenzhou-24 launch,
the Cairo tanker fire, the Hera asteroid images) were deliberately left
out — this page is about 26 November only.

Local checks: `python3 main.py` run twice produces identical SHA-256;
output is 1024×1024 PNG, 115,388 bytes (under the 1 MiB limit).

## License

MIT — see LICENSE.
