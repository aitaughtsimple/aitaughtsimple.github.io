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

  // Calendar page in "Upcoming classes": "January 2027" -> "January" / "2027"
  var when = (S.firstClasses || "").split(" ");
  each("[data-site-month]", function (el) { if (when[0]) el.textContent = when[0]; });
  each("[data-site-year]", function (el) { if (when[1]) el.textContent = when[1]; });

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

  // Links like "Request a free class" pre-pick the topic in the contact form
  each("[data-topic]", function (link) {
    link.addEventListener("click", function () {
      var radio = document.querySelector('[data-contact-form] input[name="topic"][value^="I\'d like to host"]');
      if (link.getAttribute("data-topic") === "host" && radio) radio.checked = true;
    });
  });

  /*
    Contact form: messages go to the club inbox through FormSubmit (formsubmit.co).
    Without JavaScript the form still works: it posts normally and lands on /thanks/.
  */
  each("[data-contact-form]", function (form) {
    var card = form.parentNode;
    var success = card.querySelector(".form-success");
    var status = form.querySelector(".form-status");
    var button = form.querySelector('button[type="submit"]');
    var label = form.querySelector("[data-btn-label]");
    var endpoint = "https://formsubmit.co/ajax/" + S.email;

    form.action = "https://formsubmit.co/" + S.email;
    form.elements._next.value = S.url.replace(/\/?$/, "/") + "thanks/";
    form.noValidate = true; // we show our own, larger error messages

    var checks = [
      { name: "name", test: function (v) { return v.length > 0; }, msg: "Please type your name." },
      { name: "email", test: function (v) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v); }, msg: "Please type an email address, like name@example.com." },
      { name: "message", test: function (v) { return v.length > 1; }, msg: "Please write a short message." }
    ];

    function setError(field, msg) {
      var err = document.getElementById(field.id + "-err");
      field.setAttribute("aria-invalid", msg ? "true" : "false");
      if (err) { err.textContent = msg || ""; err.hidden = !msg; }
    }

    function validate() {
      var firstBad = null;
      checks.forEach(function (c) {
        var field = form.elements[c.name];
        var ok = c.test(field.value.trim());
        setError(field, ok ? "" : c.msg);
        if (!ok && !firstBad) firstBad = field;
      });
      return firstBad;
    }

    // Clear an error as soon as the person fixes that box
    checks.forEach(function (c) {
      form.elements[c.name].addEventListener("input", function () {
        if (this.getAttribute("aria-invalid") === "true" && c.test(this.value.trim())) setError(this, "");
      });
    });

    function busy(on) {
      button.disabled = on;
      button.setAttribute("aria-busy", on ? "true" : "false");
      label.textContent = on ? "Sending..." : "Send message";
    }

    function fail() {
      busy(false);
      status.className = "form-status is-error";
      status.textContent = "Your message did not send. Please try again, or email us at " + S.email + ".";
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      status.className = "form-status";
      status.textContent = "";

      var firstBad = validate();
      if (firstBad) {
        status.className = "form-status is-error";
        status.textContent = "Please fix what's marked below, then press Send message again.";
        firstBad.focus();
        return;
      }

      var data = {
        name: form.elements.name.value.trim(),
        email: form.elements.email.value.trim(),
        organization: form.elements.organization.value.trim() || "(not given)",
        topic: (form.querySelector('input[name="topic"]:checked') || {}).value || "Not chosen",
        message: form.elements.message.value.trim(),
        _subject: "",
        _template: "table",
        _captcha: "false",
        _honey: form.elements._honey.value,
        _autoresponse: "Thank you for contacting " + S.name + ". We got your message and will reply by email soon. (This is an automatic reply, so there's no need to answer it.)"
      };
      data._subject = "Website message: " + data.topic + " (from " + data.name + ")";

      if (data._honey) { showSuccess(data.email); return; } // spam bot filled the hidden box

      if (!window.fetch) { form.submit(); return; } // very old browser: normal post

      busy(true);
      fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify(data)
      })
        .then(function (r) { return r.json(); })
        .then(function (res) {
          if (String(res.success) === "true") showSuccess(data.email);
          else fail();
        })
        .catch(fail);
    });

    function showSuccess(email) {
      busy(false);
      form.reset();
      form.hidden = true;
      var sentTo = success.querySelector("[data-sent-email]");
      if (sentTo) sentTo.textContent = email;
      success.hidden = false;
      success.focus();
    }

    var again = success.querySelector("[data-send-another]");
    if (again) again.addEventListener("click", function () {
      success.hidden = true;
      form.hidden = false;
      status.textContent = "";
      form.elements.name.focus();
    });
  });
})();
