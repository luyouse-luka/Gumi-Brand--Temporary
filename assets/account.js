(function () {
  'use strict';

  var acctNav = {
    init: function () {
      var btn = document.querySelector('[data-acct-menu-toggle]');
      var menu = document.querySelector('[data-acct-menu]');
      if (!btn || !menu) return;              // not on this page

      var header = btn.closest('.gb-acct-header');

      function setOpen(open) {
        btn.setAttribute('aria-expanded', String(open));
        menu.hidden = !open;
        if (header) header.classList.toggle('is-open', open);
      }

      btn.addEventListener('click', function () {
        setOpen(btn.getAttribute('aria-expanded') !== 'true');
      });
      document.addEventListener('click', function (e) {
        if (menu.hidden || btn.contains(e.target) || menu.contains(e.target)) return;
        setOpen(false);
      });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && !menu.hidden) {
          setOpen(false);
          btn.focus();
        }
      });

      acctNav._setOpen = setOpen;
    },
    closeMenu: function () {
      if (acctNav._setOpen) acctNav._setOpen(false);
    }
  };

  document.addEventListener('DOMContentLoaded', function () {
    var modules = [['acctNav', acctNav]];
    for (var i = 0; i < modules.length; i++) {
      try { modules[i][1].init(); }
      catch (e) { if (window.console && console.error) console.error('gumiAcct:' + modules[i][0], e); }
    }
  });

  window.gumiAcct = { acctNav: acctNav };
})();
