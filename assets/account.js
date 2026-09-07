(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    var modules = [];
    for (var i = 0; i < modules.length; i++) {
      try { modules[i][1].init(); }
      catch (e) { if (window.console && console.error) console.error('gumiAcct:' + modules[i][0], e); }
    }
  });

  window.gumiAcct = {};
})();
