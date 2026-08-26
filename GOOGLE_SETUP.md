# Google setup for Briefly

## 1. Google Search / Search Console

The repository already contains the Google verification file and `sitemap.xml`. This branch also adds `robots.txt`.

After merging/deploying, add this sitemap in Google Search Console:

`https://nadiiahonda34-svg.github.io/briefly-de/sitemap.xml`

## 2. Google Sign-In

Do not put OAuth client secrets in this repository.

Create a **Web application** OAuth client in Google Cloud Console and add the deployed GitHub Pages origin to **Authorized JavaScript origins**:

`https://nadiiahonda34-svg.github.io`

For production, use your own HTTPS domain when available.

Google Identity Services requires a public OAuth **client ID** in the frontend. The client ID is not a client secret, but authentication still needs server-side session/token validation before it can protect paid/private user data.

## 3. Gemini API

Do **not** put a Gemini API key in `index.html`, JavaScript, GitHub Pages, or this public repository.

GitHub Pages is a static public site, so a browser-side Gemini key can be extracted by visitors. Put Gemini calls behind a server-side endpoint/serverless function and store `GEMINI_API_KEY` as a secret/environment variable there.

Recommended architecture:

Browser (Briefly) -> your `/api/generate` HTTPS endpoint -> Gemini API

The endpoint should:

- accept only the fields Briefly needs;
- validate input length and allowed modes/languages;
- rate-limit requests;
- call Gemini using the server-side API key;
- return only the generated text;
- never return the API key to the browser.

Then configure the frontend with the public endpoint URL, not with a Gemini key.

## Required values before full integration

To finish Google Login + live Gemini generation, provide/configure:

- `GOOGLE_CLIENT_ID` — OAuth Web client ID;
- `BRIEFLY_API_URL` — deployed backend/serverless endpoint;
- server-side `GEMINI_API_KEY` — stored only in the backend provider's secret manager/environment.

Never commit the Gemini key or an OAuth client secret to GitHub.
