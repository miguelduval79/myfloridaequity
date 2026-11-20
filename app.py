#!/usr/bin/env python3
"""Unified Florida Home Equity site (Flask).

ONE Flask application serving the four landing pages that previously ran as
separate apps on ports 8090 / 8092 / 8093 / 8094:

    /                    main equity-comparison hub   (was port 8090)
    /cash-out-refinance  Cash-Out Refinance guide      (was port 8094)
    /heloc               HELOC guide                   (was port 8093)
    /home-equity-loan    Home Equity guide             (was port 8092)
    /healthz             health endpoint

Page content, templates, CSS, JS, images and SVG diagrams are preserved from the
source applications (landing_pages/main_equity_comparison and
landing_pages/cash_out_refi_vs_heloc/*). The approved reusable equity-first modal
and the CalcMyEquity source attribution are preserved exactly.

CalcMyEquity remains a separate, external application (https://calcmyequity.com).
This site only LINKS to it, carrying the existing ?source= attribution. No
CalcMyEquity code is copied or included here.

Not deployed. Run locally:  python3 app.py            (PORT env, default 8090)
Run in prod:  gunicorn -w 2 -b 0.0.0.0:$PORT app:app
"""
import os

from flask import Flask, render_template

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
# Absolute public base URL for canonical / OG tags. MUST be set on the host
# (e.g. https://<service>.onrender.com or the final custom domain). Left empty
# locally so nothing is ever tied to a dev IP address or port.
PUBLIC_BASE_URL = os.environ.get("PUBLIC_BASE_URL", "").rstrip("/")

# Preview should not be indexed; set META_ROBOTS="index, follow" once live.
META_ROBOTS = os.environ.get("META_ROBOTS", "noindex, nofollow")
SITE_NAME = "Florida Home Equity Guide"

# CalcMyEquity stays external. We only link to it, with source attribution.
CALCMYEQUITY_URL = os.environ.get("CALCMYEQUITY_URL", "https://calcmyequity.com").rstrip("/")
LANDING_PAGE_ID = "heloc_vs_home_equity"

# ---------------------------------------------------------------------------
# Destinations (single source of truth for every template)
# ---------------------------------------------------------------------------
# The four approved conversion CTAs all open the in-page equity-first modal whose
# single button links to CalcMyEquity. Attribution identifiers are preserved
# exactly from the approved implementation.
DESTINATIONS = {
    # Approved equity-first modal CTAs -> CalcMyEquity (external).
    "compare": f"{CALCMYEQUITY_URL}/?source={LANDING_PAGE_ID}--compare_my_options",
    "get_started": f"{CALCMYEQUITY_URL}/?source={LANDING_PAGE_ID}--get_started",
    "cash_out_refi_calculator": f"{CALCMYEQUITY_URL}/?source={LANDING_PAGE_ID}--cash_out_calculator",
    "heloc_payment_calculator": f"{CALCMYEQUITY_URL}/?source={LANDING_PAGE_ID}--heloc_payment_calculator",
    # External home-equity calculator (the educational pages funnel here).
    "home_equity_calculator": f"{CALCMYEQUITY_URL}/",
    # Internal unified pages.
    "cash_out_refinance": "/cash-out-refinance",
    "heloc": "/heloc",
    "home_equity_loan": "/home-equity-loan",
    # Preserved "coming soon" placeholder destinations (no calculator is built).
    "cash_out_refinance_calculator": "/cash-out-refinance-calculator",
    "heloc_vs_home_equity_loan": "/heloc-vs-home-equity-loan",
}

PLACEHOLDERS = {
    "cash-out-refinance-calculator": (
        "cash_out/placeholder.html",
        "Cash-Out Refinance Calculator",
        "A calculator for cash-out refinance scenarios.",
    ),
    "heloc-vs-home-equity-loan": (
        "heloc/placeholder.html",
        "HELOC vs Home Equity Loan",
        "A focused comparison of a HELOC and a home equity loan.",
    ),
}

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 3600


@app.context_processor
def inject_globals():
    return {"dest": DESTINATIONS, "site_name": SITE_NAME, "robots": META_ROBOTS}


def _canonical(path):
    return f"{PUBLIC_BASE_URL}{path}"


# ---------------------------------------------------------------------------
# The four unified pages (content preserved verbatim from the source apps)
# ---------------------------------------------------------------------------
@app.route("/")
def main_page():
    # Main equity-comparison hub. Contains the approved equity-first modal.
    return render_template(
        "main/index.html",
        canonical=_canonical("/"),
        page_title="Unlock Your Home Equity | Compare Cash-Out Refinance, HELOC & Home Equity Loan (Florida)",
        meta_description=("Compare cash-out refinance, HELOC and home equity loan options for Florida "
                          "homeowners. Plain-language explanations, calculators and a guided comparison — "
                          "no guesswork, nothing to sign up for."),
    )


@app.route("/cash-out-refinance")
def cash_out_refinance_page():
    return render_template(
        "cash_out/index.html",
        canonical=_canonical("/cash-out-refinance"),
        page_title=("Cash-Out Refinance: How It Works | HELOC vs Cash-Out, Debt Consolidation "
                    "& Rates Today"),
        meta_description=("Understand cash-out refinancing: what it is, how it works, how it depends on "
                          "your home equity, using proceeds for debt consolidation, how a cash out refi "
                          "compares with a HELOC, and why everything starts with your home equity."),
    )


@app.route("/heloc")
def heloc_page():
    return render_template(
        "heloc/index.html",
        canonical=_canonical("/heloc"),
        page_title=("How Does a HELOC Work? | Draw Period, Interest-Only Payments, "
                    "Payment After Draw Period & Requirements"),
        meta_description=("Learn how a HELOC works: what a Home Equity Line of Credit is, the HELOC "
                          "draw period, interest-only payments, the repayment period and what happens "
                          "to a HELOC payment after the draw period. Everything starts with understanding "
                          "your home equity."),
    )


@app.route("/home-equity-loan")
def home_equity_loan_page():
    return render_template(
        "home_equity/index.html",
        canonical=_canonical("/home-equity-loan"),
        page_title=("Understand Your Home Equity | How a HELOC Works, Draw Period, "
                    "Interest-Only Payments & Payment After the Draw Period"),
        meta_description=("Understand your home equity and how a HELOC works: the draw period, "
                          "interest-only payments, what happens to your HELOC payment after the draw "
                          "period, and how a HELOC payment calculator helps. Start with your own "
                          "estimated equity."),
    )


@app.route("/healthz")
def healthz():
    return {"status": "ok", "app": "unified_equity_site"}, 200


# ---------------------------------------------------------------------------
# Preserved "coming soon" placeholders (referenced by the educational pages'
# internal links). No calculators are built here.
# ---------------------------------------------------------------------------
def _make_placeholder(slug):
    template, title, blurb = PLACEHOLDERS[slug]

    def view():
        return render_template(
            template,
            canonical=_canonical(f"/{slug}"),
            page_title=f"{title} | {SITE_NAME}",
            meta_description=blurb,
            heading=title,
            blurb=blurb,
        ), 200

    view.__name__ = f"placeholder_{slug.replace('-', '_')}"
    return view


for _slug in PLACEHOLDERS:
    app.add_url_rule(f"/{_slug}", view_func=_make_placeholder(_slug))


@app.errorhandler(404)
def not_found(_e):
    return render_template(
        "main/placeholder.html",
        canonical=_canonical("/"),
        page_title=f"Page not found | {SITE_NAME}",
        meta_description="Page not found.",
        heading="Page not found",
        blurb="That page does not exist yet. Head back to the home equity overview.",
        is_404=True,
    ), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8090")), debug=False)
