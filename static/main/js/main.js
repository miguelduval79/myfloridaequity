/* Main Equity Comparison — minimal, dependency-free progressive enhancement. */
(function () {
  "use strict";

  // Keep the copyright year current without hard-coding it in the HTML.
  var y = document.querySelector("[data-year]");
  if (y) { y.textContent = String(new Date().getFullYear()); }

  // Smooth-scroll for same-page anchors (progressive; CSS also handles it).
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener("click", function (e) {
      var id = a.getAttribute("href").slice(1);
      var el = id && document.getElementById(id);
      if (!el) return;
      e.preventDefault();
      el.scrollIntoView({ behavior: "smooth", block: "start" });
      history.replaceState(null, "", "#" + id);
    });
  });

  // ---------------------------------------------------------------------
  // Equity-first modal — the ONE modal shared by all three conversion CTAs:
  //   Cash-Out Refinance Calculator, HELOC Payment Calculator, Compare My Options.
  // Every trigger is an <a> whose href already points at CalcMyEquity with the
  // right ?source= attribution, so the modal simply reuses that href. With JS
  // disabled the anchors still work (progressive enhancement).
  // ---------------------------------------------------------------------
  var equityModal = document.getElementById("equityModal");
  var equityModalCta = document.getElementById("equityModalCta");
  var lastFocused = null;

  function openEquityModal(trigger) {
    if (!equityModal) return;
    var href = trigger && trigger.getAttribute("href");
    if (href && equityModalCta) equityModalCta.setAttribute("href", href);
    lastFocused = document.activeElement;
    equityModal.hidden = false;
    document.body.classList.add("modal-open");
    if (equityModalCta) equityModalCta.focus();
  }

  function closeEquityModal() {
    if (!equityModal || equityModal.hidden) return;
    equityModal.hidden = true;
    document.body.classList.remove("modal-open");
    if (lastFocused && typeof lastFocused.focus === "function") lastFocused.focus();
  }

  // Any anchor that leads into CalcMyEquity (the two calculator cards and the
  // Compare My Options CTAs) opens the modal instead of navigating away.
  document.querySelectorAll('a[href*="heloc_vs_home_equity--"]').forEach(function (a) {
    a.addEventListener("click", function (e) {
      // Respect open-in-new-tab / modified clicks.
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
      e.preventDefault();
      openEquityModal(a);
    });
  });

  if (equityModal) {
    equityModal.addEventListener("click", function (e) {
      if (e.target === equityModal || e.target.hasAttribute("data-modal-close")) {
        closeEquityModal();
      }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" || e.keyCode === 27) closeEquityModal();
    });
  }
})();
