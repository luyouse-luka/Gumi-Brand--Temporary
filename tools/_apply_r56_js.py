# -*- coding: utf-8 -*-
"""Round 54 (build r56) -- main.js edits."""
import sys
P = "/home/ly/project/Gumi-Brand/assets/main.js"
s = open(P, encoding="utf-8").read()

EDITS = []

# 1) the selectBox module, inserted after enquiryPrefill
EDITS.append(("""  /* ---------------------------------------------------------------------
   * smoothScroll — site-wide smooth scrolling on Lenis 1.3.11 (MIT), vendored to""",
"""  /* ---------------------------------------------------------------------
   * selectBox — client-set: the enquiry select is presented as a button and a
   * ul listbox so the chevron can rotate. A native <select> paints its own
   * popup, and the background-image arrow it used before cannot be transformed.
   *
   * An enhancement, not a replacement. The native control stays in the DOM as
   * the single source of the options AND as the form's value carrier, so submit
   * still posts `enquiry`, enquiryPrefill still works, and if this module ever
   * throws the user is left with the native control rather than nothing.
   * It runs after enquiryPrefill so the button opens on the preselected option.
   *
   * ARIA listbox pattern: the ul takes focus and moves aria-activedescendant,
   * so no option ever holds a tabindex. Typeahead is not implemented.
   * ------------------------------------------------------------------- */
  var selectBox = {
    boxes: [],

    init: function () {
      var self = this;
      var all = document.querySelectorAll("select[data-select]");
      for (var i = 0; i < all.length; i++) { this.build(all[i]); }
      if (!this.boxes.length) { return; }

      document.addEventListener("click", function (e) {
        for (var i = 0; i < self.boxes.length; i++) {
          var b = self.boxes[i];
          if (b.open && !b.wrap.contains(e.target)) { self.close(b, false); }
        }
      });
    },

    build: function (native) {
      if (!native.options.length) { return; }
      var self = this;
      var id = native.id || ("gb-select-" + this.boxes.length);

      var wrap = document.createElement("div");
      wrap.className = "gb-select";
      native.parentNode.insertBefore(wrap, native);
      wrap.appendChild(native);
      native.classList.add("gb-select__native");
      native.setAttribute("tabindex", "-1");
      native.setAttribute("aria-hidden", "true");

      var btn = document.createElement("button");
      btn.type = "button";
      btn.id = id + "-button";
      btn.className = "gb-field__input gb-field__input--select gb-select__button";
      btn.setAttribute("aria-haspopup", "listbox");
      btn.setAttribute("aria-expanded", "false");
      btn.setAttribute("aria-controls", id + "-list");
      btn.innerHTML =
        '<span class="gb-select__value"></span>' +
        '<svg class="gb-select__arrow" viewBox="0 0 20 20" fill="none" aria-hidden="true">' +
        '<path d="M5 7.5L10 12.5L15 7.5" stroke="#4d4d4d" stroke-width="1.667" ' +
        'stroke-linecap="round" stroke-linejoin="round"/></svg>';

      // The label pointed at a control that is now off-screen. A button is not a
      // labelable element, so the association has to move to aria-labelledby.
      var label = document.querySelector('label[for="' + id + '"]');
      if (label) {
        if (!label.id) { label.id = id + "-label"; }
        label.removeAttribute("for");
        label.addEventListener("click", function () { btn.focus(); });
        btn.setAttribute("aria-labelledby", label.id + " " + btn.id);
      }

      var list = document.createElement("ul");
      list.className = "gb-select__list";
      list.id = id + "-list";
      list.setAttribute("role", "listbox");
      list.setAttribute("tabindex", "-1");
      if (label) { list.setAttribute("aria-labelledby", label.id); }
      // Built after smoothScroll.init has swept the DOM for PREVENT, so it has to
      // opt out of Lenis itself.
      list.setAttribute("data-lenis-prevent", "");

      for (var i = 0; i < native.options.length; i++) {
        var li = document.createElement("li");
        li.className = "gb-select__option";
        li.id = id + "-opt-" + i;
        li.setAttribute("role", "option");
        li.textContent = native.options[i].text;
        list.appendChild(li);
      }

      wrap.appendChild(btn);
      wrap.appendChild(list);

      var box = { wrap: wrap, native: native, btn: btn, list: list,
                  value: btn.firstChild, open: false, active: -1 };
      this.boxes.push(box);
      this.sync(box);

      btn.addEventListener("click", function () {
        if (box.open) { self.close(box, true); } else { self.show(box); }
      });

      btn.addEventListener("keydown", function (e) {
        var k = e.key;
        if (k === "ArrowDown" || k === "ArrowUp" || k === "Enter" || k === " ") {
          e.preventDefault();          // also stops Enter/Space firing click twice
          self.show(box);
        }
      });

      list.addEventListener("click", function (e) {
        var li = e.target.closest && e.target.closest(".gb-select__option");
        if (!li) { return; }
        self.choose(box, Array.prototype.indexOf.call(list.children, li));
        self.close(box, true);
      });

      list.addEventListener("keydown", function (e) {
        var k = e.key, last = list.children.length - 1;
        if (k === "Escape") { e.stopPropagation(); self.close(box, true); }
        else if (k === "Tab") { self.close(box, false); }
        else if (k === "ArrowDown") { e.preventDefault(); self.move(box, box.active + 1); }
        else if (k === "ArrowUp") { e.preventDefault(); self.move(box, box.active - 1); }
        else if (k === "Home") { e.preventDefault(); self.move(box, 0); }
        else if (k === "End") { e.preventDefault(); self.move(box, last); }
        else if (k === "Enter" || k === " ") {
          e.preventDefault();
          self.choose(box, box.active);
          self.close(box, true);
        }
      });

      // Anything that drives the real control (enquiryPrefill, a Shopify app,
      // a form reset) is mirrored back into the drawn one.
      native.addEventListener("change", function () { self.sync(box); });
    },

    show: function (box) {
      if (box.open) { return; }
      box.open = true;
      box.wrap.classList.add("is-open");
      box.btn.setAttribute("aria-expanded", "true");
      this.move(box, box.native.selectedIndex);
      box.list.focus();
    },

    close: function (box, refocus) {
      if (!box.open) { return; }
      box.open = false;
      box.wrap.classList.remove("is-open");
      box.btn.setAttribute("aria-expanded", "false");
      box.list.removeAttribute("aria-activedescendant");
      if (refocus) { box.btn.focus(); }
    },

    move: function (box, i) {
      var kids = box.list.children;
      if (!kids.length) { return; }
      i = Math.max(0, Math.min(kids.length - 1, i));
      for (var j = 0; j < kids.length; j++) {
        kids[j].classList.toggle("is-active", j === i);
      }
      box.active = i;
      box.list.setAttribute("aria-activedescendant", kids[i].id);
      kids[i].scrollIntoView({ block: "nearest" });
    },

    choose: function (box, i) {
      if (i < 0 || i >= box.native.options.length) { return; }
      if (box.native.selectedIndex !== i) {
        box.native.selectedIndex = i;
        box.native.dispatchEvent(new Event("change", { bubbles: true }));
      }
      this.sync(box);
    },

    sync: function (box) {
      var i = box.native.selectedIndex;
      box.value.textContent = i < 0 ? "" : box.native.options[i].text;
      var kids = box.list.children;
      for (var j = 0; j < kids.length; j++) {
        kids[j].setAttribute("aria-selected", j === i ? "true" : "false");
      }
    }
  };

  /* ---------------------------------------------------------------------
   * smoothScroll — site-wide smooth scrolling on Lenis 1.3.11 (MIT), vendored to""", 1))

# 2) register the new scrollable container
EDITS.append(('    PREVENT: ".gb-product__thumbs, .gb-header__panel, .gb-nl-panel__body",',
              '    PREVENT: ".gb-product__thumbs, .gb-header__panel, .gb-nl-panel__body, .gb-select__list",', 1))

# 3) init order: after enquiryPrefill, so the button opens on the preselected option
EDITS.append(('                   ["smoothScroll", smoothScroll], ["enquiryPrefill", enquiryPrefill]];',
              '                   ["smoothScroll", smoothScroll], ["enquiryPrefill", enquiryPrefill],\n'
              '                   ["selectBox", selectBox]];', 1))

EDITS.append(('                  smoothScroll: smoothScroll, enquiryPrefill: enquiryPrefill };',
              '                  smoothScroll: smoothScroll, enquiryPrefill: enquiryPrefill,\n'
              '                  selectBox: selectBox };', 1))

fails = []
for old, new, n in EDITS:
    c = s.count(old)
    if c != n:
        fails.append((c, n, old.strip().splitlines()[0][:80]))
        continue
    s = s.replace(old, new, n)
if fails:
    for c, n, head in fails:
        print("MISMATCH count=%d expected=%d :: %s" % (c, n, head))
    sys.exit(1)
open(P, "w", encoding="utf-8").write(s)
print("js: %d edits applied" % len(EDITS))
