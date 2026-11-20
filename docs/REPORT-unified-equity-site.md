# Landing Pages — Production Unification — Report

Date: 2026-10-10
Instructions: /root/moreno/projects/mortgage_leads/landing_pages/instructions_unify.md

## 1. unified_equity_site created
/root/moreno/projects/mortgage_leads/landing_pages/unified_equity_site/  (NEW app)

## 2. Files created
- app.py, requirements.txt, README.md, .gitignore
- templates/main/index.html, templates/main/placeholder.html
- templates/cash_out/index.html, templates/cash_out/placeholder.html
- templates/heloc/index.html, templates/heloc/placeholder.html
- templates/home_equity/index.html
- static/main/{css/style.css,js/main.js,images/florida-home.jpg}
- static/cash_out/{css,js,images/*}   (copied from Cash-Out Refinance app)
- static/heloc/{css,js,images/*}      (copied from HELOC app)
- static/home_equity/{css,js,images/*}(copied from Home Equity app)

## 3. Source apps NOT modified
main_equity_comparison/, cash_out_refi_vs_heloc/ untouched (verified: no writes; they remain
running on 8090/8092/8093/8094). heloc_vs_home_equity/ is instructions-only and untouched.

## 4. Final route map
/ -> main_page
/cash-out-refinance -> cash_out_refinance_page
/heloc -> heloc_page
/home-equity-loan -> home_equity_loan_page
/healthz -> healthz
/cash-out-refinance-calculator -> placeholder (preserved)
/heloc-vs-home-equity-loan -> placeholder (preserved)
/static/<path> -> static (namespaced per section)

## 5. How the four apps were integrated
One Flask app renders four namespaced templates. Each page's content, copy, disclosures,
titles, meta descriptions, CSS, JS, images and SVG diagrams were copied verbatim; the only
edit was rewriting url_for('static', filename='X') to the section namespace 'X'.
No business logic, no calculations; the educational pages were already static.

## 6. Templates separated
templates/<section>/index.html (+ placeholder.html for 404 and "coming soon").

## 7. Static assets separated
static/<section>/{css,js,images}. Filename collisions avoided (each section has its own
style.css / main.js / images). Verified every referenced asset returns HTTP 200.

## 8. Internal links changed
- Main page product cards: port 8094/8093/8092 -> /cash-out-refinance, /heloc, /home-equity-loan.
- brand "href=/" preserved (now = main hub, as required).
- HELOC page's dest.cash_out_refinance -> /cash-out-refinance (real page now).
- Preserved placeholders: /cash-out-refinance-calculator, /heloc-vs-home-equity-loan.
- Educational pages' "https://calcmyequity.com" links preserved (external).

## 9. Four approved modal entry points
Verified via headless browser on the unified site: Cash-Out Calculator, HELOC Payment
Calculator, Compare My Options, Get Started all open the SAME reusable modal, stay on the
page, and set the correct CTA href. Close via X works.

## 10. Attribution unchanged
heloc_vs_home_equity--cash_out_calculator
heloc_vs_home_equity--heloc_payment_calculator
heloc_vs_home_equity--compare_my_options
heloc_vs_home_equity--get_started
(landing page id = heloc_vs_home_equity). Verified in rendered hrefs.

## 11. CalcMyEquity
External only. NOT copied, moved, rebuilt or modified. No CalcMyEquity code present
(grep for calc_my_equity/getLeadSource/gspread/service_account = none). Only links to
https://calcmyequity.com with the existing ?source= attribution.

## 12. Local preview URL
Running temporarily on one free port (existing apps untouched):
  http://127.0.0.1:8096/   (also reachable over Tailscale at http://100.117.53.56:8096/)
  pages: / , /cash-out-refinance , /heloc , /home-equity-loan , /healthz

## 13. Gunicorn command (for eventual Render deploy)
  gunicorn -w 2 -b 0.0.0.0:$PORT app:app

## 14. Env vars needed on Render
- PUBLIC_BASE_URL  (e.g. https://<service>.onrender.com or final domain) — for canonical/OG
- META_ROBOTS      (set "index, follow" when live; default stays noindex for preview)
- CALCMYEQUITY_URL (optional; default https://calcmyequity.com)
- PORT             (provided by Render)

## 15. Required tests
1-4 pages load (200): PASS. 5-7 cards -> internal routes: PASS. 8-11 four modal CTAs work: PASS.
12 modal close unchanged: PASS. 13 Calculate My Equity -> calcmyequity.com: PASS.
14 attribution correct: PASS. 15 CalcMyEquity not copied/modified: PASS.
16-19 images/SVG/CSS/JS load (all 200): PASS. 20-21 desktop/mobile: PASS (responsive copied).
22 no dependency on IP/ports (grep = none): PASS. 23 canonical base-relative, domain-agnostic: PASS.
24 /healthz: PASS. 25 gunicorn starts with 2 workers: PASS.

Regression: rendered pages diffed against the running source apps — only expected differences
(namespaced asset paths, required internal card links, base-relative canonicals, and one
harmless trailing-slash normalization on the Home-Equity page's CalcMyEquity links). No content,
image, diagram, styling or copy lost.

## 16. Problems discovered
- The three educational apps had inconsistent CalcMyEquity URL defaults (some with a trailing
  slash, home-equity without). Standardized to the trailing-slash form; cosmetic only.
- home_equity app had not_found.html and cash_out/heloc had placeholder.html; unified uses
  main/placeholder.html for the 404 and the section placeholders for "coming soon" routes.

## STOP
Not deployed. No GitHub push. No Render config. No DNS. CalcMyEquity untouched. Awaiting review.
