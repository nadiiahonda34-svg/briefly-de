(() => {
  const box = document.querySelector('[data-share-guide]');
  if (!box) return;
  const button = box.querySelector('[data-share-button]');
  const status = box.querySelector('[data-share-status]');
  const fallback = box.querySelector('[data-share-fallback]');
  const input = box.querySelector('[data-share-url]');
  const url = document.querySelector('link[rel="canonical"]')?.href || location.href.split('#')[0];
  const title = document.querySelector('h1')?.textContent.trim() || 'Briefly';
  const language = document.documentElement.lang === 'uk' ? 'uk' : 'ru';
  const messages = {
    ru: {shared:'Ссылка отправлена.',copied:'Ссылка скопирована. Можно отправить её знакомому.',manual:'Выделите и скопируйте ссылку ниже.'},
    uk: {shared:'Посилання надіслано.',copied:'Посилання скопійовано. Можна надіслати його знайомим.',manual:'Виділіть і скопіюйте посилання нижче.'}
  }[language];
  box.hidden = false;
  button.addEventListener('click',async () => {
    try {
      if (navigator.share) {
        await navigator.share({title,url});
        status.textContent = messages.shared;
        return;
      }
    } catch (error) {if (error.name === 'AbortError') return;}
    try {
      await navigator.clipboard.writeText(url);
      status.textContent = messages.copied;
    } catch {
      input.value = url;
      fallback.hidden = false;
      input.focus();
      input.select();
      status.textContent = messages.manual;
    }
  });
})();
