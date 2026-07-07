(function () {
  var STORAGE_KEY = "arngcor_lang";

  var PL_TO_EN = {
    "/": "/en/",
    "/index.html": "/en/",
    "/o-nas.html": "/en/about.html",
    "/polityka-prywatnosci.html": "/en/privacy-policy.html",
    "/regulamin.html": "/en/terms-of-service.html",
  };

  var EN_TO_PL = {
    "/en": "/",
    "/en/": "/",
    "/en/index.html": "/",
    "/en/about.html": "/o-nas.html",
    "/en/privacy-policy.html": "/polityka-prywatnosci.html",
    "/en/terms-of-service.html": "/regulamin.html",
  };

  function normalizePath(pathname) {
    if (!pathname || pathname === "/") return "/";
    if (pathname.endsWith("/") && pathname.length > 1) {
      return pathname.slice(0, -1);
    }
    return pathname;
  }

  function browserPrefersPolish() {
    var langs = navigator.languages || [navigator.language || ""];
    for (var i = 0; i < langs.length; i++) {
      var code = (langs[i] || "").toLowerCase();
      if (code.indexOf("pl") === 0) return true;
    }
    return false;
  }

  function isEnglishPath(path) {
    return path === "/en" || path.indexOf("/en/") === 0;
  }

  function maybeAutoRedirect() {
    var stored = localStorage.getItem(STORAGE_KEY);
    if (stored === "pl" || stored === "en") return;

    var path = normalizePath(window.location.pathname);
    if (isEnglishPath(path)) return;
    if (browserPrefersPolish()) return;

    var target = PL_TO_EN[path];
    if (target && target !== path) {
      window.location.replace(target);
    }
  }

  function switchLocale(locale) {
    localStorage.setItem(STORAGE_KEY, locale);
    var path = normalizePath(window.location.pathname);
    var target =
      locale === "en"
        ? PL_TO_EN[path] || "/en/"
        : EN_TO_PL[path] || "/";
    if (target !== path) {
      window.location.href = target;
    }
  }

  maybeAutoRedirect();

  document.addEventListener("DOMContentLoaded", function () {
    var dropdown = document.querySelector(".lang-dropdown");
    if (!dropdown) return;

    var trigger = dropdown.querySelector(".lang-dropdown__trigger");
    var menu = dropdown.querySelector(".lang-dropdown__menu");
    if (!trigger || !menu) return;

    function closeMenu() {
      dropdown.classList.remove("is-open");
      trigger.setAttribute("aria-expanded", "false");
      menu.hidden = true;
    }

    function openMenu() {
      dropdown.classList.add("is-open");
      trigger.setAttribute("aria-expanded", "true");
      menu.hidden = false;
    }

    trigger.addEventListener("click", function (event) {
      event.preventDefault();
      event.stopPropagation();
      if (menu.hidden) openMenu();
      else closeMenu();
    });

    menu.addEventListener("click", function (event) {
      var btn = event.target.closest("[data-lang]");
      if (!btn) return;
      var locale = btn.getAttribute("data-lang");
      if (locale !== "pl" && locale !== "en") return;
      event.preventDefault();
      closeMenu();
      switchLocale(locale);
    });

    document.addEventListener("click", function (event) {
      if (!dropdown.contains(event.target)) closeMenu();
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") closeMenu();
    });
  });
})();
