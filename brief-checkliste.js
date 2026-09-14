(() => {
  'use strict';
  const panel = document.getElementById('versand-check');
  if (!panel) return;
  const checks = [...panel.querySelectorAll('input[type="checkbox"]')];
  const count = document.getElementById('send-check-count');
  const progress = document.getElementById('send-check-progress');
  const next = document.getElementById('send-check-next');
  const reset = document.getElementById('send-check-reset');
  const print = document.getElementById('send-check-print');
  function update() {
    const checked = checks.filter(input => input.checked).length;
    count.textContent = checked + ' von ' + checks.length + ' Punkten geprüft.';
    progress.max = checks.length;
    progress.value = checked;
    next.textContent = checked === checks.length
      ? 'Sie haben alle Punkte selbst abgehakt. Klären Sie verbleibende Unsicherheiten vor dem Versand; die Liste ist keine automatische Inhalts- oder Rechtsprüfung.'
      : 'Noch ' + (checks.length - checked) + ' Punkte offen. Gehen Sie diese anhand Ihrer Unterlagen durch.';
  }
  checks.forEach(input => input.addEventListener('change', update));
  reset.addEventListener('click', () => {
    checks.forEach(input => { input.checked = false; });
    update();
  });
  print.addEventListener('click', () => window.print());
  window.addEventListener('pageshow', update);
  reset.hidden = false;
  print.hidden = false;
  update();
})();
