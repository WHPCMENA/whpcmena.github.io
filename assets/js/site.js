/* WHPC MENA — site behaviour
   1. Mobile menu   2. Copy buttons   3. Email-based forms   4. Google Analytics (with consent)

   ------------------------------------------------------------------
   GOOGLE ANALYTICS SETUP
   Paste your GA4 Measurement ID below (it looks like "G-ABC123XYZ9").
   Until it is set, no analytics code loads and no cookie banner shows.
   ------------------------------------------------------------------ */
var GA_MEASUREMENT_ID = "G-XXXXXXXXXX";

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

  /* ---------- 4. Google Analytics, loaded only after consent ---------- */
  var KEY = "whpcmena-analytics-consent";
  var gaReady = /^G-[A-Z0-9]{6,}$/.test(GA_MEASUREMENT_ID) && GA_MEASUREMENT_ID !== "G-XXXXXXXXXX";
  var banner = document.getElementById("consent");

  function getChoice() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function setChoice(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }

  function loadGA() {
    if (window.__gaLoaded) return;
    window.__gaLoaded = true;
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(GA_MEASUREMENT_ID);
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag("js", new Date());
    window.gtag("config", GA_MEASUREMENT_ID);
  }
  function track(name, params) {
    if (window.gtag && window.__gaLoaded) window.gtag("event", name, params || {});
  }

  if (gaReady && banner) {
    var choice = getChoice();
    if (choice === "granted") loadGA();
    else if (choice !== "denied") banner.hidden = false;

    banner.querySelector("[data-consent='accept']").addEventListener("click", function () {
      setChoice("granted"); banner.hidden = true; loadGA();
    });
    banner.querySelector("[data-consent='decline']").addEventListener("click", function () {
      setChoice("denied"); banner.hidden = true;
    });
  }
  document.querySelectorAll("[data-open-consent]").forEach(function (b) {
    if (!gaReady) { b.hidden = true; return; }
    b.addEventListener("click", function () { if (banner) banner.hidden = false; });
  });

  // Count clicks on outbound links (e.g. LinkedIn, registration pages) once GA is on.
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a[href^='http']");
    if (a && a.hostname !== location.hostname) track("outbound_click", { link_url: a.href });
  });

  /* Footer year */
  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
