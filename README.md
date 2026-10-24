# katachilabs-site (v2 prototype, two themes)
Static site for katachilabs.uk (plain HTML/CSS), published with GitHub Pages. Local prototype, not yet deployed.

- Main site, Clean Slate theme (`assets/clean-slate.css`): `/` home, `/bookmark-plus/` Bookmark+ landing (Chrome Web Store Homepage URL), `/bookmark-plus/privacy/` privacy policy (stable URL, text unchanged), `/consultancy/`, `/contact/`, `404.html`
- Labs, Midnight Studio theme (`assets/midnight.css`): `/labs/` hub, `/labs/bookmark-plus/` product page with gallery
- Shared tokens: `assets/tokens.css`. Images: `labs/bookmark-plus/img/` (WebP with PNG fallback)
- `CNAME` = katachilabs.uk

Tools (`_tools/`, ignored by Jekyll): `build.py` regenerates the HTML (copies the privacy policy body from the live repo copy), `images.py` optimises screenshots, `shots.py` takes screenshots, `linkcheck.py` checks internal links.

Placeholders to fill: search the HTML for `TBC` (contact email, community link, Chrome Web Store URL, build log entries).
Do not touch Proton MX/TXT/DKIM records at Porkbun.
