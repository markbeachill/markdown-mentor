/* Copy-to-clipboard for the editable prompt and edit blocks.

   Each copy button has data-target pointing at a textarea id. The button copies
   the textarea's LIVE value, so anything the user edits is what gets copied.

   Works without a server. Falls back to a manual select if the clipboard API is
   blocked (which can happen when opening the page directly from disk). */

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

  function copyFrom(textarea, button) {
    var text = textarea.value;

    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(
        function () { flash(button, true); },
        function () { selectFallback(textarea, button); }
      );
    } else {
      selectFallback(textarea, button);
    }
  }

  function selectFallback(textarea, button) {
    // Older or file:// contexts: select the text and try execCommand.
    textarea.focus();
    textarea.select();
    var ok = false;
    try {
      ok = document.execCommand("copy");
    } catch (e) {
      ok = false;
    }
    flash(button, ok);
  }

  document.addEventListener("click", function (event) {
    var button = event.target.closest("[data-target]");
    if (!button) return;
    var textarea = document.getElementById(button.dataset.target);
    if (!textarea) return;
    copyFrom(textarea, button);
  });
})();
