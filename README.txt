Briefly — AI Letter Assistant

Production website: https://brieflyletters.com/
Repository: nadiiahonda34-svg/briefly-de
Updated: 2026-10-04

This repository is the source for the Briefly production website. Its CNAME,
canonical URLs, robots.txt and sitemap.xml use brieflyletters.com.
Publish this repository through its existing Pages configuration and keep the
production content in this repository only.

The site includes 33 German guides, PDF templates and an interactive
pre-send checklist. The glossary contains 40 terms.
Seven local letter forms work without sign-in, with DE/RU/UK guidance.
The newest forms cover employer sick leave, rental repair requests and
school illness notifications. Translated entry pages link to each form.
Regenerate these entries using python3 scripts/build-everyday-guides.py.
Run node --test tests/*.test.mjs before publishing form changes.
The letter assistant offers Google sign-in and calls its Cloudflare backend.
Article reading and the checklist do not require sign-in.

Operational settings for Search Console, AdSense, Google sign-in and the
consent message are documented in GOOGLE_SETUP.md. Repository configuration
does not prove that the corresponding account settings are complete.

The public site check runs after Pages deployment. It checks HTTPS, published
content, discovery files, SEO/internal-link consistency and the backend's CORS
preflight for the production origin. It does not sign in, create letters,
inspect private accounts or confirm an actual regional consent dialog.
