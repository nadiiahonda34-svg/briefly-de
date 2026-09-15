Briefly — AI Letter Assistant

Production website: https://brieflyletters.com/
Repository: nadiiahonda34-svg/briefly-de
Updated: 2026-09-15

This repository is the source for the Briefly production website. Its CNAME,
canonical URLs, robots.txt and sitemap.xml use brieflyletters.com.
Publish this repository through its existing Pages configuration and keep the
production content in this repository only.

The site includes 28 German guides, 15 PDF templates and an interactive
pre-send checklist. The glossary contains 40 terms.
The letter assistant offers Google sign-in and calls its Cloudflare backend.
Article reading and the checklist do not require sign-in.

Operational settings for Search Console, AdSense, Google sign-in and the
consent message are documented in GOOGLE_SETUP.md. Repository configuration
does not prove that the corresponding account settings are complete.

The public site check runs after Pages deployment. It checks HTTPS, published
content, discovery files, SEO/internal-link consistency and the backend's CORS
preflight for the production origin. It does not sign in, create letters,
inspect private accounts or confirm an actual regional consent dialog.
