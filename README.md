# WHPC MENA website

A static website for WHPC MENA (Women in High Performance Computing – Middle East & North Africa). Plain HTML, CSS and a little JavaScript: no build tools are needed to host it, and it runs on GitHub Pages, Cloudflare Pages, Netlify or any web server.

## Before going live

1. **Google Analytics ID.** Open `assets/js/site.js` and replace `G-XXXXXXXXXX` with your GA4 Measurement ID. Until you do, no analytics code loads and no cookie banner appears.
2. **LinkedIn link.** In `_build/build.py`, set `LINKEDIN` to your LinkedIn page URL, then rebuild (see below).
3. **Example content.** Anything on a pale yellow card with a dashed border and an "Example — replace" label is a placeholder: team members, partners, institutions, jobs, events and the first news post. Replace or remove them.
4. **Privacy policy.** Read `privacy.html` and adjust it to how you actually handle mailing-list data.

## Editing pages

All pages share one header, menu and footer, defined in `_build/build.py` together with each page's content.

- Edit the content in `_build/build.py`, then run `python3 _build/build.py` (Python 3.8+, nothing to install). It rewrites every `.html` file and `sitemap.xml`.
- Or edit an `.html` file directly for a quick fix. Note that re-running the build script overwrites it, so copy the change into `build.py` as well.

### Adding a past event

Copy the `event-template` entry in `build.py`, give it a new slug (for example `event-2026-03-meetup`), fill in the recap, and link to it from the Past events page.

## Forms

The forms (mailing list, contact, mentorship, volunteering) do not use any outside service. When someone submits one, their email app opens with a message to marhaba@whpcmena.org, filled in from the form. If you later choose a form or mailing-list service, only the `data-mailto` handling in `assets/js/site.js` needs to change.

## Analytics

Google Analytics 4 loads only after a visitor clicks "Allow analytics" in the cookie banner. Once it is running you can see, in the GA dashboard:

- **Reports → Engagement → Pages and screens**: which pages are viewed most.
- **Reports → User attributes → Demographic details**: visitors by country and city.
- **Reports → Acquisition → Traffic acquisition**: where visitors come from (LinkedIn, search, direct).

Form submissions and clicks on outside links are also recorded as events (`form_submit`, `outbound_click`).

## Hosting on GitHub Pages

1. Create a public repository and upload the contents of this folder to it (the `.html` files at the top level).
2. In the repository, go to **Settings → Pages**, choose **Deploy from a branch**, select `main` and `/ (root)`, and save.
3. The site appears at `https://<account>.github.io/<repository>/`.

### Using whpcmena.org

1. In **Settings → Pages → Custom domain**, enter `whpcmena.org` and save. GitHub adds a `CNAME` file to the repository.
2. At whoever manages the whpcmena.org DNS, add the records GitHub lists in its "Managing a custom domain" guide (A records for the bare domain and a CNAME for `www`).
3. **Do not change or remove the existing MX records**; those deliver your email.
4. Once DNS has updated, tick **Enforce HTTPS**.

## Fonts

Bricolage Grotesque, IBM Plex Sans, IBM Plex Sans Arabic and IBM Plex Mono are included in `assets/fonts` under the SIL Open Font License. The site makes no requests to font services.
