# Briefly production setup

Production origin: https://brieflyletters.com
Public sitemap: https://brieflyletters.com/sitemap.xml
Source repository: nadiiahonda34-svg/briefly-de
Configuration reviewed: 2026-09-14

## What is already configured in this repository

- CNAME: brieflyletters.com.
- Canonical URLs and sitemap entries use the production domain.
- robots.txt allows crawling and points to the production sitemap.
- The AdSense account meta tag and homepage script use publisher ID pub-8272791832669756.
- ads.txt contains the same publisher ID.
- The homepage privacy-settings link integrates with Google's consent API and
  retains a link to the privacy policy if the API is unavailable.
- The glossary description is consistent at 40 terms in all nine interface languages.

These items describe source configuration. They do not confirm account approval,
DNS propagation, successful sign-in or a displayed consent dialog.

## 1. Domain and HTTPS

The registrar/DNS configuration must point brieflyletters.com to this GitHub
Pages site. Check the existing repository Pages custom-domain configuration and
the issued HTTPS certificate. Keep the primary domain consistent.

The automatic public check validates normal HTTPS responses after a Pages
deployment. It does not disable certificate verification.

## 2. Search Console

Use a property that covers https://brieflyletters.com/ and submit:
https://brieflyletters.com/sitemap.xml

Inspect the homepage and catalogue on that domain. The existing Google
verification file is present, but the account's property and verification
status must still be checked. An old GitHub Pages property is not a substitute
for the new domain's property.

Official instructions:
https://support.google.com/webmasters/answer/34592

## 3. AdSense site entry

Check AdSense > Sites for brieflyletters.com. If it is absent, add it as a new
site and use one of the verification methods supported by AdSense.
The source already includes the publisher meta tag, homepage ad script and
ads.txt. Do not replace the publisher ID with an example value.

Review the status of this exact domain. Approval or a pending review of the
old GitHub Pages address does not establish approval of brieflyletters.com.
Request review only after checking the deployed site.

Official instructions:
https://support.google.com/adsense/answer/12169212

## 4. European consent message

In AdSense > Privacy & messaging > European regulations, check that the
published message applies to brieflyletters.com. A previously published
message does not by itself confirm that the new domain is selected.

In a fresh browser session from the EEA, check the actual message and the
Privacy and cookie settings link after a consent choice. Google's existing
AdSense tag can deliver a published message; an additional homemade banner
is not needed to duplicate it.

For diagnostic preview, Google's documentation describes the fc and fctype
URL parameters. A forced preview is not proof of normal regional behavior.

Official requirements and API documentation:
https://support.google.com/adsense/answer/13554116
https://developers.google.com/funding-choices/fc-api-docs

## 5. Google sign-in

In the Google Cloud console, the existing Web application's authorized
JavaScript origins must include:
https://brieflyletters.com

Keep the public client ID aligned with the backend token audience. Do not
commit an OAuth client secret or a Gemini API key.
Test sign-in and sign-out on the production origin using a normal browser.

## 6. Cloudflare backend

The production frontend calls:
https://briefly-api.nadiiahonda34.workers.dev/

The backend must accept the production origin, POST, and the Content-Type
and Authorization headers used by the browser. Token validation, rate limits,
the daily counter and any Gemini credential remain server-side.

The public check makes an unauthenticated OPTIONS preflight only. It does
not generate text or consume the daily allowance. A passing preflight does
not prove that authentication or generation succeeds.

## Remaining checks that require account/browser access

- The new domain's AdSense site status.
- Selection and publication of the consent message for that domain.
- Actual regional consent display and reopening settings.
- Google sign-in and generation on the production domain.
