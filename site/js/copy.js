/* Copy-to-clipboard helpers.

   This file does two jobs:
   1. It keeps the older textarea copy-button behaviour for prompt/edit blocks.
   2. It adds a small copy button to every command/code block on the website.

   The code block button copies only the text inside the code block. It does not
   copy labels, headings, or terminal prompt symbols added by the page. */

(function () {
  "use strict";

  function flash(button, ok) {
    var original = button.dataset.label || button.textContent;
    button.dataset.label = original;
    button.textContent = ok ? "Copied" : "Press Ctrl/Cmd+C";
    button.classList.toggle("copied", ok);
    window.setTimeout(function () {
      button.textContent = original;
      button.classList.remove("copied");
    }, 1600);
  }

  function copyText(text, button, fallbackElement) {
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(
        function () { flash(button, true); },
        function () { selectFallback(text, button, fallbackElement); }
      );
    } else {
      selectFallback(text, button, fallbackElement);
    }
  }

  function selectFallback(text, button, fallbackElement) {
    var ok = false;

    // If this is a textarea, select its existing content so the user can copy
    // manually if the browser blocks script copying.
    if (fallbackElement && fallbackElement.tagName === "TEXTAREA") {
      fallbackElement.focus();
      fallbackElement.select();
      try {
        ok = document.execCommand("copy");
      } catch (e) {
        ok = false;
      }
      flash(button, ok);
      return;
    }

    // Otherwise create a temporary textarea just for copying code text.
    var temp = document.createElement("textarea");
    temp.value = text;
    temp.setAttribute("readonly", "");
    temp.style.position = "fixed";
    temp.style.left = "-9999px";
    temp.style.top = "0";
    document.body.appendChild(temp);
    temp.focus();
    temp.select();
    try {
      ok = document.execCommand("copy");
    } catch (e2) {
      ok = false;
    }
    document.body.removeChild(temp);
    flash(button, ok);
  }

  function copyFromTextarea(textarea, button) {
    copyText(textarea.value, button, textarea);
  }

  function addCodeCopyButtons() {
    var blocks = document.querySelectorAll("pre > code");
    blocks.forEach(function (code) {
      var pre = code.parentElement;
      if (!pre || pre.dataset.copyReady === "true") return;
      pre.dataset.copyReady = "true";

      var wrapper = document.createElement("div");
      wrapper.className = "copy-code-block";
      pre.parentNode.insertBefore(wrapper, pre);
      wrapper.appendChild(pre);

      var button = document.createElement("button");
      button.type = "button";
      button.className = "copy-code-button";
      button.textContent = "Copy";
      button.setAttribute("aria-label", "Copy this code block");
      button.addEventListener("click", function () {
        copyText(code.textContent.trim(), button, code);
      });
      wrapper.appendChild(button);
    });
  }

  document.addEventListener("click", function (event) {
    var button = event.target.closest("[data-target]");
    if (!button) return;
    var textarea = document.getElementById(button.dataset.target);
    if (!textarea) return;
    copyFromTextarea(textarea, button);
  });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", addCodeCopyButtons);
  } else {
    addCodeCopyButtons();
  }
})();
