(() => {
  'use strict';
  for (const button of document.querySelectorAll('[data-copy-example]')) {
    const sample = document.getElementById(button.dataset.copyExample);
    const status = button.parentElement.querySelector('.copy-status');
    if (!sample || !status) continue;
    button.hidden = false;
    button.addEventListener('click', async () => {
      const text = sample.innerText.trim();
      try {
        await navigator.clipboard.writeText(text);
        status.textContent = 'Muster kopiert. Bitte Platzhalter ersetzen und den Text prüfen.';
      } catch (_) {
        sample.focus();
        const selection = window.getSelection();
        if (selection) {
          const range = document.createRange();
          range.selectNodeContents(sample);
          selection.removeAllRanges();
          selection.addRange(range);
        }
        status.textContent = 'Bitte den markierten Mustertext manuell kopieren und die Platzhalter ersetzen.';
      }
    });
  }
})();
