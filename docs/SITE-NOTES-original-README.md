# Unified Equity Site

ONE Flask application serving the four Florida home-equity landing pages that
previously ran as separate apps on ports 8090 / 8092 / 8093 / 8094.

## Routes

| Route | Page | Source app |
|---|---|---|
| `/` | Main equity-comparison hub (with the approved equity-first modal) | main_equity_comparison |
| `/cash-out-refinance` | Cash-Out Refinance guide | cash_out_refi_vs_heloc/Cash-Out Refinance |
| `/heloc` | HELOC guide | cash_out_refi_vs_heloc/cash_out_refi_calculator/HELOC |
| `/home-equity-loan` | Home Equity guide | cash_out_refi_vs_heloc/cash_out_refi_calculator |
| `/healthz` | health check | — |

Preserved "coming soon" placeholders referenced by internal links:
`/cash-out-refinance-calculator`, `/heloc-vs-home-equity-loan`.

## Architecture

- One Flask app; templates namespaced under `templates/<section>/`.
- Static assets namespaced under `static/<section>/{css,js,images}/` (no collisions).
- Every page keeps its original content, CSS, JS, images, SVG diagrams, copy,
  disclosures, titles, meta descriptions and responsive behavior.
- The approved reusable equity-first modal and CalcMyEquity `?source=`
  attribution are preserved exactly.
- CalcMyEquity is external (https://calcmyequity.com); no CalcMyEquity code here.

## Configuration (env vars)

- `PUBLIC_BASE_URL` — absolute base URL for canonical/OG tags. Set on Render
  (e.g. `https://<service>.onrender.com` or the final domain). Empty locally.
- `META_ROBOTS` — default `noindex, nofollow`; set `index, follow` when live.
- `CALCMYEQUITY_URL` — default `https://calcmyequity.com`.
- `PORT` — provided by Render.

## Run

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
PORT=8096 .venv/bin/python app.py          # dev
# production:
gunicorn -w 2 -b 0.0.0.0:$PORT app:app
```

## Status

Prepared for deployment. NOT deployed yet (no Render/GitHub/DNS configuration).
