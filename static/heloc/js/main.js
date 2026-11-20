/* HELOC educational landing page — minimal progressive enhancement. */
(function () {
  "use strict";

  var y = document.querySelector("[data-year]");
  if (y) { y.textContent = String(new Date().getFullYear()); }

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
