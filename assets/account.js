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

  /* acctForm — note 2284:27446: Save stays asleep until the form above it has
   * actually been changed. Panels with nothing to change (the confirm-only ones)
   * have no [data-acct-field] and are left alone, which is also how their boards
   * draw them: green, not #e6e6e6.
   */
  var acctForm = {
    watch: function (panel) {
      var save = panel.querySelector('[data-acct-save]');
      var fields = panel.querySelectorAll('[data-acct-field]');
      if (!save || !fields.length || panel.getAttribute('data-acct-watched')) return;
      panel.setAttribute('data-acct-watched', '1');
      var initial = this._snapshot(fields);
      save.disabled = true;
      var self = this;
      panel.addEventListener('input', function () {
        save.disabled = self._snapshot(fields) === initial;
      });
      // A <select> fires change, not input, in older engines; listening to both
      // costs nothing and the comparison is idempotent.
      panel.addEventListener('change', function () {
        save.disabled = self._snapshot(fields) === initial;
      });
    },

    _snapshot: function (fields) {
      var v = [];
      for (var i = 0; i < fields.length; i++) v.push(fields[i].value);
      return v.join('\u0000');
    }
  };

  /* acctQty — the product card stepper.
   *
   * ⚠ The floor is declared per card (data-acct-qty-min), not inferred from how
   * many cards are on screen. Note 34502 is about the subscription's last
   * product, and how many of its products a panel happens to render is not the
   * same question -- 30960 draws one card that may still go to 0 because the
   * subscription has others.
   */
  var acctQty = {
    bind: function (root) {
      if (root.getAttribute('data-acct-qty-bound')) return;   // delegated: once only
      root.setAttribute('data-acct-qty-bound', '1');
      var self = this;
      root.addEventListener('click', function (e) {
        var btn = e.target.closest && e.target.closest('[data-acct-qty]');
        if (!btn || btn.disabled) return;
        var row = btn.closest('[data-acct-product]');
        var out = row && row.querySelector('[data-acct-qty-value]');
        if (!out) return;
        var n = parseInt(out.textContent, 10) || 0;
        var min = parseInt(row.getAttribute('data-acct-qty-min'), 10) || 0;
        var next = n + (btn.getAttribute('data-acct-qty') === 'up' ? 1 : -1);
        if (next < min) return;
        out.textContent = next;
        self._sync(root, row, next, min);
      });
      var rows = root.querySelectorAll('[data-acct-product]');
      for (var i = 0; i < rows.length; i++) {
        var v = rows[i].querySelector('[data-acct-qty-value]');
        var m = parseInt(rows[i].getAttribute('data-acct-qty-min'), 10) || 0;
        this._sync(root, rows[i], parseInt(v ? v.textContent : '0', 10) || 0, m);
      }
    },

    _sync: function (root, row, n, min) {
      var down = row.querySelector('[data-acct-qty="down"]');
      if (down) down.disabled = n <= min;
      var cta = root.querySelector('[data-acct-save]');
      if (!cta) return;
      // note 34504: a product stepped down to nothing turns the action into a
      // removal -- but only where 0 means "take it out". In the picker 0 just
      // means "not chosen", and 28942/29399 keep the CTA at "Add products", so
      // the swap is opt-in per panel rather than automatic.
      var zeroLabel = cta.getAttribute('data-acct-label-zero');
      if (!zeroLabel) return;
      var zero = false;
      var rows = root.querySelectorAll('[data-acct-product]');
      for (var i = 0; i < rows.length; i++) {
        var v = rows[i].querySelector('[data-acct-qty-value]');
        var m = parseInt(rows[i].getAttribute('data-acct-qty-min'), 10) || 0;
        if (m === 0 && parseInt(v ? v.textContent : '1', 10) === 0) { zero = true; break; }
      }
      cta.textContent = zero ? zeroLabel : cta.getAttribute('data-acct-label-default');
    }
  };

  /* modal — every [data-acct-modal] opens the panel of the same name.
   *
   * The lock reuses the site's own is-modal-open rather than a second class of
   * ours. customstyle.scss already solves two traps here and a parallel lock
   * would have to solve them again: body must get overflow-x:clip /
   * overflow-y:visible (hidden makes body the sticky header's scrollport and
   * .gb-acct-header drops out of view), and the freed scrollbar width must be
   * padded back on html ONLY (paying it on both spends it twice). Setting the
   * class is not calling main.js -- the two scripts still do not talk.
   *
   * ⚠ main.js also drives is-modal-open for [data-modal]. account.html has no
   * [data-modal] trigger, so the two never hold the lock at once; if one is ever
   * added here, whichever closes first would unlock the other.
   */
  var modal = {
    _last: null,

    init: function () {
      var self = this;
      // Armed up front, not on first open: the board ships Save greyed out, so
      // it has to be disabled before the panel is ever shown.
      var panels = document.querySelectorAll('.gb-acct-modal');
      for (var i = 0; i < panels.length; i++) {
        acctForm.watch(panels[i]);
        acctQty.bind(panels[i]);
      }
      document.addEventListener('click', function (e) {
        if (!e.target.closest) return;
        var open = e.target.closest('[data-acct-modal]');
        if (open) {
          e.preventDefault();
          self.open(open.getAttribute('data-acct-modal'), open);
          return;
        }
        if (e.target.closest('[data-acct-modal-close]')) { e.preventDefault(); self.close(); }
      });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && self.isOpen()) { e.preventDefault(); self.close(); }
        else if (e.key === 'Tab' && self.isOpen()) self._trap(e);
      });
    },

    isOpen: function () { return !!document.querySelector('.gb-acct-modal.is-open'); },

    panel: function (name) {
      return document.querySelector('.gb-acct-modal[data-acct-modal-panel="' + name + '"]');
    },

    open: function (name, trigger) {
      var el = this.panel(name);
      if (!el) return;                                  // panel not built yet
      var already = this.isOpen();
      if (already) this._hide(document.querySelector('.gb-acct-modal.is-open'));
      this._last = trigger || this._last;
      // Measure while the scrollbar is still on screen, and only the first time:
      // the cancel flow swaps content inside one open panel, and a second
      // measurement would read 0 and wipe the compensation already applied.
      if (!document.documentElement.classList.contains('is-modal-open')) {
        var sbw = window.innerWidth - document.documentElement.clientWidth;
        document.documentElement.style.setProperty('--scrollbar-w', sbw + 'px');
        document.documentElement.classList.add('is-modal-open');
        document.body.classList.add('is-modal-open');
      }
      el.hidden = false;
      void el.offsetWidth;                              // reflow, or the entry has nothing to run from
      el.classList.add('is-open');
      el.setAttribute('aria-hidden', 'false');
      // The dialog itself takes focus, not its first control: a scripted focus
      // with no pointer input before it still counts as :focus-visible, so the
      // ring would be painted the moment the panel appears.
      el.querySelector('.gb-acct-modal__panel').focus();
    },

    close: function () {
      var el = document.querySelector('.gb-acct-modal.is-open');
      if (!el) return;
      var self = this;
      var back = this._last;
      this._last = null;
      this._hide(el, function () {
        // Released only after the exit has played: handing the scrollbar back
        // while the panel is still opaque makes the centred panel jump sideways.
        document.documentElement.classList.remove('is-modal-open');
        document.body.classList.remove('is-modal-open');
        if (back && document.contains(back)) back.focus();
        self._token = null;
      });
    },

    // Shared by close() and by open()-over-an-open-panel, which must not drop
    // the lock at all.
    _hide: function (el, done) {
      el.classList.remove('is-open');
      el.setAttribute('aria-hidden', 'true');
      var ms = this._exitMs(el);
      var token = this._token = {};
      setTimeout(function () {
        el.hidden = true;
        // A panel that was replaced mid-exit must not run the stale callback:
        // it would unlock the page under the panel that replaced it.
        if (done && token === this._token) done();
      }.bind(this), ms);
    },

    _exitMs: function (el) {
      var v = getComputedStyle(el).getPropertyValue('--acct-modal-exit').trim();
      var n = parseFloat(v);
      if (!n) return 0;
      return v.indexOf('ms') > -1 ? n : n * 1000;
    },

    // Focus stays inside the dialog while it is open.
    _trap: function (e) {
      var el = document.querySelector('.gb-acct-modal.is-open');
      var f = el.querySelectorAll('a[href], button:not([disabled]), input:not([disabled]),'
                                  + ' select:not([disabled]), textarea:not([disabled]),'
                                  + ' [tabindex]:not([tabindex="-1"])');
      if (!f.length) { e.preventDefault(); return; }
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  };

  document.addEventListener('DOMContentLoaded', function () {
    // view runs after acctNav: its init calls acctNav.closeMenu().
    var modules = [['acctNav', acctNav], ['view', view], ['modal', modal]];
    for (var i = 0; i < modules.length; i++) {
      try { modules[i][1].init(); }
      catch (e) { if (window.console && console.error) console.error('gumiAcct:' + modules[i][0], e); }
    }
  });

  window.gumiAcct = { acctNav: acctNav, view: view, modal: modal, form: acctForm, qty: acctQty };
})();
