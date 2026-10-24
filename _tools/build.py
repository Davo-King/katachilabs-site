#!/usr/bin/env python3
"""Generates the static pages for katachilabs.uk v2 (two themes). Run from repo root.
The privacy policy <main> content is copied byte-for-byte from the live page (SRC_PRIVACY)."""
import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_PRIVACY = "/workspace/katachilabs-site/bookmark-plus/privacy/index.html"

FONTS_LIGHT = "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
FONTS_DARK = "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap"
CONTACT = '<a href="/contact/" class="placeholder-link"><span class="placeholder">[CONTACT EMAIL TBC]</span></a>'
NAV = [("Home", "/", "home"), ("Labs", "/labs/", "labs"), ("Consultancy", "/consultancy/", "consultancy"),
       ("Privacy", "/bookmark-plus/privacy/", "privacy"), ("Contact", "/contact/", "contact")]

def nav(active):
    out = []
    for label, href, key in NAV:
        cls = ' class="c"' if key == "contact" else ""
        cur = ' aria-current="page"' if key == active else ""
        out.append(f'<a href="{href}"{cls}{cur}>{label}</a>')
    return '<nav aria-label="Main">' + "".join(out) + "</nav>"

def head(title, desc, theme, extra=""):
    css = "clean-slate" if theme == "light" else "midnight"
    fonts = FONTS_LIGHT if theme == "light" else FONTS_DARK
    color = "#ffffff" if theme == "light" else "#0A0F1E"
    d = f'<meta name="description" content="{desc}">' if desc else ""
    return f'''<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>{d}<meta name="theme-color" content="{color}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{fonts}" rel="stylesheet">
<link rel="stylesheet" href="/assets/tokens.css"><link rel="stylesheet" href="/assets/{css}.css">{extra}
</head><body class="{'theme-light' if theme=='light' else 'theme-dark dark'}">
<a class="skip" href="#main">Skip to content</a>
'''

def header(theme, active):
    if theme == "light":
        logo = '<a class="logo" href="/" aria-label="KatachiLabs home"><i></i>KatachiLabs</a>'
    else:
        logo = '<a class="logo" href="/labs/" aria-label="KatachiLabs Labs home"><i></i><span>Katachi<b>Labs</b></span><small>labs</small></a>'
    return f'<header class="site"><div class="wrap">{logo}{nav(active)}</div></header>\n'

def footer(theme):
    if theme == "light":
        return f'''<footer class="site"><div class="wrap"><div>&copy; 2026 KatachiLabs</div>
<div class="l"><a href="/labs/">Labs</a><a href="/bookmark-plus/">Bookmark+</a><a href="/bookmark-plus/privacy/">Bookmark+ privacy policy</a><a href="/contact/">Contact</a></div></div></footer>
</body></html>
'''
    return f'''<footer class="site"><div class="wrap"><div>&copy; 2026 KatachiLabs Labs</div>
<div class="l"><a href="/">&larr; Back to the main site</a><a href="/bookmark-plus/privacy/">Bookmark+ privacy policy</a><a href="/contact/">Contact</a></div></div></footer>
</body></html>
'''

def page(path, title, desc, theme, active, body, extra=""):
    html = head(title, desc, theme, extra) + header(theme, active) + body + "\n" + footer(theme)
    full = os.path.join(ROOT, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(html)

IMG="/labs/bookmark-plus/img"
def pic(name, alt, w=1280, h=800, small=640, loading="lazy", cls="", sizes="(max-width:900px) 100vw, 1080px"):
    c=f' class="{cls}"' if cls else ""
    if small:
        ws=f"{IMG}/{name}-{small}.webp {small}w, {IMG}/{name}-1280.webp 1280w"
        wp=f"{IMG}/{name}-{small}.png {small}w, {IMG}/{name}-1280.png 1280w"
        return (f'<picture><source type="image/webp" srcset="{ws}" sizes="{sizes}"><img{c} src="{IMG}/{name}-1280.png" '
                f'srcset="{wp}" sizes="{sizes}" width="{w}" height="{h}" alt="{alt}" loading="{loading}" decoding="async"></picture>')
    return (f'<picture><source type="image/webp" srcset="{IMG}/{name}.webp"><img{c} src="{IMG}/{name}.png" width="{w}" height="{h}" alt="{alt}" loading="{loading}" decoding="async"></picture>')

ALT_DARK="The Bookmark+ new-tab dashboard in dark mode, showing a search bar, pinned sites, favourites, colour-coded categories such as Work, Learning and Recipes, and a Projects column. Sample bookmarks."
ALT_LIGHT="The Bookmark+ new-tab dashboard in light mode with pinned sites, favourites, categories and projects. Sample bookmarks."
ALT_SEARCH="Searching for 'google' in Bookmark+ shows ten matching bookmarks from different categories and projects in a drop-down list."
ALT_POPUP="The Bookmark+ toolbar pop-up, with a category list for saving the current page and options to save to a project or save all open tabs. Shortcut Alt+Shift+B."
ALT_SETTINGS="The Bookmark+ settings panel, with options for light or dark mode, six colour themes, font size, density, icon size, clock format and column widths."
ALT_PROMO="Bookmark+ logo tile: a bookmark icon with a plus sign, and the text 'A calm bookmark dashboard for your new tab.'"

SHOT_LIGHT = '<div class="shot" aria-hidden="true"><div class="dots"><i></i><i></i><i></i></div><div class="s">Search bookmarks</div><div class="g"><b></b><b></b><b></b><b></b><b></b><b></b><b></b><b></b></div></div>'
MOCK_DARK = '<div class="mock" aria-hidden="true"><div class="search mono">Search your bookmarks...</div><div class="row"><div class="tile on"></div><div class="tile"></div><div class="tile"></div><div class="tile"></div><div class="tile on"></div><div class="tile"></div></div></div>'
ICO_SHIELD = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l8 3v6c0 4.5-3.2 8-8 9-4.8-1-8-4.5-8-9V6z"/><path d="M9 12l2 2 4-4"/></svg>'
ICO_PEOPLE = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="9" cy="8" r="3"/><circle cx="17" cy="9" r="2.5"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6M15 14.5c3 0 6 1.5 6 5.5"/></svg>'
ICO_CASE = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 012-2h2a2 2 0 012 2v2M3 13h18"/></svg>'
ICO_CODE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 7l-5 5 5 5M16 7l5 5-5 5M14 4l-4 16"/></svg>'

# ---------------- MAIN SITE (Clean Slate) ----------------
home = f'''<main id="main">
<div class="wrap"><div class="hero"><div class="kicker">Independent tech studio</div>
<h1>Security shaped by design, <em>not disaster.</em></h1>
<p class="lead">KatachiLabs makes calm, privacy-first apps and builds a community of people who make and learn together. Consultancy will follow in time, built on the same principles.</p>
<div class="btns"><a class="btn p" href="/bookmark-plus/">Meet Bookmark+</a><a class="btn t" href="/labs/">Join the community &rarr;</a></div></div></div>
<hr>
<div class="wrap sec"><div class="label">What we do</div><h2>Apps, a community, and advice in time.</h2>
<div class="cols">
<div class="col"><span class="n">01</span><h3>Apps</h3><p>Small, focused tools that keep your data on your device. Our first is Bookmark+, a Chrome new-tab dashboard.</p><a class="more" href="/bookmark-plus/">See Bookmark+ &rarr;</a></div>
<div class="col"><span class="n">02</span><h3>Community</h3><p>We share what we are making and what we are learning, with people who like to build and learn together.</p><a class="more" href="/labs/">Visit Labs &rarr;</a></div>
<div class="col"><span class="n">03</span><h3>Consultancy</h3><p>Not available yet. In time, practical advice on security, privacy, data protection and governance.</p><a class="more" href="/consultancy/">Read more &rarr;</a></div>
</div></div>
<hr>
<div class="wrap sec"><div class="label">Our first product</div><h2>A quieter place to keep the web you use.</h2>
<div class="product"><div><div class="pills"><span class="pill a">Free</span><span class="pill">Coming soon</span></div>
<h3>Bookmark+</h3><p>A calm bookmark dashboard for your Chrome new tab, with categories, search, pins and projects. Everything stays on your device.</p><a class="btn p" href="/bookmark-plus/">Learn more</a></div>
<div class="promo">{pic("promo-440",ALT_PROMO,440,280,None,sizes=None)}</div></div></div>
<div class="wrap" style="padding-bottom:88px"><div class="labsband"><div><div class="tagline">KatachiLabs / Labs</div><h2>Where we build in the open.</h2>
<p>Labs is the builder side of KatachiLabs: what we are making, how it works, and a place to join in.</p><a class="btn" href="/labs/">Go to Labs</a></div>
<pre><span class="c"># how we build</span>
<span class="k">data</span>      = <span class="v">"stays on your device"</span>
<span class="k">tracking</span>  = <span class="v">none</span>
<span class="k">accounts</span>  = <span class="v">not required</span>
<span class="k">roadmap</span>   = <span class="v">shared with the community</span></pre></div></div>
<div class="wrap cta"><div class="box"><div><h2>Come and build with us.</h2><p>Whether you write code, ask good questions or just want to learn, there is a place for you.</p></div><a class="btn" href="/contact/">Say hello</a></div></div>
</main>'''
page("/index.html", "KatachiLabs | Security shaped by design, not disaster",
     "KatachiLabs is an independent tech studio building calm, privacy-first apps and a builder community. Home of Bookmark+.", "light", "home", home)

consult = f'''<main id="main"><div class="wrap">
<div class="hero sm"><div class="kicker">Consultancy</div><h1>Coming soon. <em>Not open yet.</em></h1>
<p class="lead">We plan to offer consultancy in time, built on the same principles as our apps. It is not available yet, and there is nothing to buy today.</p></div>
<div class="page" style="padding-top:0">
<div class="card soft"><h2>What to expect</h2><p>We expect consultancy to focus on practical, plain-English help in these areas:</p>
<ul><li>Security</li><li>Privacy and data protection</li><li>Data governance</li></ul>
<p style="margin-top:14px">This list is a direction of travel, not a service menu. Scope, availability and pricing are all to be confirmed.</p></div>
<div class="card"><h2>Interested?</h2><p>If you would like to talk, or be told when consultancy opens, get in touch.</p>
<div class="btns" style="margin-top:18px"><a class="btn p" href="/contact/">Get in touch</a><a class="btn t" href="/labs/">See what we are building &rarr;</a></div></div>
</div></div></main>'''
page("/consultancy/index.html", "Consultancy | KatachiLabs", "KatachiLabs consultancy is coming in time. Not available yet; get in touch to register interest.", "light", "consultancy", consult)

contact = f'''<main id="main"><div class="wrap">
<div class="hero sm"><div class="kicker">Contact</div><h1>Say <em>hello.</em></h1>
<p class="lead">Questions about Bookmark+, the community, or consultancy? Send us a message.</p></div>
<div class="page" style="padding-top:0">
<div class="card"><h2>Email</h2><p><a class="inline" href="mailto:contact-email-tbc@example.invalid"><span class="placeholder">[CONTACT EMAIL TBC]</span></a></p>
<p style="color:var(--muted);font-size:14.5px;margin-top:10px">Placeholder: the public contact address will be added here once it is confirmed.</p></div>
<div class="card soft"><h2>Good to know</h2><ul>
<li>Bookmark+ does not collect your data, so we cannot look up or recover bookmarks for you. See the <a class="inline" href="/bookmark-plus/privacy/">privacy policy</a>.</li>
<li>Consultancy is not open yet. Tell us what you have in mind and we will get back to you when it is.</li></ul></div>
</div></div></main>'''
page("/contact/index.html", "Contact | KatachiLabs", "How to contact KatachiLabs.", "light", "contact", contact)

# privacy: copy main content byte-for-byte from the live page
src = open(SRC_PRIVACY, encoding="utf-8").read()
m = re.search(r'<main class="wrap">(.*?)</main>', src, re.S)
assert m, "main not found in live privacy page"
inner = m.group(1)
privacy_body = f'<main id="main" class="wrap prose">{inner}</main>'
page("/bookmark-plus/privacy/index.html", "Bookmark+ Privacy Policy | KatachiLabs", "", "light", "privacy", privacy_body,
     extra='<link rel="canonical" href="https://katachilabs.uk/bookmark-plus/privacy/">')

# /bookmark-plus/ : real Clean Slate landing page (Chrome Web Store Homepage URL)
lp = f"""<main id="main">
<div class="wrap"><div class="hero sm" style="max-width:none"><div class="kicker">Chrome extension</div>
<h1>Your bookmarks, <em>calm and organised.</em></h1>
<p class="lead">Bookmark+ turns every new tab into a calm, tidy dashboard of the sites you actually use. Categories, search, pins and projects, with everything kept on your device.</p>
<div class="pills"><span class="pill a">Free</span><span class="pill a">Your data stays on your device</span><span class="pill">No account</span></div>
<!-- TODO: replace with the Chrome Web Store listing URL once published -->
<div class="btns"><a class="btn p" href="#" aria-disabled="true">Add to Chrome: coming soon</a><a class="btn t" href="/bookmark-plus/privacy/">Read the privacy policy &rarr;</a></div>
<p style="font-size:14px;color:var(--muted);margin-top:14px">Chrome Web Store link: <span class="placeholder">[CHROME STORE URL TBC]</span></p></div>
<figure class="hero-shot">{pic("dashboard-light", ALT_LIGHT, loading="eager")}<figcaption>Sample bookmarks shown.</figcaption></figure></div>
<hr>
<div class="wrap sec"><div class="label">What it does</div><h2>Everything in one calm place.</h2>
<div class="cols">
<div class="col"><span class="n">01</span><h3>Organise</h3><p>Group bookmarks into colour-coded categories laid out in columns. Pin your must-have sites and let Favourites show your most used.</p></div>
<div class="col"><span class="n">02</span><h3>Find fast</h3><p>Search as you type across names, sites and projects. Press <kbd>/</kbd> to jump to search, or Enter to search the web with your own default search engine.</p></div>
<div class="col"><span class="n">03</span><h3>Save projects</h3><p>Save the current page, or all your open tabs, into a project with <kbd>Alt+Shift+B</kbd>, then open the whole project again later.</p></div>
</div>
<ul class="checks"><li>Import your Chrome bookmarks in one step; Bookmark+ only reads them</li><li>Back up and restore with a JSON file</li><li>Light and dark mode, with six colour themes</li><li>Undo for deletes and imports</li></ul></div>
<hr>
<div class="wrap sec"><div class="label">Private by design</div><h2>Your bookmarks never leave your device.</h2>
<p class="lead" style="margin-bottom:24px">Bookmark+ has no account, no analytics, no advertising and no servers. Data is kept in Chrome's local extension storage only. Because nothing is sent anywhere, bookmarks do not sync between computers on their own: use Download backup on one and Import on the other.</p>
<div class="btns"><a class="btn p" href="/bookmark-plus/privacy/">Privacy policy</a><a class="btn t" href="/labs/bookmark-plus/">See the builder view in Labs &rarr;</a></div></div>
</main>"""
page("/bookmark-plus/index.html", "Bookmark+ | KatachiLabs", "Bookmark+ is a calm, private bookmark dashboard for Chrome's new tab. Free, with everything stored on your device.", "light", "", lp,
     extra='<link rel="canonical" href="https://katachilabs.uk/bookmark-plus/">')


notfound = '''<main id="main"><div class="wrap"><div class="hero sm"><div class="kicker">404</div><h1>Page not <em>found.</em></h1>
<p class="lead">That page does not exist (yet). Try the home page, Labs or Bookmark+.</p>
<div class="btns"><a class="btn p" href="/">Home</a><a class="btn t" href="/labs/">Labs</a><a class="btn t" href="/bookmark-plus/">Bookmark+</a></div></div></div></main>'''
page("/404.html", "Page not found | KatachiLabs", "", "light", "", notfound)

# ---------------- LABS (Midnight Studio) ----------------
labs = f'''<main id="main">
<div class="hero"><div class="wrap"><div>
<div class="eyebrow mono">KatachiLabs / Labs</div>
<h1>Build calm things. <span>Build them together.</span></h1>
<p class="lead">Labs is where we build in the open: the apps we are making, how they work, and a community of people who like to build and learn.</p>
<div class="btns"><a class="btn p" href="/labs/bookmark-plus/">Meet Bookmark+ &rarr;</a><a class="btn g" href="#community">Join the community</a></div></div>
<div class="term" aria-hidden="true"><div class="bar"><i></i><i></i><i></i><span class="mono" style="margin-left:8px">principles.md</span></div>
<pre><span class="c"># how we build</span>
<span class="k">data</span>      = <span class="v">"stays on your device"</span>
<span class="k">tracking</span>  = <span class="v">none</span>
<span class="k">accounts</span>  = <span class="v">not required</span>
<span class="k">roadmap</span>   = <span class="v">shared with the community</span>
<span class="k">status</span>    = <span class="v">calm, on purpose</span></pre></div></div></div>

<section><div class="wrap"><div class="sec-label mono">01 / Projects</div><h2>What we are building</h2>
<div class="product"><div class="txt"><div class="tags"><span class="tag a">Free</span><span class="tag">Coming soon</span><span class="tag">Chrome</span></div>
<h3>Bookmark+</h3><p>A new-tab dashboard for your bookmarks. Categories, search, pins and projects, all kept on your device. No account, no tracking.</p>
<div class="btns"><a class="btn p" href="/labs/bookmark-plus/">Project page</a><a class="btn g" href="/bookmark-plus/privacy/">Privacy policy</a></div></div>
<div class="vis">{pic("dashboard-dark", ALT_DARK, small=640, sizes="(max-width:900px) 100vw, 520px")}</div></div></div></section>

<section style="padding-top:0"><div class="wrap"><div class="sec-label mono">02 / Build log</div><h2>Notes from the bench</h2>
<p class="sub">A short, honest log of what we ship and learn. Full posts will land here as we write them.</p>
<div class="log">
<div class="entry"><div class="d">24 Oct 2026</div><div><h3>Bookmark+ privacy policy published</h3><p>The policy states plainly that data stays on your device in local storage, with no account and no tracking. <a class="inline" href="/bookmark-plus/privacy/" style="color:var(--accent);text-decoration:underline">Read it</a>.</p></div></div>
<div class="entry next"><div class="d">Next</div><div><h3>Bookmark+ on the Chrome Web Store</h3><p>In progress. Date to be confirmed.</p></div></div>
<div class="entry next"><div class="d">Later</div><div><h3><span class="placeholder">[BUILD LOG ENTRY TBC]</span></h3><p>Posts and write-ups to be added by David.</p></div></div>
</div></div></section>

<section style="padding-top:0"><div class="wrap"><div class="sec-label mono">03 / Approach</div><h2>How we work</h2>
<div class="grid3">
<div class="pillar"><div class="ico">{ICO_SHIELD}</div><h3>Privacy by design</h3><p>Privacy is part of the first sketch, not a patch at the end. We collect as little as possible, and with Bookmark+ nothing at all.</p></div>
<div class="pillar"><div class="ico">{ICO_PEOPLE}</div><h3>Built in the open</h3><p>Ideas, progress and mistakes are shared with a community of people who like to build and learn together.</p></div>
<div class="pillar"><div class="ico">{ICO_CODE}</div><h3>Small and focused</h3><p>Each app does a few things well, and works without an account or a server.</p></div>
</div></div></section>

<div class="cta" id="community"><div class="wrap"><div class="box"><div><h2>Build something with us.</h2><p>Curious, skilled or just getting started? Say hello and tell us what you would like to see. Community channel: <span class="placeholder">[COMMUNITY LINK TBC]</span></p></div><a class="btn p" href="/contact/">Say hello</a></div></div></div>
</main>'''
page("/labs/index.html", "Labs | KatachiLabs", "KatachiLabs Labs: build in the open, the Bookmark+ project and the builder community.", "dark", "labs", labs)

bp = f"""<main id="main">
<div class="hero one"><div class="wrap"><div>
<div class="crumb"><a href="/labs/">Labs</a> / Bookmark+</div>
<div class="eyebrow mono">Chrome extension</div>
<h1>Your bookmarks, <span>calm and organised.</span></h1>
<p class="lead">Bookmark+ is a calm bookmark dashboard for your new tab: categories, search, pins and projects.</p>
<div class="tags"><span class="tag a">Free</span><span class="tag a">Your data stays on your device</span></div>
<!-- TODO: replace with the Chrome Web Store listing URL once published -->
<div class="btns"><a class="btn p" href="#" aria-disabled="true">Add to Chrome: coming soon</a><a class="btn g" href="/bookmark-plus/privacy/">Privacy policy</a></div>
<p class="sub" style="font-size:14px">Chrome Web Store link: <span class="placeholder">[CHROME STORE URL TBC]</span></p></div>
<figure class="hero-img">{pic("dashboard-dark", ALT_DARK, loading="eager")}<figcaption class="mono">Sample bookmarks shown.</figcaption></figure></div></div>

<section><div class="wrap"><div class="sec-label mono">01 / Features</div><h2>What it does</h2>
<div class="grid2">
<div class="pillar"><h3>Organise</h3><ul><li>Organise bookmarks into categories and columns</li><li>Pinned, Favourites and Projects</li><li>Light and dark mode, with six colour themes</li></ul></div>
<div class="pillar"><h3>Find and save</h3><ul><li>Fast search (press <kbd>/</kbd>), with your own default search engine for the web</li><li>Save the current page, or all open tabs, with <kbd>Alt+Shift+B</kbd></li><li>Import your Chrome bookmarks, back up and restore with a JSON file</li></ul></div>
</div></div></section>

<section style="padding-top:0"><div class="wrap"><div class="sec-label mono">02 / Gallery</div><h2>A closer look</h2>
<p class="sub">Click an image to open it full size. All screenshots use sample bookmarks.</p>
<div class="gallery">
<figure><a href="{IMG}/dashboard-light-1280.png">{pic("dashboard-light", ALT_LIGHT, sizes="(max-width:900px) 100vw, 540px")}</a><figcaption>Light mode</figcaption></figure>
<figure><a href="{IMG}/search-1280.png">{pic("search", ALT_SEARCH, sizes="(max-width:900px) 100vw, 540px")}</a><figcaption>Search as you type</figcaption></figure>
<figure><a href="{IMG}/popup-1280.png">{pic("popup", ALT_POPUP, sizes="(max-width:900px) 100vw, 540px")}</a><figcaption>Save any page in one click</figcaption></figure>
<figure><a href="{IMG}/settings-1280.png">{pic("settings", ALT_SETTINGS, sizes="(max-width:900px) 100vw, 540px")}</a><figcaption>Settings and themes</figcaption></figure>
</div></div></section>

<section style="padding-top:0"><div class="wrap"><div class="sec-label mono">03 / Privacy</div><h2>Private by design</h2>
<div class="grid2">
<div class="pillar"><div class="ico">{ICO_SHIELD}</div><h3>Local storage only</h3><p>Everything you save stays on your device in Chrome's extension storage. No account, no tracking, no servers. Bookmarks do not sync between computers on their own; move them with a backup file.</p></div>
<div class="pillar"><div class="ico">{ICO_CASE}</div><h3>Read the details</h3><p>The privacy policy lists exactly what Bookmark+ handles and why each permission is needed. <a class="inline" href="/bookmark-plus/privacy/">Read the privacy policy</a>.</p></div>
</div></div></section>

<div class="cta"><div class="wrap"><div class="box"><div><h2>Tell us what you think.</h2><p>Ideas, bugs or wishes for Bookmark+ are welcome. Guide, help and feedback pages will follow.</p></div><a class="btn p" href="/contact/">Get in touch</a></div></div></div>
</main>"""
page("/labs/bookmark-plus/index.html", "Bookmark+ | KatachiLabs Labs", "Bookmark+: a calm, private bookmark dashboard for Chrome's new tab.", "dark", "labs", bp)
print("built")
