(() => {
  'use strict';
  // Load Google's AdSense tag so the published Google CMP can be displayed.
  // Keep ad requests paused until the site is approved and advertising is enabled.
  window.adsbygoogle = window.adsbygoogle || [];
  window.adsbygoogle.pauseAdRequests = 1;
  window.googlefc = window.googlefc || {};
  window.googlefc.callbackQueue = window.googlefc.callbackQueue || [];

  const tag = document.createElement('script');
  tag.async = true;
  tag.crossOrigin = 'anonymous';
  tag.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8272791832669756';
  document.head.append(tag);
})();
