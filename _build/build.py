#!/usr/bin/env python3
"""Builds every HTML page of the WHPC MENA website.

The header, navigation, footer and cookie banner are written once here and
applied to every page, so a change to the menu only has to be made in one place.

    python3 _build/build.py

Page content lives in the PAGES list below. You can also edit the generated
.html files directly; just remember that re-running this script overwrites them.
"""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- settings ---
SITE_URL = "https://whpcmena.org"          # used for canonical links and sitemap.xml
EMAIL = "marhaba@whpcmena.org"
LINKEDIN = "https://www.linkedin.com/company/whpc-mena-middle-east-north-africa/"
WHPC_GLOBAL = "https://womeninhpc.org/"
LAST_UPDATED = "29 September 2026"         # shown on the privacy policy

# Top navigation: (label, page slug, [(sub-page label, slug), ...])
NAV = [
    ("About", "about", [("Mission", "about-mission"), ("Our team", "about-team"), ("Partners", "about-partners")]),
    ("Events", "events", [("Upcoming", "events-upcoming"), ("Past events", "events-past")]),
    ("Community", "community", [("Institutions", "community-institutions"), ("Resources", "community-resources"), ("Jobs", "community-jobs")]),
    ("Get involved", "get-involved", [("Join the list", "get-involved-join"), ("Mentorship", "get-involved-mentorship"), ("Volunteer", "get-involved-volunteer")]),
    ("News", "news", []),
    ("Contact", "contact", []),
]


def href(slug):
    return "index.html" if slug == "index" else f"{slug}.html"


def section_of(slug):
    if slug.startswith("event-"):          # individual event pages live under Events
        slug = "events-past"
    for label, top, subs in NAV:
        if slug == top or slug in [s for _, s in subs]:
            return label, top, subs
    return None


def header(slug):
    sec = section_of(slug)
    items = []
    for label, top, subs in NAV:
        attrs = ""
        if slug == top:
            attrs = ' aria-current="page"'
        elif sec and sec[1] == top:
            attrs = ' class="is-section"'
        sub_html = ""
        if subs:
            sub_items = "".join(
                f'<li><a href="{href(s)}"{" aria-current=" + chr(34) + "page" + chr(34) if s == slug else ""}>{l}</a></li>'
                for l, s in subs)
            sub_html = f'<ul class="submenu">{sub_items}</ul>'
        cls = ' class="has-sub"' if subs else ""
        items.append(f'<li{cls}><a href="{href(top)}"{attrs}>{label}</a>{sub_html}</li>')
    return f"""<a class="skip-link" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap">
  <a href="get-involved.html">Get involved</a>
  <a href="get-involved-join.html">Mailing list</a>
  <a href="{LINKEDIN}">LinkedIn</a>
  <a href="contact.html">Contact</a>
</div></div>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html">
      <picture><source srcset="assets/img/logo-header.webp" type="image/webp"><img src="assets/img/logo-header.png" alt="WHPC MENA" width="187" height="112"></picture>
      <span class="brand-sub">Women in HPC · Middle East &amp; North Africa</span>
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="main-nav">Menu</button>
    <nav class="main-nav" id="main-nav" aria-label="Main">
      <ul>{''.join(items)}</ul>
    </nav>
  </div>
</header>"""


def page_head(slug, eyebrow, h1, lede):
    sec = section_of(slug)
    crumbs = ""
    if sec and sec[1] != slug:
        crumbs = f'<p class="crumbs"><a href="{href(sec[1])}">{sec[0]}</a> / {escape(h1)}</p>'
    lede_html = f'<p class="lede">{lede}</p>' if lede else ""
    head = f"""<section class="page-head">
  <div class="wrap">
    {crumbs}
    <p class="eyebrow">{eyebrow}</p>
    <h1>{h1}</h1>
    {lede_html}
  </div>
</section>"""
    if sec and sec[2]:
        cur_top = ' aria-current="page"' if slug == sec[1] else ""
        links = [f'<li><a href="{href(sec[1])}"{cur_top}>Overview</a></li>']
        for label, s in sec[2]:
            cur = ' aria-current="page"' if s == slug else ""
            links.append(f'<li><a href="{href(s)}"{cur}>{label}</a></li>')
        head += f"""
<nav class="subnav" aria-label="{sec[0]} pages"><div class="wrap"><ul>{''.join(links)}</ul></div></nav>"""
    return head


def footer():
    return f"""<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="stack">
      <a class="footer-logo" href="index.html"><picture><source srcset="assets/img/logo-white.webp" type="image/webp"><img src="assets/img/logo-white.png" alt="WHPC MENA" width="187" height="112"></picture></a>
      <p>The official Middle East &amp; North Africa affiliate of <a href="{WHPC_GLOBAL}">Women in HPC</a>, supporting women in high-performance and advanced computing across the region.</p>
    </div>
    <div>
      <h2>Quick links</h2>
      <ul>
        <li><a href="about.html">About</a></li>
        <li><a href="events.html">Events</a></li>
        <li><a href="community.html">Community</a></li>
        <li><a href="get-involved.html">Get involved</a></li>
        <li><a href="news.html">News</a></li>
      </ul>
    </div>
    <div>
      <h2>Policies</h2>
      <ul>
        <li><a href="code-of-conduct.html">Code of conduct</a></li>
        <li><a href="privacy.html">Privacy policy</a></li>
        <li><button class="linkbtn" type="button" data-open-consent>Cookie settings</button></li>
      </ul>
    </div>
    <div class="stack">
      <h2 style="margin-bottom:0">Stay in touch</h2>
      <form class="signup" id="footer-signup" data-mailto data-subject="Please add me to the WHPC MENA mailing list">
        <label class="skip-link" for="footer-email">Email address</label>
        <input id="footer-email" name="email" data-label="Email" type="email" placeholder="you@example.org" required autocomplete="email">
        <button class="btn btn-sm" type="submit">Join the list</button>
        <p class="form-status" role="status" aria-live="polite" style="flex-basis:100%"></p>
      </form>
      <p><a href="mailto:{EMAIL}">{EMAIL}</a><br><a href="{LINKEDIN}">WHPC MENA on LinkedIn</a></p>
    </div>
  </div>
  <div class="footer-bottom">
    <div class="wrap">
      <span>© <span data-year>2026</span> WHPC MENA</span>
      <nav aria-label="Affiliation"><a href="{WHPC_GLOBAL}">Women in HPC (global)</a></nav>
    </div>
  </div>
</footer>
<div class="consent" id="consent" role="dialog" aria-label="Analytics cookies" hidden>
  <div class="consent-inner">
    <p>We use Google Analytics to see which pages are read and which countries visitors come from. It sets cookies only if you allow it. <a href="privacy.html">Privacy policy</a></p>
    <div class="actions">
      <button class="btn btn-ghost btn-sm" type="button" data-consent="decline">Decline</button>
      <button class="btn btn-sm" type="button" data-consent="accept">Allow analytics</button>
    </div>
  </div>
</div>"""


def layout(p):
    title = "WHPC MENA — Women in HPC, Middle East & North Africa" if p["slug"] == "index" else f"{p['title']} · WHPC MENA"
    canonical = f"{SITE_URL}/" if p["slug"] == "index" else f"{SITE_URL}/{href(p['slug'])}"
    robots = '\n  <meta name="robots" content="noindex">' if p.get("noindex") else ""
    top = p.get("top")
    if top is None:
        top = page_head(p["slug"], p["eyebrow"], p["h1"], p.get("lede", ""))
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(p['desc'])}">{robots}
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="WHPC MENA">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(p['desc'])}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE_URL}/assets/img/og-banner.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#3179b3">
  <link rel="icon" href="assets/img/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="icon" href="assets/img/favicon-48.png" sizes="48x48" type="image/png">
  <link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
  <link rel="preload" href="assets/fonts/nunito-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="assets/fonts/nunito-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
{header(p['slug'])}
<main id="main">
{top}
{p['body']}
</main>
{footer()}
<script src="assets/js/site.js" defer></script>
</body>
</html>
"""


# ------------------------------------------------------------ reusable bits ---
def example_tag(text="Example — replace"):
    return f'<span class="tag tag-example">{text}</span>'


def mail_note():
    return (f'<p class="hint muted">Sending opens your email app with a message to '
            f'<strong>{EMAIL}</strong>, filled in from this form. Nothing is stored on this website.</p>')


def join_band():
    return """<section class="band">
  <div class="wrap">
    <div class="stack" style="gap:.5rem">
      <h2>Hear about events and opportunities first</h2>
      <p>Join the WHPC MENA mailing list for event announcements, calls for speakers, scholarships and jobs across the region.</p>
    </div>
    <a class="btn" href="get-involved-join.html">Join the mailing list</a>
  </div>
</section>"""


def overview_cards(cards):
    items = "".join(
        f'<a class="card" href="{href(s)}"><h3>{t}</h3><p>{d}</p><span class="more">{m} →</span></a>'
        for t, s, d, m in cards)
    return f'<div class="grid">{items}</div>'


def person_link(name, url):
    return f'<a href="{url}">{name}</a>'


# ---------------------------------------------------------------- content ---
# Founding team (from the 2025 annual report). Add roles or institutions here.
TEAM = [
    ("Mennatallah Samier Saleh", "MS", "https://www.linkedin.com/in/mennatallah-samier-saleh-53087aa9/"),
    ("Safae Bourhnane", "SB", "https://www.linkedin.com/in/safae-bourhnane-3261a4b5/"),
    ("Hadeel Albahar", "HA", "https://www.linkedin.com/in/hadeelalbahar/"),
]

# Founding institutions: (name, detail line, country, website)
FOUNDERS = [
    ("NYU Abu Dhabi", "New York University Abu Dhabi", "United Arab Emirates", "https://nyuad.nyu.edu/"),
    ("MoroccoHPC", "with UM6P, Mohammed VI Polytechnic University", "Morocco", "https://www.linkedin.com/company/moroccohpc/"),
    ("Kuwait University", "", "Kuwait", "https://ku.edu.kw/"),
    ("KAUST", "King Abdullah University of Science and Technology", "Saudi Arabia", "https://www.kaust.edu.sa/"),
]

COUNTRIES = ["United Arab Emirates", "Morocco", "Kuwait", "Saudi Arabia", "Tunisia", "Algeria", "Egypt"]

PANEL = [
    ("Anan Ibrahim", "https://www.linkedin.com/in/anan-ibrahim-x/",
     "Brings HPC closer to real-world scientific needs, from bioinformatics to global R&amp;D, bridging the gap between researchers and computing platforms."),
    ("Huda Ibeid", "https://www.linkedin.com/in/huda-ibeid-30a6082b/",
     "Optimised applications on one of the world's first exascale supercomputers, and now works on data centre performance at NVIDIA."),
    ("Nessrine Aloulou", "https://www.linkedin.com/in/nessrine-aloulou/",
     "Builds next-generation HPC systems and actively supports students and the growing HPC community in Tunisia."),
]

MENNA = person_link("Mennatallah Samier Saleh", TEAM[0][2])
SAFAE = person_link("Safae Bourhnane", TEAM[1][2])

# Past events, newest first:
# (slug, day, month, year, title, kind line, card summary)
EVENTS = [
    ("event-2026-06-isc", "22", "Jun", "2026", "ISC High Performance 2026", "Conference · Hamburg, Germany · 22–26 June",
     "Our representatives shared the WHPC MENA story in several sessions and connected with Women in HPC leaders from around the world."),
    ("event-2026-04-her-hpc-journey", "21", "Apr", "2026", "Her HPC Journey: the official kick-off of WHPC MENA", "Webinar · Online · 21 April",
     "Our first webinar: three women in HPC on how they entered the field, what the work is really like, and the advice they wish they'd had."),
    ("event-2026-01-sca-hpcasia", "26", "Jan", "2026", "SCA/HPCAsia 2026", "Conference · Osaka, Japan · 26–29 January",
     "WHPC MENA's first international appearance, building connections for the region within the global Women in HPC network."),
]


def event_card(ev, cls=""):
    slug, day, mon, year, title, kind, summary = ev
    return f"""<article class="card event {cls}">
  <div class="datebox"><span class="m">{mon}</span><span class="d">{day}</span><span class="y">{year}</span></div>
  <div class="stack" style="gap:.4rem">
    <h3><a href="{href(slug)}">{title}</a></h3>
    <p class="meta">{kind}</p>
    <p>{summary}</p>
  </div>
</article>"""


def no_upcoming(compact=False):
    extra = "" if compact else '<p class="muted">We announce events on LinkedIn and to our mailing list first.</p>'
    return f"""<div class="empty">
  <h3>Next event to be announced</h3>
  {extra}
  <div class="actions"><a class="btn btn-ghost btn-sm" href="get-involved-join.html">Join the mailing list</a><a class="btn btn-ghost btn-sm" href="{LINKEDIN}">Follow on LinkedIn</a></div>
</div>"""


# News, newest first: (anchor id, date label, category, headline, html body, related page or "")
# Date labels are empty until the original post dates are confirmed.
NEWS = [
    ("nine-months", "", "Milestone", "From a conversation at ISC 2025 to a regional network",
     f"""<p>What began as a conversation at ISC 2025 has grown into the first official Women in HPC affiliate for the Middle East and North Africa. Our mission from the start: build community, highlight female role models and advance diversity in HPC across the region.</p>
<h3>Building the foundation</h3>
<ul>
  <li><strong>Official recognition.</strong> We submitted our application on 7 November 2025, and Women in HPC approved it on 5 December 2025.</li>
  <li><strong>Founding institutions.</strong> New York University Abu Dhabi, MoroccoHPC, Kuwait University and KAUST.</li>
  <li><strong>Regional reach.</strong> From four founding countries to a community across seven: the UAE, Morocco, Kuwait, Saudi Arabia, Tunisia, Algeria and Egypt.</li>
  <li><strong>Community.</strong> More than 50 mailing list subscribers and 300 LinkedIn followers.</li>
</ul>
<h3>Highlights</h3>
<ul>
  <li>Our kick-off webinar, <a href="event-2026-04-her-hpc-journey.html">Her HPC Journey</a>, in April 2026.</li>
  <li>Representing the region at <a href="event-2026-01-sca-hpcasia.html">SCA/HPCAsia 2026</a> and delivering sessions at <a href="event-2026-06-isc.html">ISC High Performance 2026</a> in Hamburg.</li>
  <li>A complete visual identity, interactive regional maps and presentation materials.</li>
</ul>
<p>Thank you to our founding team, {person_link(*TEAM[0][::2])}, {person_link(*TEAM[1][::2])} and {person_link(*TEAM[2][::2])}, to our speakers, and to everyone who has joined us so far.</p>""", ""),
    ("isc-2026", "", "Event", "A week at ISC High Performance 2026",
     f"""<p>Our representatives {MENNA} and {SAFAE} spent an inspiring week at ISC High Performance 2026 in Hamburg, sharing the WHPC MENA story in several sessions and joining deep-dive workshops.</p>
<p>The week was about connection: exchanging experiences with other Women in HPC leaders and meeting women in HPC from the MENA region and around the world. We came home grateful, with new ideas and a stronger commitment to building the future of HPC in our region.</p>""",
     "event-2026-06-isc"),
    ("kick-off-webinar", "", "Announcement", "Announcing our first webinar: Her HPC Journey",
     """<p>After weeks of conversations and planning, we invited the community to our very first webinar, <em>Her HPC Journey</em>, the official kick-off of WHPC MENA, on Tuesday 21 April 2026.</p>
<p>The session is about real journeys into HPC, with all the twists, challenges and breakthroughs along the way. Whether you are just discovering HPC, already in the field, or simply curious, it is for you. It is also the beginning of a community for women in HPC across the MENA region.</p>""",
     "event-2026-04-her-hpc-journey"),
    ("sca-hpcasia-2026", "", "Event", "WHPC MENA at SCA/HPCAsia 2026",
     f"""<p>WHPC MENA was delighted to take part in SCA/HPCAsia 2026, which brings together researchers, industry leaders and practitioners shaping the future of HPC and AI.</p>
<p>{MENNA} represented us, engaging with the international community and raising the visibility of the MENA region within the global Women in HPC network. The conversations there are shaping our upcoming activities, events and initiatives in the region.</p>""",
     "event-2026-01-sca-hpcasia"),
]

TIMELINE = [
    ("2025-06", "June 2025", "The idea", "WHPC MENA begins with a conversation at ISC 2025 in Hamburg."),
    ("2025-11-07", "7 Nov 2025", "Application", "We submit our formal affiliate application to Women in HPC."),
    ("2025-12-05", "5 Dec 2025", "Approval", "Women in HPC approves WHPC MENA as its affiliate for the Middle East and North Africa."),
    ("2026-01-07", "7 Jan 2026", "Launch", "Our visual identity and LinkedIn page go live."),
    ("2026-01-26", "Jan 2026", "First conference", "We represent the region at SCA/HPCAsia 2026 in Osaka."),
    ("2026-04-21", "21 Apr 2026", "Kick-off webinar", "Her HPC Journey, our first public event."),
    ("2026-06-22", "Jun 2026", "ISC 2026", "We deliver sessions at ISC High Performance in Hamburg."),
]


def timeline():
    items = "".join(
        f'<li><time datetime="{dt}">{label}</time><div><strong>{title}</strong><p>{text}</p></div></li>'
        for dt, label, title, text in TIMELINE)
    return f'<ol class="timeline">{items}</ol>'


def founder_cards():
    out = ""
    for name, detail, country, url in FOUNDERS:
        det = f"<p>{detail}</p>" if detail else ""
        out += f'<article class="card"><span class="tag">Founding institution</span><h3><a href="{url}">{name}</a></h3>{det}<p class="meta">{country}</p></article>'
    return f'<div class="grid">{out}</div>'


def country_chips():
    return '<ul class="chips">' + "".join(f"<li>{c}</li>" for c in COUNTRIES) + "</ul>"


# -------------------------------------------------------------------- pages ---
PAGES = []


def page(**kw):
    PAGES.append(kw)


def community_tiles():
    tiles = [
        ("Mentorship", "get-involved-mentorship", "Find a mentor, or share your experience as one."),
        ("Resources", "community-resources", "Learning materials, conferences and communities in HPC."),
        ("Jobs", "community-jobs", "HPC and research computing openings in the region."),
        ("Volunteer", "get-involved-volunteer", "Help run events, content and outreach in your country."),
    ]
    return '<div class="grid">' + "".join(
        f'<a class="card tile" href="{href(s)}"><div class="tile-art" aria-hidden="true"></div><div class="tile-body"><h3>{t}</h3><p>{d}</p><span class="more">Read more →</span></div></a>'
        for t, s, d in tiles) + "</div>"


def supporters_strip():
    return '<div class="supporters">' + "".join(
        f'<a class="supporter" href="{url}"><strong>{name}</strong><span>{country}</span></a>'
        for name, _, country, url in FOUNDERS) + "</div>"


def news_cards(n=3):
    out = ""
    for nid, date, cat, head, body_, rel in NEWS[:n]:
        first = body_.split("</p>")[0].replace("<p>", "")
        import re as _re
        text = _re.sub(r"<[^>]+>", "", first)
        if len(text) > 170:
            text = text[:text.rfind(" ", 0, 165)] + "…"
        meta = " · ".join(x for x in (cat, date) if x)
        out += f'<a class="card news-card" href="news.html#{nid}"><div class="tile-art" aria-hidden="true"></div><div class="tile-body"><p class="meta">{meta}</p><h3>{head}</h3><p>{text}</p><span class="more">Read more →</span></div></a>'
    return f'<div class="grid-3">{out}</div>'


latest = NEWS[0]

# Home ------------------------------------------------------------------------
page(slug="index", title="Home",
     desc="WHPC MENA supports and amplifies women in high-performance computing across the Middle East and North Africa through networking, mentorship, events and outreach.",
     top="""<section class="banner"><img src="assets/img/banner.webp" width="1584" height="396" alt="Women in High-Performance Computing, Middle East and North Africa Region. مرحباً (Welcome)"></section>""",
     body=f"""<section class="section">
  <div class="wrap welcome">
    <div class="stack">
            <h1 class="section-title">Welcome to WHPC MENA</h1>
      <p class="lede" style="color:var(--ink)">We are the official Women in HPC affiliate for the Middle East and North Africa. We connect women working in high-performance computing, advanced computing and related fields, highlight female role models, and help the next generation into the field.</p>
      <p class="muted">Founded by NYU Abu Dhabi, MoroccoHPC, Kuwait University and KAUST, and open to everyone who wants a more inclusive computing community in the region.</p>
      <div class="actions"><a class="btn" href="about.html">Read more about us</a><a class="btn btn-ghost" href="get-involved-join.html">Join the mailing list</a></div>
    </div>
    <div class="region-card">
      <h3>Our community across the region</h3>
      {country_chips()}
      <dl class="stats">
        <div><dt>Affiliate since</dt><dd>Dec 2025</dd></div>
        <div><dt>Countries</dt><dd>7</dd></div>
        <div><dt>Founding institutions</dt><dd>4</dd></div>
        <div><dt>LinkedIn followers</dt><dd>300+</dd></div>
      </dl>
    </div>
  </div>
</section>
<section class="section section-tint">
  <div class="wrap">
    <div class="section-head"><h2 class="section-title">Events</h2><a class="more" href="events.html">All events →</a></div>
    <div class="stack">
      <div class="grid-2">
        {event_card(EVENTS[0])}
        {event_card(EVENTS[1])}
      </div>
      <div class="callout" style="background:#fff;display:flex;flex-wrap:wrap;gap:12px 24px;align-items:center;justify-content:space-between"><p><strong>Next event to be announced.</strong> Join the mailing list or follow us on LinkedIn to hear first.</p><div class="actions"><a class="btn btn-sm" href="get-involved-join.html">Join the mailing list</a><a class="btn btn-ghost btn-sm" href="{LINKEDIN}">Follow on LinkedIn</a></div></div>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head"><h2 class="section-title">Latest news</h2><a class="more" href="news.html">All news →</a></div>
    {news_cards(3)}
  </div>
</section>
<section class="section section-tint">
  <div class="wrap">
    <div class="section-head"><h2 class="section-title">Community</h2><a class="more" href="community.html">Explore the community →</a></div>
    {community_tiles()}
  </div>
</section>
<section class="section">
  <div class="wrap stack-lg">
    <div class="center stack" style="align-items:center;gap:.75rem"><h2 class="section-title">Founding institutions</h2><p class="muted">WHPC MENA is a collaboration between four institutions in four countries.</p></div>
    {supporters_strip()}
    <p class="center muted">An affiliate of <a href="{WHPC_GLOBAL}">Women in HPC</a>, the global organisation working to diversify high-performance computing.</p>
  </div>
</section>
{join_band()}""")

# About -----------------------------------------------------------------------
page(slug="about", title="About", eyebrow="About", h1="About WHPC MENA",
     desc="WHPC MENA is the official Middle East and North Africa affiliate of Women in HPC.",
     lede="WHPC MENA (Women in High Performance Computing – Middle East &amp; North Africa) is the official regional affiliate of the global Women in HPC initiative.",
     body=f"""<section class="section"><div class="wrap two-col">
  <div class="prose">
    <p>We are dedicated to closing the gender gap in high-performance computing (HPC) across the Middle East and North Africa. We support and amplify women in HPC, advanced computing and related fields through networking, knowledge sharing, mentorship and outreach, shaped for the MENA context.</p>
    <p>WHPC MENA is a collaboration between four founding institutions in four countries: NYU Abu Dhabi in the UAE, MoroccoHPC with UM6P in Morocco, Kuwait University, and KAUST in Saudi Arabia. Our community now reaches seven countries.</p>
    <p>We welcome everyone who is interested in HPC and in building a more inclusive and diverse computing ecosystem in the region.</p>
  </div>
  <aside class="callout aside"><p><strong>Affiliate of Women in HPC</strong></p><p>Approved by Women in HPC on 5 December 2025. <a href="{WHPC_GLOBAL}">Learn about Women in HPC →</a></p></aside>
</div></section>
<section class="section"><div class="wrap stack-lg">
  <div class="stack"><p class="eyebrow">Our story</p><h2>How we got here</h2></div>
  {timeline()}
</div></section>
<section class="section"><div class="wrap">
  {overview_cards([
      ("Mission", "about-mission", "What we are here to do and the values that guide us.", "Read our mission"),
      ("Our team", "about-team", "The founding team behind WHPC MENA.", "Meet the team"),
      ("Partners", "about-partners", "Our founding institutions and the network we belong to.", "See our partners"),
  ])}
</div></section>""")

page(slug="about-mission", title="Mission", eyebrow="About", h1="Our mission",
     desc="The mission, aims and values of WHPC MENA.",
     lede="To close the gender gap in high-performance computing across the Middle East and North Africa, and to build a more inclusive computing ecosystem in the region.",
     body="""<section class="section"><div class="wrap prose">
  <h2>Our values</h2>
  <p>Diversity, equity and inclusion.</p>
  <h2>What we work towards</h2>
  <ul>
    <li><strong>Visible role models.</strong> Highlight women in HPC across the region, so that students can see people like them in the field.</li>
    <li><strong>Mentorship.</strong> Connect people starting out with people who have been there, for advice, confidence and career direction.</li>
    <li><strong>Inclusive practice.</strong> Advocate for inclusive practices across the regional HPC ecosystem.</li>
    <li><strong>Community.</strong> Bring women in HPC together across countries, institutions and career stages, so no one works in isolation.</li>
  </ul>
  <h2>Who we serve</h2>
  <p>Students, researchers, engineers and practitioners, in academia and industry, across the Middle East and North Africa.</p>
  <h2>Why high-performance computing matters here</h2>
  <p>HPC is the use of supercomputers and large clusters to solve problems too big for a single machine: climate and weather models, energy research, genomics, materials design, and training large AI models. The fastest systems today work at exascale, around 10<sup>18</sup> calculations per second.</p>
  <p>Countries across the region are investing in computing facilities and research. Those systems need people to design, run and use them. We want women to be well represented among those people.</p>
  <h2>How we work</h2>
  <ul>
    <li>We are volunteer-run and open to everyone who shares our goals.</li>
    <li>We bring the programmes of Women in HPC to the region and adapt them to its languages, cultures and institutions.</li>
    <li>Everyone at our events and in our online spaces follows our <a href="code-of-conduct.html">code of conduct</a>.</li>
  </ul>
</div></section>""")

team_cards = "".join(
    f'<article class="card person"><span class="avatar">{ini}</span><div class="stack" style="gap:.25rem"><h3>{name}</h3><p>Founding team</p><a href="{url}">LinkedIn →</a></div></article>'
    for name, ini, url in TEAM)
page(slug="about-team", title="Our team", eyebrow="About", h1="Our team",
     desc="The founding team of WHPC MENA.",
     lede="WHPC MENA was founded and is run by volunteers from across the region.",
     body=f"""<section class="section"><div class="wrap stack-lg">
  <div class="stack"><h2>Founding team</h2><div class="grid">{team_cards}</div></div>
  <div class="callout"><p>Want to help run WHPC MENA? We're always glad to hear from new volunteers. <a href="get-involved-volunteer.html">Volunteer with us →</a></p></div>
</div></section>""")

page(slug="about-partners", title="Partners", eyebrow="About", h1="Partners and supporters",
     desc="WHPC MENA's founding institutions and affiliation with Women in HPC.",
     lede="WHPC MENA brings together institutions across the region that share our goals.",
     body=f"""<section class="section"><div class="wrap stack-lg">
  <div class="stack"><h2>Our affiliation</h2>
    <a class="card" href="{WHPC_GLOBAL}" style="max-width:560px"><span class="tag">Parent organisation</span><h3>Women in HPC</h3><p>The global organisation working to improve diversity and inclusion in high-performance computing. WHPC MENA is its official regional affiliate.</p><span class="more">womeninhpc.org →</span></a>
  </div>
  <div class="stack"><h2>Founding institutions</h2>{founder_cards()}</div>
  <div class="callout"><p><strong>Partner with us</strong></p><p>Hosting an event, sponsoring a workshop or supporting our mentorship programme are all ways to work with us. <a href="contact.html">Get in touch →</a></p></div>
</div></section>""")

# Events ----------------------------------------------------------------------
past_cards = "".join(event_card(e) for e in EVENTS)
page(slug="events", title="Events", eyebrow="Events", h1="Events",
     desc="WHPC MENA webinars and conference appearances, with recaps.",
     lede="Webinars, talks and conference appearances for people working in or curious about HPC.",
     body=f"""<section class="section"><div class="wrap stack-lg">
  <div class="stack">
    <div class="section-head" style="margin-bottom:0"><h2>Coming up</h2><a href="events-upcoming.html">Upcoming events →</a></div>
    {no_upcoming()}
  </div>
  <div class="stack">
    <div class="section-head" style="margin-bottom:0"><h2>Past events</h2><a href="events-past.html">All past events →</a></div>
    {past_cards}
  </div>
</div></section>
{join_band()}""")

page(slug="events-upcoming", title="Upcoming events", eyebrow="Events", h1="Upcoming events",
     desc="Upcoming WHPC MENA events.",
     lede="Register for our next webinars, talks and meetups.",
     body=f"""<section class="section"><div class="wrap stack">
  {no_upcoming()}
  <div class="callout"><p><strong>Want to host or speak at an event?</strong> We welcome proposals for talks, workshops and panels. <a href="contact.html">Tell us your idea →</a></p></div>
</div></section>""")

page(slug="events-past", title="Past events", eyebrow="Events", h1="Past events",
     desc="Recaps from past WHPC MENA events and conference appearances.",
     lede="Recaps and highlights from our events, kept in one place.",
     body=f"""<section class="section"><div class="wrap stack">
  <h2 class="section-title" style="font-size:var(--step-2)">2026</h2>
  {past_cards}
</div></section>""")


def event_page(ev, lede, facts, prose, links=()):
    slug, _, _, _, title, _, _ = ev
    fact_html = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in facts)
    mats = ""
    if links:
        lis = "".join(f'<li><a href="{u}">{t}</a><span class="domain">{d}</span></li>' for t, u, d in links)
        mats = f'<div class="card"><h3>Links</h3><ul class="linklist">{lis}</ul></div>'
    page(slug=slug, title=title, eyebrow="Past event", h1=title, desc=lede, lede=lede,
         body=f"""<section class="section"><div class="wrap two-col">
  <div class="prose">{prose}</div>
  <aside class="aside stack">
    <dl class="spec">{fact_html}</dl>
    {mats}
    <a href="events-past.html">← All past events</a>
  </aside>
</div></section>""")


panel_html = "".join(
    f'<article class="card person"><span class="avatar">{"".join(w[0] for w in n.split()[:2])}</span><div class="stack" style="gap:.25rem"><h3><a href="{u}">{n}</a></h3><p>{b}</p></div></article>'
    for n, u, b in PANEL)

event_page(EVENTS[1],
    "Our first webinar and the official kick-off of WHPC MENA: real journeys into high-performance computing.",
    [("Date", "Tuesday 21 April 2026"), ("Time", "18:00 (GMT+1)"), ("Format", "Webinar, online")],
    f"""<p>Her HPC Journey was our very first webinar and the official kick-off of WHPC MENA. It was a session about stories: real journeys into HPC, with all the twists, challenges and breakthroughs that come with them.</p>
<h2>The panel</h2>
<div class="stack" style="gap:.75rem">{panel_html}</div>
<h2>What we talked about</h2>
<ul>
  <li>How each panellist found her way into HPC</li>
  <li>The realities of working in the field</li>
  <li>Lessons learned along the way</li>
  <li>The advice they wish they had been given earlier</li>
</ul>
<p>The session was open to everyone, from people just discovering HPC to those already working in it. It marked the beginning of a community for women in HPC across the MENA region.</p>""")

event_page(EVENTS[0],
    "WHPC MENA delivered sessions and connected with the global Women in HPC network at ISC High Performance 2026 in Hamburg.",
    [("Dates", "22–26 June 2026"), ("Location", "Hamburg, Germany"), ("Represented by", "Mennatallah Samier Saleh and Safae Bourhnane")],
    f"""<p>{MENNA} and {SAFAE} represented WHPC MENA at ISC High Performance 2026, Europe's major conference for high-performance computing.</p>
<h2>Highlights</h2>
<ul>
  <li>Shared the WHPC MENA story in several sessions.</li>
  <li>Attended deep-dive workshops.</li>
  <li>Exchanged experiences with Women in HPC leaders from other chapters and affiliates.</li>
  <li>Met women in HPC from the MENA region and around the world.</li>
</ul>
<p>We came home with new insights and a stronger commitment to building the future of HPC in our region. Thank you to everyone we met and to every leader who shared their expertise with us.</p>""",
    [("ISC High Performance", "https://isc-hpc.com/", "isc-hpc.com")])

event_page(EVENTS[2],
    "WHPC MENA's first international appearance, at SCA/HPCAsia 2026 in Osaka.",
    [("Dates", "26–29 January 2026"), ("Location", "Osaka, Japan"), ("Represented by", "Mennatallah Samier Saleh")],
    f"""<p>SCA/HPCAsia 2026 brought together researchers, industry leaders and practitioners shaping the future of high-performance computing and AI. Its technical programme bridged research and industry, and it gave space for community building and global knowledge exchange.</p>
<p>{MENNA} represented WHPC MENA, engaging with the international community, exchanging perspectives with researchers and practitioners, and raising the visibility of the MENA region within the global Women in HPC network.</p>
<p>The connections and ideas from the conference are shaping our activities, events and initiatives in the region.</p>""",
    [("SCA/HPCAsia 2026", "https://www.sca-hpcasia2026.jp/", "sca-hpcasia2026.jp")])

page(slug="event-template", title="Event recap template", eyebrow="Past event", h1="Event title",
     desc="Template for a past event recap page.", noindex=True,
     lede="Template: copy this page for each new event and replace the content.",
     body=f"""<section class="section"><div class="wrap two-col">
  <div class="prose">
    <p>{example_tag("Template — copy for each event")}</p>
    <h2>Recap</h2>
    <p>Two or three short paragraphs: who came, what was discussed and what came out of it.</p>
    <h2>Speakers</h2>
    <ul><li><strong>Speaker name</strong>, Role, Institution: “Talk title”</li></ul>
    <h2>Photos</h2>
    <div class="photos"><div class="logo-slot">Photo</div><div class="logo-slot">Photo</div><div class="logo-slot">Photo</div></div>
    <p class="muted">Ask for consent before publishing photos where people can be identified.</p>
  </div>
  <aside class="aside stack">
    <dl class="spec"><div><dt>Date</dt><dd>Date</dd></div><div><dt>Format</dt><dd>Format</dd></div><div><dt>Location</dt><dd>Venue, City</dd></div></dl>
    <a href="events-past.html">← All past events</a>
  </aside>
</div></section>""")

# Community -------------------------------------------------------------------
page(slug="community", title="Community", eyebrow="Community", h1="Community",
     desc="Institutions and countries in the WHPC MENA network, HPC resources and job opportunities.",
     lede="The people, places and resources that make up our community across the Middle East and North Africa.",
     body=f"""<section class="section"><div class="wrap stack-lg">
  {overview_cards([
      ("Institutions", "community-institutions", "Our founding institutions and the countries our community reaches.", "View institutions"),
      ("Resources", "community-resources", "Learning materials, conferences and communities for people in HPC.", "Browse resources"),
      ("Jobs", "community-jobs", "HPC and research computing openings shared with our community.", "See openings"),
  ])}
</div></section>
{join_band()}""")

page(slug="community-institutions", title="Institutions", eyebrow="Community", h1="Institutions",
     desc="WHPC MENA's founding institutions and the countries its community reaches.",
     lede="WHPC MENA started with four institutions in four countries. Our community now reaches seven.",
     body=f"""<section class="section"><div class="wrap stack-lg">
  <div class="stack"><h2>Founding institutions</h2>{founder_cards()}</div>
  <div class="stack"><h2>Where our community is</h2>{country_chips()}</div>
  <div class="callout"><p><strong>Is your institution active in HPC in the region?</strong></p><p>Let us know and we'll add it to this page. <a href="contact.html">Get listed →</a></p></div>
</div></section>""")

RESOURCES = [
    ("Community", [
        ("Women in HPC", "https://womeninhpc.org/", "womeninhpc.org", "The global organisation we are affiliated with: membership, mentoring, webinars and events."),
        ("ACM SIGHPC", "https://www.sighpc.org/", "sighpc.org", "The ACM special interest group on high-performance computing, with student programmes and awards."),
    ]),
    ("Learning", [
        ("HPC Carpentry", "https://www.hpc-carpentry.org/", "hpc-carpentry.org", "Free lessons that teach the basics of using a cluster, the command line and job schedulers."),
        ("TOP500", "https://top500.org/", "top500.org", "The twice-yearly ranking of the world's most powerful supercomputers, with system details."),
    ]),
    ("Conferences", [
        ("ISC High Performance", "https://isc-hpc.com/", "isc-hpc.com", "Europe's major HPC conference, held each year in Hamburg, Germany."),
        ("SupercomputingAsia (SCA)", "https://www.sc-asia.org/", "sc-asia.org", "The Asia-Pacific HPC conference series, held jointly with HPCAsia in 2026."),
        ("SC, the International Conference for High Performance Computing", "https://supercomputing.org/", "supercomputing.org", "The largest annual HPC conference, held each November in the United States."),
    ]),
]
res_html = ""
for group, items in RESOURCES:
    lis = "".join(f'<li><div><a href="{u}">{t}</a><p>{d}</p></div><span class="domain">{dom}</span></li>' for t, u, dom, d in items)
    res_html += f'<div class="stack"><h2>{group}</h2><ul class="linklist">{lis}</ul></div>'

page(slug="community-resources", title="Resources", eyebrow="Community", h1="Resources",
     desc="Learning materials, conferences and communities for people in high-performance computing.",
     lede="A short, curated list for getting started and staying connected in HPC. Suggestions are welcome.",
     body=f"""<section class="section"><div class="wrap stack-lg" style="max-width:860px;margin-inline:0 auto">
  {res_html}
  <div class="stack"><h2>In the region</h2>
    <div class="empty"><p class="muted">We're collecting training programmes, scholarships and events from across the Middle East and North Africa. Know of one we should list?</p><a class="btn btn-ghost btn-sm" href="contact.html">Suggest a resource</a></div>
  </div>
</div></section>""")

page(slug="community-jobs", title="Jobs", eyebrow="Community", h1="Jobs",
     desc="HPC and research computing job openings shared with the WHPC MENA community.",
     lede="Openings in HPC, research computing and related fields, shared with our community.",
     body=f"""<section class="section"><div class="wrap two-col">
  <div class="empty">
    <h3>No openings listed right now</h3>
    <p class="muted">We share roles, PhD positions and fellowships here and with our mailing list as we hear about them.</p>
    <a class="btn btn-ghost btn-sm" href="get-involved-join.html">Join the mailing list</a>
  </div>
  <aside class="aside card"><h3>Share a job</h3><p>Hiring for an HPC or research computing role in the region? Email us the title, organisation, location, closing date and a link to the full posting.</p>
    <div class="copybox"><code>{EMAIL}</code><button class="btn btn-ghost btn-sm" type="button" data-copy="{EMAIL}">Copy</button></div></aside>
</div></section>""")

# Get involved ----------------------------------------------------------------
page(slug="get-involved", title="Get involved", eyebrow="Get involved", h1="Get involved",
     desc="Join the WHPC MENA mailing list, take part in mentorship, or volunteer.",
     lede="There are several ways to take part, whatever your career stage.",
     body=f"""<section class="section"><div class="wrap">
  {overview_cards([
      ("Join the mailing list", "get-involved-join", "Event announcements, opportunities and news.", "Sign up"),
      ("Mentorship", "get-involved-mentorship", "Find a mentor, or share your experience as one.", "About mentorship"),
      ("Volunteer", "get-involved-volunteer", "Help organise events, create content or represent us in your country.", "Volunteer with us"),
  ])}
</div></section>""")


def interest_checks(name, options):
    return "".join(f'<label><input type="checkbox" name="{name}" value="{o}"> {o}</label>' for o in options)


page(slug="get-involved-join", title="Join the mailing list", eyebrow="Get involved", h1="Join the mailing list",
     desc="Sign up for WHPC MENA updates on events and opportunities.",
     lede="Get event announcements, calls for speakers, scholarships and jobs from across the region.",
     body=f"""<section class="section"><div class="wrap two-col">
  <form class="form card" id="join-form" data-mailto data-subject="Please add me to the WHPC MENA mailing list">
    <div class="row">
      <div class="field"><label for="join-name">Name</label><input id="join-name" name="name" data-label="Name" type="text" required autocomplete="name"></div>
      <div class="field"><label for="join-email">Email</label><input id="join-email" name="email" data-label="Email" type="email" required autocomplete="email"></div>
    </div>
    <div class="row">
      <div class="field"><label for="join-country">Country</label><input id="join-country" name="country" data-label="Country" type="text" autocomplete="country-name"></div>
      <div class="field"><label for="join-org">Organisation</label><input id="join-org" name="organisation" data-label="Organisation" type="text" autocomplete="organization"></div>
    </div>
    <fieldset class="fieldset" data-label="Interested in"><legend>I'm interested in</legend>
      <div class="checks">{interest_checks("interests", ["Events", "Mentorship", "Jobs and scholarships", "Volunteering"])}</div>
    </fieldset>
    {mail_note()}
    <div><button class="btn" type="submit">Send sign-up email</button></div>
    <p class="form-status" role="status" aria-live="polite"></p>
  </form>
  <aside class="aside stack">
    <div class="callout"><p>More than 50 people across the region already get our updates. You can ask to be removed at any time by emailing us. See our <a href="privacy.html">privacy policy</a>.</p></div>
    <p class="muted">Prefer to write yourself? Email <a href="mailto:{EMAIL}">{EMAIL}</a> with the subject “Join the list”.</p>
  </aside>
</div></section>""")

page(slug="get-involved-mentorship", title="Mentorship", eyebrow="Get involved", h1="Mentorship",
     desc="WHPC MENA mentorship: find a mentor or become one.",
     lede="Good mentors make a real difference, especially in a field where women are still few. We are preparing our first regional cycle of the Women in HPC mentorship programme.",
     body=f"""<section class="section"><div class="wrap two-col">
  <div class="prose">
    <h2>How it will work</h2>
    <p>We will match mentees with mentors working in HPC, research computing and related fields, taking career stage, interests and language into account. Pairs agree how often to meet, usually online.</p>
    <h3>Mentees</h3>
    <p>Students, early-career researchers and engineers, and anyone moving into HPC from another field.</p>
    <h3>Mentors</h3>
    <p>People with experience in HPC or advanced computing, in academia or industry, who can spare an hour or so a month. Mentors of any gender are welcome.</p>
    <p>Women in HPC also runs <a href="{WHPC_GLOBAL}">global mentoring programmes and webinars</a> that are open to our community.</p>
  </div>
  <form class="form card aside" id="mentor-form" data-mailto data-subject="WHPC MENA mentorship: registering interest">
    <h3>Register your interest</h3>
    <div class="field"><label for="m-name">Name</label><input id="m-name" name="name" data-label="Name" type="text" required autocomplete="name"></div>
    <div class="field"><label for="m-email">Email</label><input id="m-email" name="email" data-label="Email" type="email" required autocomplete="email"></div>
    <div class="field"><label for="m-role">I'd like to be a</label><select id="m-role" name="role" data-label="Role"><option>Mentee</option><option>Mentor</option><option>Either</option></select></div>
    <div class="field"><label for="m-area">Area of work or study</label><input id="m-area" name="area" data-label="Area" type="text"></div>
    {mail_note()}
    <div><button class="btn" type="submit">Send</button></div>
    <p class="form-status" role="status" aria-live="polite"></p>
  </form>
</div></section>""")

page(slug="get-involved-volunteer", title="Volunteer", eyebrow="Get involved", h1="Volunteer with us",
     desc="Volunteer with WHPC MENA: events, content, website and country ambassadors.",
     lede="WHPC MENA is run by volunteers. A few hours a month helps us reach more people.",
     body=f"""<section class="section"><div class="wrap stack-lg">
  <div class="grid">
    <div class="card"><h3>Events</h3><p>Plan webinars and meetups, invite speakers and run sessions on the day.</p></div>
    <div class="card"><h3>Content and social media</h3><p>Write event recaps and member stories, and help run our LinkedIn page.</p></div>
    <div class="card"><h3>Website</h3><p>Keep this site up to date with events, resources and jobs.</p></div>
    <div class="card"><h3>Country ambassadors</h3><p>Represent WHPC MENA at your university or in your country and connect local groups.</p></div>
  </div>
  <form class="form card" id="volunteer-form" data-mailto data-subject="Volunteering with WHPC MENA" style="max-width:720px">
    <h2 style="font-size:var(--step-2)">Tell us how you'd like to help</h2>
    <div class="row">
      <div class="field"><label for="v-name">Name</label><input id="v-name" name="name" data-label="Name" type="text" required autocomplete="name"></div>
      <div class="field"><label for="v-email">Email</label><input id="v-email" name="email" data-label="Email" type="email" required autocomplete="email"></div>
    </div>
    <fieldset class="fieldset" data-label="Areas"><legend>Areas</legend>
      <div class="checks">{interest_checks("areas", ["Events", "Content and social media", "Website", "Country ambassador"])}</div>
    </fieldset>
    <div class="field"><label for="v-note">Anything else we should know?</label><textarea id="v-note" name="note" data-label="Note"></textarea></div>
    {mail_note()}
    <div><button class="btn" type="submit">Send</button></div>
    <p class="form-status" role="status" aria-live="polite"></p>
  </form>
</div></section>""")

# News ------------------------------------------------------------------------
news_html = ""
for nid, date, cat, head, body_, rel in NEWS:
    meta = " · ".join(x for x in (cat, date) if x)
    rel_link = f'<p><a href="{href(rel)}">Event page →</a></p>' if rel else ""
    news_html += f"""<article class="card news-item" id="{nid}">
  <p class="meta">{meta}</p>
  <h2 style="font-size:var(--step-2)">{head}</h2>
  <div class="prose">{body_}{rel_link}</div>
</article>"""

page(slug="news", title="News", eyebrow="News", h1="News",
     desc="News and updates from WHPC MENA.",
     lede="Announcements and updates from WHPC MENA. For day-to-day posts, follow us on LinkedIn.",
     body=f"""<section class="section"><div class="wrap two-col">
  <div class="stack">{news_html}</div>
  <aside class="aside card"><h3>Follow along</h3><p>We post event announcements and community news on LinkedIn.</p><a class="btn btn-ghost btn-sm" href="{LINKEDIN}">WHPC MENA on LinkedIn</a></aside>
</div></section>""")

# Contact ---------------------------------------------------------------------
page(slug="contact", title="Contact", eyebrow="Contact", h1="Contact us",
     desc="Contact WHPC MENA about events, partnerships, speaking and media.",
     lede="Questions, partnership ideas, speaker proposals or media requests: we'd like to hear from you.",
     body=f"""<section class="section"><div class="wrap two-col">
  <form class="form card" id="contact-form" data-mailto data-subject="Message via the WHPC MENA website">
    <div class="row">
      <div class="field"><label for="c-name">Name</label><input id="c-name" name="name" data-label="Name" type="text" required autocomplete="name"></div>
      <div class="field"><label for="c-email">Email</label><input id="c-email" name="email" data-label="Email" type="email" required autocomplete="email"></div>
    </div>
    <div class="field"><label for="c-topic">Topic</label>
      <select id="c-topic" name="topic" data-label="Topic"><option>General question</option><option>Partnership or sponsorship</option><option>Speaking or hosting an event</option><option>Event registration</option><option>Media</option><option>Other</option></select></div>
    <div class="field"><label for="c-message">Message</label><textarea id="c-message" name="message" data-label="Message" required></textarea></div>
    {mail_note()}
    <div><button class="btn" type="submit">Send message</button></div>
    <p class="form-status" role="status" aria-live="polite"></p>
  </form>
  <aside class="aside stack">
    <div class="card"><h3>Email</h3><div class="copybox"><code>{EMAIL}</code><button class="btn btn-ghost btn-sm" type="button" data-copy="{EMAIL}">Copy</button></div><p>We aim to reply within a week.</p></div>
    <div class="card"><h3>LinkedIn</h3><p>Follow our page for announcements.</p><a href="{LINKEDIN}">WHPC MENA on LinkedIn →</a></div>
  </aside>
</div></section>""")

# Policies --------------------------------------------------------------------
page(slug="code-of-conduct", title="Code of conduct", eyebrow="Policies", h1="Code of conduct",
     desc="The WHPC MENA code of conduct for events and online spaces.",
     lede="We want everyone to feel welcome and safe at WHPC MENA events and in our online spaces.",
     body=f"""<section class="section"><div class="wrap prose">
  <h2>Scope</h2>
  <p>This code applies to everyone who takes part in WHPC MENA activities: attendees, speakers, volunteers, organisers and sponsors, at in-person and online events, and in our online groups and channels.</p>
  <h2>Expected behaviour</h2>
  <ul>
    <li>Be respectful and considerate, including of different backgrounds, cultures, languages and levels of experience.</li>
    <li>Give others room to speak, and credit people for their work and ideas.</li>
    <li>Ask before taking or sharing photos or recordings of people.</li>
    <li>Look out for each other, and tell an organiser if someone needs help.</li>
  </ul>
  <h2>Unacceptable behaviour</h2>
  <ul>
    <li>Harassment, intimidation or discrimination of any kind.</li>
    <li>Offensive comments or jokes about gender, religion, ethnicity, nationality, disability, age or appearance.</li>
    <li>Unwelcome physical contact or sexual attention.</li>
    <li>Disrupting talks or discussions, or continuing contact after being asked to stop.</li>
  </ul>
  <h2>Reporting</h2>
  <p>If you experience or witness behaviour that breaks this code, tell an organiser at the event or email <a href="mailto:{EMAIL}">{EMAIL}</a>. Reports are handled in confidence.</p>
  <h2>Consequences</h2>
  <p>Organisers may take any action they consider appropriate, from a warning to removal from an event or from our community, without refund.</p>
</div></section>""")

page(slug="privacy", title="Privacy policy", eyebrow="Policies", h1="Privacy policy",
     desc="How WHPC MENA handles personal information and analytics on this website.",
     lede=f"Last updated {LAST_UPDATED}.",
     body=f"""<section class="section"><div class="wrap prose">
  <h2>Who we are</h2>
  <p>This website is run by WHPC MENA, the Middle East and North Africa affiliate of Women in HPC. You can reach us at <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
  <h2>Information you send us</h2>
  <p>The forms on this site do not store anything on the website. They open your own email app with a message addressed to us. When you send it, we receive your name, email address and whatever else you include. We use this only to reply to you, to add you to our mailing list if you asked, or to organise the activity you asked about.</p>
  <p>We keep mailing-list details until you ask us to remove them. Email us at any time to see, correct or delete what we hold about you.</p>
  <h2>Analytics</h2>
  <p>With your permission, we use Google Analytics 4 to understand how the site is used: which pages are visited, roughly which country and city visitors come from, which site referred them, and what type of device and browser they use. This helps us decide what to publish.</p>
  <ul>
    <li>Google Analytics loads only after you choose “Allow analytics”. If you decline, it does not load.</li>
    <li>It sets cookies (named <code>_ga</code> and <code>_ga_*</code>) to recognise returning visitors.</li>
    <li>Google processes this data on our behalf. Google Analytics 4 does not log or store IP addresses. See <a href="https://policies.google.com/privacy">Google's privacy policy</a>.</li>
    <li>You can change your choice at any time with the “Cookie settings” link at the bottom of every page.</li>
  </ul>
  <p>Your choice itself is saved in your browser's local storage so we don't ask on every page.</p>
  <h2>Hosting and fonts</h2>
  <p>Our web host records standard technical logs, such as IP addresses and request times, to keep the site running and secure. Fonts are served from this website, not from a third-party font service.</p>
  <h2>Links to other sites</h2>
  <p>We link to other websites, such as LinkedIn and Women in HPC. Their own privacy policies apply when you visit them.</p>
  <h2>Changes</h2>
  <p>If we change this policy, we will update the date at the top of this page.</p>
</div></section>""")

page(slug="404", title="Page not found", eyebrow="Error 404", h1="Page not found", noindex=True,
     desc="This page could not be found.",
     lede="The page may have moved, or the link may be mistyped.",
     body="""<section class="section"><div class="wrap actions">
  <a class="btn" href="index.html">Go to the home page</a>
  <a class="btn btn-ghost" href="events.html">See our events</a>
</div></section>""")


# -------------------------------------------------------------------- build ---
def main():
    for p in PAGES:
        if p.get("top") is None and "eyebrow" not in p:
            raise SystemExit(f"page {p['slug']} needs eyebrow/h1 or top")
        out = ROOT / href(p["slug"])
        out.write_text(layout(p), encoding="utf-8")
    urls = [f"  <url><loc>{SITE_URL}/{'' if p['slug'] == 'index' else href(p['slug'])}</loc></url>"
            for p in PAGES if not p.get("noindex")]
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls) + "\n</urlset>\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
    print(f"Built {len(PAGES)} pages")


if __name__ == "__main__":
    main()
