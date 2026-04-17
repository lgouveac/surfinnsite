/* Shared navbar + menu behaviour.
   Overrides toggleMenu() and toggleNavGroup() inline handlers on every page. */
(function () {
  'use strict';

  function setMenu(open) {
    const menu = document.querySelector('.nav-menu');
    const overlay = document.querySelector('.nav-overlay');
    if (!menu || !overlay) return;
    menu.classList.toggle('active', open);
    overlay.classList.toggle('active', open);
    document.body.classList.toggle('menu-open', open);
  }

  // Replace inline handlers with our clean version
  window.toggleMenu = function () {
    const isOpen = document.body.classList.contains('menu-open');
    setMenu(!isOpen);
  };

  window.toggleNavGroup = function (btn) {
    const group = btn && btn.parentElement;
    if (!group) return;
    group.classList.toggle('open');
  };

  // Close menu when clicking overlay or pressing Escape
  document.addEventListener('click', function (e) {
    if (e.target && e.target.classList && e.target.classList.contains('nav-overlay')) {
      setMenu(false);
    }
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && document.body.classList.contains('menu-open')) {
      setMenu(false);
    }
  });

  // Close menu when an internal link is clicked
  document.addEventListener('click', function (e) {
    const link = e.target.closest && e.target.closest('.nav-menu a');
    if (link && !link.closest('.nav-group-toggle')) {
      // allow the click to navigate, then close
      setTimeout(() => setMenu(false), 10);
    }
  });
})();
