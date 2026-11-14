/*
  Fills the page with the settings from config.js.
  The HTML already contains the same text, so pages still read correctly
  if this file fails to load.
*/
(function () {
  var S = window.SITE;
  if (!S) return;

  function each(selector, fn) {
    var list = document.querySelectorAll(selector);
    for (var i = 0; i < list.length; i++) fn(list[i]);
  }

  // Plain text: <span data-site="name">...</span>
  each("[data-site]", function (el) {
    var value = S[el.getAttribute("data-site")];
    if (value) el.textContent = value;
  });

  // Web address shown without "https://" (used on the flyer)
  each("[data-site-url]", function (el) {
    el.textContent = S.url.replace(/^https?:\/\//, "").replace(/\/$/, "");
  });

  // Page title: <html data-title="{name}: ...">
  var titleTemplate = document.documentElement.getAttribute("data-title");
  if (titleTemplate) document.title = titleTemplate.replace("{name}", S.name);

  // Email links: <a data-mailto data-subject="..." data-body="...">
  each("a[data-mailto]", function (a) {
    var params = [];
    var subject = a.getAttribute("data-subject");
    var body = a.getAttribute("data-body");
    if (subject) params.push("subject=" + encodeURIComponent(subject));
    if (body) {
      body = body.replace(/\{team\}/g, S.team).replace(/\\n/g, "\r\n");
      params.push("body=" + encodeURIComponent(body));
    }
    a.href = "mailto:" + S.email + (params.length ? "?" + params.join("&") : "");
  });

  // "Copy email address" button
  each("[data-copy-email]", function (btn) {
    var status = document.getElementById(btn.getAttribute("aria-describedby"));
    btn.hidden = false;
    btn.addEventListener("click", function () {
      function done(ok) {
        if (status) {
          status.textContent = ok
            ? "Copied. You can paste it into any email app."
            : "Could not copy. The address is " + S.email + ".";
        }
      }
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(S.email).then(function () { done(true); }, function () { done(false); });
      } else {
        done(false);
      }
    });
  });

  // Print button on the flyer
  each("[data-print]", function (btn) {
    btn.addEventListener("click", function () { window.print(); });
  });
})();
