/* Home Equity / HELOC educational page — minimal progressive enhancement. */
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
})();
