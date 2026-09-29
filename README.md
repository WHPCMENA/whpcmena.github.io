# WHPC MENA website

A static website for WHPC MENA (Women in High Performance Computing – Middle East & North Africa). Plain HTML, CSS and a little JavaScript: no build tools are needed to host it, and it runs on GitHub Pages, Cloudflare Pages, Netlify or any web server.

## Before going live

1. **Google Analytics.** Runs on every page with Measurement ID `G-T6E0G7T9XZ` (set as `GA_ID` in `_build/build.py`).
2. **Privacy policy.** Read `privacy.html` and adjust it to how you actually handle mailing-list data.

## Editing pages

All pages share one header, menu and footer, defined in `_build/build.py` together with each page's content.

- Edit the content in `_build/build.py`, then run `python3 _build/build.py` (Python 3.8+, nothing to install). It rewrites every `.html` file and `sitemap.xml`.
- Or edit an `.html` file directly for a quick fix. Note that re-running the build script overwrites it, so copy the change into `build.py` as well.

### Adding a past event

Copy the `event-template` entry in `build.py`, give it a new slug (for example `event-2026-03-meetup`), fill in the recap, and link to it from the Past events page.

## Photos

Photos live in `assets/img/` and are listed in `PHOTOS` in `_build/build.py`. Until a photo file exists, its page shows a "Photo coming soon" placeholder. Upload a file with exactly the listed name and it appears on the next page load, with no rebuild needed.

| File name | Where it appears |
|---|---|
| `photo-isc-2026-speakers.jpg` | ISC High Performance 2026 event page |
| `photo-news-milestone.jpg` | Milestone post on the News page, and its card on the home page |

Use landscape JPGs about 1600 px wide and under 500 KB. File names are case-sensitive.

## Forms

Every "Join the mailing list" button links to the WHPC MENA Google Form (set as `JOIN_URL` in `_build/build.py`). The contact, mentorship and volunteering forms use no outside service: submitting one opens the visitor's email app with a message to marhaba@whpcmena.org, filled in from the form.

## Analytics

Google Analytics 4 runs on every page. You can see, in the GA dashboard:

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

Nunito, Nunito Sans and Noto Naskh Arabic are included in `assets/fonts` under the SIL Open Font License. The site makes no requests to font services.
