# My Florida Equity — website

Flask site for **myfloridaequity.com**: a Florida home-equity guide with four
landing pages that share one application and one design system. Built to be
deployed on Render as a Python web service.

## Pages

| Route | Page |
|---|---|
| `/` | Main equity comparison hub |
| `/cash-out-refinance` | Cash-out refinance guide |
| `/heloc` | HELOC guide |
| `/home-equity-loan` | Home equity loan guide |
| `/healthz` | Health check (returns `ok`) |

Every page links out to **CalcMyEquity** (calcmyequity.com) with the existing
`?source=` attribution. No CalcMyEquity code lives in this repo — it stays a
separate application.

## Run locally

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
PORT=8090 python3 app.py          # http://127.0.0.1:8090
```

Production-style run:

```bash
gunicorn -w 2 -t 60 -b 0.0.0.0:$PORT app:app
```

## Environment variables

| Variable | Purpose | Local | Production |
|---|---|---|---|
| `PORT` | Bind port for gunicorn | any | set by Render |
| `PUBLIC_BASE_URL` | Absolute base URL used for canonical and Open Graph tags | leave empty | `https://myfloridaequity.com` |
| `META_ROBOTS` | Robots meta tag for every page | `noindex, nofollow` (default) | `index, follow` once live |

`PUBLIC_BASE_URL` must be set in production — with it empty the canonical tags
fall back to relative paths.

## Deploy on Render

`render.yaml` in the repo root defines the service, so Render can create it as a
Blueprint:

- **Type:** Web Service (Python)
- **Build:** `pip install -r requirements.txt`
- **Start:** `gunicorn app:app --workers 2 --timeout 60 --bind 0.0.0.0:$PORT`
- **Health check:** `/healthz`

Then set the env vars above in the Render dashboard and add the custom domain.

### DNS at the registrar

For an apex domain on Render, either delegate DNS to Render or point the apex at
their address and `www` at the service:

```
A      @      216.24.57.1
CNAME  www    <service-name>.onrender.com
```

Render issues and renews the TLS certificate automatically once the DNS resolves.

## Repo layout

```
app.py                  Flask app (routes, page config, canonical/OG handling)
templates/<section>/    Jinja templates per landing page
static/<section>/       CSS, JS, images and SVG diagrams per landing page
requirements.txt        Flask + gunicorn
render.yaml             Render blueprint
docs/                   Build reports and design screenshots
```

## Docs

- `docs/REPORT-unified-equity-site.md` — how the four pages were merged into one app
- `docs/REPORT-calcmyequity-stage1.md` — CalcMyEquity visual redesign (stage 1)
- `docs/REPORT-heloc-vs-home-equity-cta.md` — HELOC vs home equity CTA work
- `docs/screenshots/` — desktop and mobile captures of each page

## Notes

- The site ships with `META_ROBOTS=noindex, nofollow` by default so a preview
  can never be indexed by accident. Flip it to `index, follow` at launch.
- Content is educational: no rate quotes, no application, no personal data
  collected. Lead capture happens on CalcMyEquity after the outbound click.
