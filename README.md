# RPGT Calculator — Lelong Academy (Malaysia)

An installable Progressive Web App that estimates **Real Property Gains Tax (RPGT)**
on a Malaysian property disposal, for individuals, companies and non-citizens.
Based on the Lelong Academy RPGT worksheet and the LHDN Schedule 5 rates.

**Live app:** https://rja9291.github.io/PWA_RumahLelong/

## What it does
Enter the purchase and disposal details and it computes, live:

- **Chargeable gain** = Selling price − Purchase price − Allowable expenses − Allowable improvements
- **Exemption** (individuals only) = greater of RM10,000 or 10% of the gain
- **Taxable amount** = Chargeable gain − Exemption
- **RPGT rate** by holding period and disposer category
- **RPGT payable** = Taxable amount × Rate

## Rate table (LHDN Schedule 5, RPGT Act 1976)

| Holding period | Individual (Citizen/PR) | Company | Non-Citizen |
|---|---|---|---|
| Within 3 years | 30% | 30% | 30% |
| 4th year | 20% | 20% | 30% |
| 5th year | 15% | 15% | 30% |
| 6th year onward | 0% | 10% | 10% |

## Assumptions
- A **non-citizen** is treated as an individual foreigner and receives the RM10k/10% exemption. A foreign **company** would not — pick the Company category for that.
- **Companies** do not receive the RM10k/10% individual exemption.
- No **once-in-a-lifetime private-residence** exemption, gifts, part-disposals or loss carry-forward are applied.
- Estimate only — confirm your actual liability with LHDN or a licensed tax agent.

## How it's built
- `app.html` — the single source of truth: a self-contained fragment (inline CSS + JS, fonts embedded as base64, no external requests). Also published as a claude.ai Artifact.
- `index.html` — generated from `app.html` by `.claude/build-pages.sh` (adds the PWA `<head>`, manifest link and service-worker registration). **Do not hand-edit.**
- `sw.js` — service worker (offline; network-first for navigations, cache-first for assets).
- `manifest.webmanifest`, `icon.svg`, `icon-180/192/512.png` — PWA metadata and icons (`make_icons.py` regenerates the PNGs).

### Rebuild after editing `app.html`
```bash
bash .claude/build-pages.sh
```
Bump the `CACHE` name in `sw.js` and the `v1` string in `app.html` whenever assets change so returning visitors get the update.

## Install on a phone
Open the live URL in the phone browser → **Share → Add to Home Screen** (use Safari on iPhone). It then runs full-screen and works offline.
