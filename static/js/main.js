// Mobile menu, inquiry modal and nav highlighting. Nothing else needs JavaScript.
(function () {
  "use strict";

  /* --- mobile menu -------------------------------------------------------- */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  /* --- highlight the current page in the nav ------------------------------ */
  var here = window.location.pathname;
  document.querySelectorAll(".site-nav a").forEach(function (link) {
    var href = link.getAttribute("href");
    // Skip in-page anchors such as /#why-us: they are not a separate page.
    if (href.indexOf("#") !== -1) return;
    if (href === here) {
      link.classList.add("active");
      link.setAttribute("aria-current", "page");
    }
  });

  /* --- inquiry modal ------------------------------------------------------ */
  var modal = document.getElementById("inquiry-modal");
  if (!modal) return;

  var box = modal.querySelector(".modal-box");
  var lastFocused = null;

  function focusable() {
    return box.querySelectorAll(
      'a[href], button:not([disabled]), input:not([type="hidden"]), textarea, select'
    );
  }

  function openModal() {
    lastFocused = document.activeElement;
    modal.hidden = false;
    document.body.classList.add("modal-open");
    var first = box.querySelector('input[name="full_name"]');
    if (first) first.focus();
  }

  function closeModal() {
    modal.hidden = true;
    document.body.classList.remove("modal-open");
    if (lastFocused) lastFocused.focus();
  }

  document.querySelectorAll(".js-open-modal").forEach(function (btn) {
    btn.addEventListener("click", openModal);
  });
  modal.querySelectorAll(".js-close-modal").forEach(function (btn) {
    btn.addEventListener("click", closeModal);
  });

  document.addEventListener("keydown", function (e) {
    if (modal.hidden) return;
    if (e.key === "Escape") {
      closeModal();
      return;
    }
    // Keep keyboard focus inside the dialog while it is open.
    if (e.key === "Tab") {
      var items = focusable();
      if (!items.length) return;
      var first = items[0];
      var last = items[items.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }
  });
})();
