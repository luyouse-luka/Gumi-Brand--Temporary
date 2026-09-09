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

  var view = {
    init: function () {
      if (!document.querySelector('[data-acct-view]')) return;   // not on this page
      var self = this;

      document.addEventListener('click', function (e) {
        var t = e.target.closest && e.target.closest('[data-acct-goto]');
        if (!t || t.getAttribute('aria-disabled') === 'true') return;
        e.preventDefault();
        self.show(t.getAttribute('data-acct-goto'));
        acctNav.closeMenu();
      });

      window.addEventListener('hashchange', function () {
        self.show(location.hash.slice(1));
      });

      this.show(location.hash.slice(1));
    },

    show: function (name) {
      var views = document.querySelectorAll('[data-acct-view]');
      var found = false;
      var i;
      for (i = 0; i < views.length; i++) {
        var match = views[i].getAttribute('data-acct-view') === name;
        views[i].hidden = !match;
        if (match) found = true;
      }
      if (!found) { this.show('overview'); return; }             // unknown hash

      var links = document.querySelectorAll('[data-acct-goto]');
      for (i = 0; i < links.length; i++) {
        var on = links[i].getAttribute('data-acct-goto') === name;
        links[i].classList.toggle('is-current', on);
        if (on) links[i].setAttribute('aria-current', 'page');
        else links[i].removeAttribute('aria-current');
      }

      if (location.hash.slice(1) !== name) {
        history.replaceState(null, '', '#' + name);
      }
      window.scrollTo(0, 0);
    }
  };

  document.addEventListener('DOMContentLoaded', function () {
    // view runs after acctNav: its init calls acctNav.closeMenu().
    var modules = [['acctNav', acctNav], ['view', view]];
    for (var i = 0; i < modules.length; i++) {
      try { modules[i][1].init(); }
      catch (e) { if (window.console && console.error) console.error('gumiAcct:' + modules[i][0], e); }
    }
  });

  window.gumiAcct = { acctNav: acctNav, view: view };
})();
