/* WHPC MENA — site behaviour
   1. Mobile menu   2. Copy buttons   3. Email-based forms   4. Analytics events
*/

var CONTACT_EMAIL = "marhaba@whpcmena.org";

(function () {
  "use strict";

  /* ---------- 1. Mobile menu ---------- */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("main-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.textContent = open ? "Close" : "Menu";
    });
  }

  /* ---------- 2. Copy buttons ---------- */
  document.querySelectorAll("[data-copy]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var text = btn.getAttribute("data-copy");
      var done = function () {
        var old = btn.textContent;
        btn.textContent = "Copied";
        setTimeout(function () { btn.textContent = old; }, 1600);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, function () { selectNear(btn); });
      } else {
        selectNear(btn);
      }
    });
  });
  function selectNear(btn) {
    var code = btn.parentElement && btn.parentElement.querySelector("code");
    if (!code) return;
    var range = document.createRange();
    range.selectNodeContents(code);
    var sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
  }

  /* ---------- 3. Email-based forms ----------
     These forms use no outside service. On submit they open the visitor's
     email app with a message to CONTACT_EMAIL, pre-filled from the form.
     Replace this with a form service later if you decide to use one. */
  document.querySelectorAll("form[data-mailto]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var subject = form.getAttribute("data-subject") || "Message from the website";
      var lines = [];
      var seen = {};
      Array.prototype.forEach.call(form.elements, function (el) {
        if (!el.name || seen[el.name] || el.type === "submit") return;
        var label = el.getAttribute("data-label") || el.name;
        var value;
        if (el.type === "checkbox") {
          seen[el.name] = true;
          value = Array.prototype.filter.call(form.querySelectorAll('[name="' + el.name + '"]'), function (c) { return c.checked; })
            .map(function (c) { return c.value; }).join(", ");
          label = el.closest("fieldset") ? el.closest("fieldset").getAttribute("data-label") || label : label;
        } else {
          value = el.value.trim();
        }
        if (value) lines.push(label + ": " + value);
      });
      var href = "mailto:" + CONTACT_EMAIL +
        "?subject=" + encodeURIComponent(subject) +
        "&body=" + encodeURIComponent(lines.join("\n") + "\n");
      window.location.href = href;
      var status = form.querySelector(".form-status");
      if (status) {
        status.textContent = "Your email app should now open with this message ready to send. " +
          "If nothing opened, email us directly at " + CONTACT_EMAIL + ".";
      }
      track("form_submit", { form_name: form.id || subject });
    });
  });

  /* ---------- 4. Analytics events ---------- */
  function track(name, params) {
    if (typeof window.gtag === "function") window.gtag("event", name, params || {});
  }

  // Count clicks on outbound links (e.g. LinkedIn, registration pages) once GA is on.
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a[href^='http']");
    if (a && a.hostname !== location.hostname) track("outbound_click", { link_url: a.href });
  });

  /* Footer year */
  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
