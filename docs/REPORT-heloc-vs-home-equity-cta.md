# HELOC vs Home Equity — Calculator CTA Integration — Report

Date: 2026-10-10
Instructions: /root/moreno/projects/mortgage_leads/landing_pages/heloc_vs_home_equity/instructions.md
Target app: /root/moreno/projects/mortgage_leads/landing_pages/main_equity_comparison
Preview (internal, Tailscale): http://100.117.53.56:8090/  (NOT deployed publicly)

## Files modified
- app.py — new `/equity-first` route; two old calculator routes now 302-redirect to it;
  added CALCMYEQUITY_URL / LANDING_PAGE_ID / CALC_CTA_SOURCES; DESTINATIONS updated;
  removed the two calculator entries from PLACEHOLDERS.
- templates/index.html — the two "Helpful Calculators" cards are now fully-clickable
  `<a class="card card-link">` cards pointing at the equity-first intermediary;
  CSS cache-bust bumped.
- static/css/style.css — added `a.card-link:focus-visible` outline (keyboard focus).

## Files created
- templates/equity_first.html — the equity-first intermediary page.

Backup: outputs/landing_backups/heloc-vs-home-equity-cta-2026-10-10/

## How the clickable cards were implemented
The two cards were `<article class="card">` with a small inner text link. They are now
`<a class="card card-link" href="...">`, reusing the existing `.card-link` styles
(whole card is the click/tap target). The inner link became a `<span class="text-link">`
(no nested anchors). This gives, from the existing stylesheet: pointer cursor, subtle
hover elevation (translateY(-2px)), soft shadow + border response, smooth 0.16s
transition — plus a new visible keyboard `:focus-visible` outline.

## How the intermediary experience was implemented
A new page at `/equity-first` (template `equity_first.html`) reuses the site header,
footer and design system. Content:
- H1: "First, Let's Calculate Your Home Equity"
- Lead: "Before we can provide you with your potential options, we first need to estimate
  how much equity you have in your home."
- "CalcMyEquity will help you estimate your current home equity using your estimated
  property value and current mortgage balance."
- Primary CTA button "Calculate My Equity" -> https://calcmyequity.com
- Note: "It only takes a few minutes."
The old calculator URLs (/cash-out-refi-calculator, /heloc-payment-calculator) 302-redirect
into the intermediary, so no "Coming Soon" page is shown for either card.

## How source attribution was preserved
CalcMyEquity's existing URL attribution reads a single `?source=` value. To preserve BOTH
the landing page and the originating CTA in that one value (no new tracking system, no
CalcMyEquity change), the CTA link is:
  https://calcmyequity.com/?source=heloc_vs_home_equity--cash_out_calculator
  https://calcmyequity.com/?source=heloc_vs_home_equity--heloc_payment_calculator
(each card passes ?cta=cash_out_calculator | ?cta=heloc_payment_calculator to /equity-first;
invalid/absent cta falls back to cash_out_calculator).
Attribution only; it does NOT change products, equity calc, comparisons, or the lead process.
NOTE: if you later want the landing page and CTA as two SEPARATE stored fields, CalcMyEquity
would need a one-line change (its lead payload currently stores only `source`) — say the word.

## Testing performed (local, port 8099 + internal preview)
1. Cash-Out card hover: yes (reuses a.card-link:hover).
2. HELOC card hover: yes.
3. Entire Cash-Out card clickable: yes (single anchor covers the whole card).
4. Entire HELOC card clickable: yes.
5. Mobile/touch: full card is the anchor -> large tap target; responsive layout unchanged.
6. Old "Coming Soon" no longer shown: 0 occurrences; both old URLs 302 -> intermediary.
7. Both lead into the equity-first message: yes.
8. CTA opens https://calcmyequity.com with correct ?source: yes.
9. Rest of main_equity_comparison intact: home 200, other placeholders untouched.
10. No unrelated content changed: only the two calculator cards + new intermediary + app routes.

## STOP
Only this process completed. No calculators built. CalcMyEquity not modified. Not deployed.
Awaiting review.

---

# UPDATE — Instructions 2: equity-first as an in-page MODAL (2026-10-10)

Instructions: heloc_vs_home_equity/instructions_two.md

## Change
Replaced the separate /equity-first page with ONE reusable in-page modal on the
existing page. The visitor stays on main_equity_comparison.

## Files modified
- templates/index.html — added the single modal markup (#equityModal) at end of body;
  asset cache-bust bumped to v=20261010-2.
- static/css/style.css — modal styles (centered white card, rounded, shadow, backdrop,
  close button, body scroll lock, mobile rules).
- static/js/main.js — modal open/close + trigger wiring.
- app.py — DESTINATIONS: the two calculator keys and "compare" now point at the
  CalcMyEquity URLs (with attribution); removed "equity_first"; removed /equity-first
  route; old calculator URLs now 302 -> "/"; PLACEHOLDERS: removed "compare".

## Files removed
- templates/equity_first.html (unreferenced after the change).

## How ONE modal serves all three triggers
The three CTAs are anchors whose href already points at CalcMyEquity with attribution.
main.js attaches one click handler to every `a[href*="heloc_vs_home_equity--"]`
(the two calculator cards + all Compare My Options CTAs), prevents the default
navigation, copies the trigger's href onto the modal CTA, and shows the modal.
Only one modal implementation exists. With JS disabled the anchors still navigate
straight to CalcMyEquity (progressive enhancement).

## Attribution
- Cash-Out Refinance Calculator card -> ?source=heloc_vs_home_equity--cash_out_calculator
- HELOC Payment Calculator card        -> ?source=heloc_vs_home_equity--heloc_payment_calculator
- Compare My Options                    -> ?source=heloc_vs_home_equity--compare_my_options

## Cleanup
/equity-first route + equity_first.html removed (confirmed no code references remain).
Old /cash-out-refi-calculator and /heloc-payment-calculator now 302-redirect to "/".

## Modal behavior
Centered, max-width 460px, white rounded card, soft shadow, one primary CTA
"Calculate My Equity", visible "X" close, closable via X / Esc / backdrop click,
background dimmed+blurred, body scroll locked, focus moves to the CTA and returns
on close. Mobile: reduced padding, full-width CTA, easy to tap.

## Testing (temp instance 8099 + internal preview 8090)
- All three triggers open the SAME modal; page stays put (no navigation).
- CTA href correct per trigger (attribution verified).
- Close via X, Esc, and backdrop; clicking inside the modal does NOT close it.
- No JS errors. /equity-first -> 404. Old calculator URLs -> 302 to "/".
- Unrelated placeholders (heloc-vs-home-equity, get-started) still 200.

---

# UPDATE — Instructions 3: "Get Started" joins the same modal (2026-10-10)

Instructions: heloc_vs_home_equity/instructions_three.md

## Exact change
- app.py, DESTINATIONS["get_started"]: was "/get-started" (placeholder) -> now
  https://calcmyequity.com/?source=heloc_vs_home_equity--get_started
- app.py, CALC_CTA_SOURCES: added "get_started": "Get Started" (attribution inventory).
- app.py, PLACEHOLDERS: removed the now-unused "get-started" entry.
- app.py: added a 302 redirect /get-started -> "/" for the old URL.

No other file changed. The Get Started button already renders dest.get_started, and
main.js already opens the modal for any `a[href*="heloc_vs_home_equity--"]`, so no
HTML/JS change was needed — the smallest possible change.

## Confirmation
- Existing modal reused: YES (same #equityModal; no modal/markup change).
- Existing CTA processes modified: NO (Cash-Out, HELOC, Compare My Options untouched).
- Attribution: get_started (landing page heloc_vs_home_equity preserved).

## Testing (temp 8099 + CDP)
- Get Started opens the SAME modal, stays on page, CTA href =
  ...?source=heloc_vs_home_equity--get_started, closes via X.
- Regression: Cash-Out / HELOC / Compare My Options still open the same modal with
  their original attribution. No JS errors. /get-started -> 302 -> "/".
