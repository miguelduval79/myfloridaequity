# CalcMyEquity — Stage 1 (Visual Redesign) — Report

Date: 2026-10-10
Project: /root/moreno/projects/calc_my_equity
Branch: stage-1-visual-redesign
Commit: ee5b6f2 — "Stage 1: modern financial redesign of CalcMyEquity (style.css only, no logic changes)"

## Review link
- https://equity-review.2-24-117-139.sslip.io/
- Served by a safe preview instance (stubbed backend — no real emails, no Google Sheets writes).

## Files modified (deliverable)
- Backend/static/style.css  (302 insertions, 75 deletions) — the ONLY deliverable file changed.

## Files NOT touched
- Backend/app.py
- Backend/templates/index.html
- Backend/static/app.js

No HTML IDs/classes renamed or removed. app.js contract fully preserved.

## Design
- Light professional background with subtle navy/blue radial accents.
- White rounded card (radius 26px) with soft layered shadow + slim navy→blue top accent bar.
- Navy/blue primary palette; pill eyebrow badge; strong heading hierarchy.
- Pill language toggle (EN/ES); modern inputs with focus ring; modern primary/secondary buttons.
- Progress bar restyled in navy→blue gradient.
- Result screen (#step-7) presented in a highlighted light-blue panel with a big navy equity figure and a card-style summary list.
- Fully responsive (single column on mobile, stacked buttons).
- Respects prefers-reduced-motion.

## Behaviour
- ZERO functional change. Redesign is CSS-only.
- Verified: page loads (HTTP 200), static assets 200, app.js executes (step-1 renders,
  EN strings applied), stub endpoints respond success so the full funnel is click-through-able.

## Review preview (not the deliverable)
- /root/moreno/projects/calc_my_equity_preview — copy of front-end + stubbed Flask backend.
- systemd: moreno-equity-review.service (gunicorn, 127.0.0.1:8095).
- nginx: /etc/nginx/sites-available/moreno-equity-review (HTTPS, Let's Encrypt cert, noindex).

## Next
- Stage 2 (Cash-Out vs HELOC vs Home Equity Loan comparison) NOT started — awaiting Miguel's separate instruction.

---

# CalcMyEquity — Stage 2 (Home Equity Options Comparison) — Report

Date: 2026-10-10
Branch: stage-2-comparison
Commit: c74f69d

## Review link
- https://equity-review.2-24-117-139.sslip.io/ (same preview; go through the funnel, use code 1234, then "Compare My Options")

## Files modified
- Backend/templates/index.html — added "Compare My Options" button on result screen + new #step-8 comparison markup.
- Backend/static/style.css — appended Stage 2 styles (sliders, cards, CTA, disclosure), reusing the Stage 1 system.
- Backend/static/app.js — appended centralized ASSUMPTIONS, scenario math, live update, EN/ES strings.
- Backend/app.py UNCHANGED. Existing verification/lead/Sheets flow unchanged.

## Assumptions (centralized in ASSUMPTIONS, app.js)
- Base rate: 7.50% (slider 4%–11%). Default term 30 yr (slider 10–30). Rate clamp 3%–15%.
- Cash-Out: max LTV 0.80, rate spread +0.00.
- HELOC: max CLTV 0.85, rate spread +0.50, draw 10 yr, repay 20 yr, default amount drawn 50%.
- Home Equity Loan: max CLTV 0.85, rate spread +0.75, term 15 yr.
- Credit bands: Excellent 740+ (rate -0.25, LTV +0.02) / Good 700-739 (0,0) / Fair 640-699 (+0.50, -0.03) / Lower <640 (+1.25, -0.06).

## Formulas
- Equity = property value - mortgage balance (min 0).
- Cash-Out: Max New Mortgage = value × cashOutLTV; Cash Out = Max New Mortgage − balance (min 0);
  Payment = amortized payment on the FULL new mortgage.
- HELOC: Credit Limit = value × helocCLTV − balance; Amount Drawn = limit × drawn%;
  Draw-period payment = interest-only on amount drawn.
- Home Equity Loan: Amount = value × heloanCLTV − balance; Payment = amortized on that amount (first mortgage stays separate); Total = payment × months.
- Potential Accessible Equity = max(cash-out cash, HELOC limit, home equity loan amount).
- Amortized payment: P·r / (1 − (1+r)^-n), r = APR/100/12, n = years×12.

## Testing (headless Chrome, full funnel driven)
- Stage 1 screens + funnel still work; equity $350,000 for value $600k / balance $250k.
- Defaults: accessible $260k; cash-out $230k @7.50% / $3,356/mo; HELOC limit $260k @8.00%, pay $867/mo (50% drawn); HEL $260k @8.25%, $2,522/mo, total $454,026.
- Sliders (credit 780 Excellent, rate 6.5%, term 15, drawn 100%): live update confirmed; accessible $272k; cash-out $242k @6.25% / $4,219/mo.
- Negative-equity guard: value 200k / balance 300k → equity $0, all amounts $0, no negatives.
- EN/ES toggle updates the comparison screen. CTA confirm shows. No JS console errors.

## STOP
Stage 2 complete. Did NOT deploy to Render. Not merged with mortgage_leads. Awaiting review/approval.
