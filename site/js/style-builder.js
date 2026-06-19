/* Style builder: turns the form choices into a style profile JSON file.

   Keeps a live preview in sync, shows the JSON, and lets the user download it
   or copy it. No server: the download is made in the browser from a Blob. */

(function () {
  "use strict";

  var fields = {
    name: "name",
    body_font: "body_font",
    body_size_pt: "body_size_pt",
    heading_font: "heading_font",
    heading_color: "heading_color",
    h1_size_pt: "h1_size_pt",
    h2_size_pt: "h2_size_pt",
    h3_size_pt: "h3_size_pt",
    html_title: "html_title"
  };

  var numberKeys = ["body_size_pt", "h1_size_pt", "h2_size_pt", "h3_size_pt"];

  function val(id) {
    return document.getElementById(id).value;
  }

  function cleanHex(s) {
    return (s || "").replace(/[^0-9a-fA-F]/g, "").slice(0, 6).toUpperCase();
  }

  function profile() {
    var p = {};
    Object.keys(fields).forEach(function (key) {
      var v = val(fields[key]);
      if (numberKeys.indexOf(key) !== -1) {
        v = parseInt(v, 10);
        if (isNaN(v)) v = 0;
      }
      if (key === "heading_color") v = cleanHex(v);
      p[key] = v;
    });
    return p;
  }

  function asJson() {
    return JSON.stringify(profile(), null, 2);
  }

  function updatePreview() {
    var p = profile();
    var pv = document.getElementById("preview");
    var h1 = pv.querySelector(".pv-h1");
    var h2 = pv.querySelector(".pv-h2");
    var body = pv.querySelector(".pv-body");
    var list = pv.querySelector("ul");
    var color = "#" + cleanHex(p.heading_color);

    h1.style.fontFamily = p.heading_font;
    h1.style.fontSize = p.h1_size_pt + "pt";
    h1.style.color = color;
    h2.style.fontFamily = p.heading_font;
    h2.style.fontSize = p.h2_size_pt + "pt";
    h2.style.color = color;
    body.style.fontFamily = p.body_font;
    body.style.fontSize = p.body_size_pt + "pt";
    list.style.fontFamily = p.body_font;
    list.style.fontSize = p.body_size_pt + "pt";

    document.getElementById("json-out").textContent = asJson();
  }

  // Keep the colour picker and the hex text box in step.
  var picker = document.getElementById("heading_color_picker");
  var hexBox = document.getElementById("heading_color");
  picker.addEventListener("input", function () {
    hexBox.value = cleanHex(picker.value);
    updatePreview();
  });
  hexBox.addEventListener("input", function () {
    var hex = cleanHex(hexBox.value);
    if (hex.length === 6) picker.value = "#" + hex;
    updatePreview();
  });

  // Update on any change.
  Object.keys(fields).forEach(function (key) {
    var el = document.getElementById(fields[key]);
    el.addEventListener("input", updatePreview);
    el.addEventListener("change", updatePreview);
  });

  // Download as a .json file, named after the profile.
  document.getElementById("download-btn").addEventListener("click", function () {
    var p = profile();
    var safeName = (p.name || "style").replace(/[^a-zA-Z0-9_-]+/g, "-");
    var blob = new Blob([asJson()], { type: "application/json" });
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    a.href = url;
    a.download = safeName + ".json";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  });

  // The copy button reads the live JSON (copy.js handles data-target; this one
  // uses data-json, so wire it directly).
  document.getElementById("copy-json").addEventListener("click", function () {
    var text = asJson();
    var btn = this;
    function flash(ok) {
      var original = btn.dataset.label || btn.textContent;
      btn.dataset.label = original;
      btn.textContent = ok ? "Copied" : "Copy failed";
      btn.classList.toggle("copied", ok);
      setTimeout(function () {
        btn.textContent = original;
        btn.classList.remove("copied");
      }, 1600);
    }
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(function () { flash(true); }, function () { flash(false); });
    } else {
      var ta = document.createElement("textarea");
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      var ok = false;
      try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
      document.body.removeChild(ta);
      flash(ok);
    }
  });

  updatePreview();
})();
