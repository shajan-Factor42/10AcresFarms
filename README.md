# 10acresfarms.com: homepage handoff

This is the approved homepage design for **10 Acre Farms**, a family farm in Gwinnett County, GA, selling cage-free, free-range chicken and duck eggs. It's a static, mobile-first page with no build step and no framework, so it drops into any host (Netlify, Cloudflare Pages, GitHub Pages, cPanel) or can be rebuilt as a theme in WordPress, Squarespace, Shopify, and so on.

## What's in the folder

```
index.html                    the homepage
assets/css/styles.css         all styles; brand colours are CSS variables at the top
assets/img/logo-wordmark.svg  header logo
assets/img/badge.svg          round badge (colour) used in the hero
assets/img/badge-reverse.svg  round badge (light-on-dark) used in the footer
assets/img/favicon.svg        favicon (the "10" monogram)
robots.txt, sitemap.xml       for search engines
CNAME                         tells GitHub Pages to serve the site on 10acresfarms.com (don't delete)
```

Hosted on GitHub Pages from `main` of `shajan-Factor42/10AcresFarms`: pushing to `main` publishes the site. The previous multi-page site (order form, FAQ, blog, contact, privacy) was replaced on 2026-10-03 and is still in git history if any of it is needed again.

Fonts load from Google Fonts: **Fraunces** for headlines and prices, **Libre Franklin** for body text, and **Courier Prime** for the date-stamp details.

The page was checked at 1440, 390 and 360 px wide, with no sideways scrolling.

## Before launch: fill every [BRACKET]

Search the HTML for `[` to find them all.

| Placeholder | Where |
| --- | --- |
| `[DAYS, HOURS]` | Fresh-today bar at the top |
| `[DATE]` | "Collected on" stamp in the hero. Update it weekly, or delete the stamp. |
| `[PRICE]` ×2 | Chicken and duck egg cards |
| `[ADD A LINE ABOUT SHELL COLOURS OR BREEDS]` | Chicken egg card |
| `[COOP / BARN]` | "Cage-free" promise |
| `[STREET ADDRESS]`, `[CITY]`, `[DAYS]`, `[HOURS]` | Farm stand card |
| `[MARKET NAME]`, `[DAY]`, `[HOURS]` | Farmers markets card |
| `[STORE NAME]` | Grocers & co-ops card |
| `[DELIVERY AREA]`, `[DELIVERY DAYS]` | Order ahead card |
| `[TWO OR THREE SENTENCES…]` | Our farm story |
| `[EMAIL ADDRESS]`, `[PHONE]` | Footer. Keep the `mailto:` and `tel:` links. |
| JSON-LD block in `<head>` | Phone, email, address, ZIP, opening hours. Delete any line you can't fill. |

## Links and the form to wire up

- **`[ORDERING LINK]`**: the "Start an order" button. Every "Order" and "Reserve" button scrolls to that card, so this one link is the main conversion point. Point it at whatever ordering tool the farm uses (Square, Shopify, Local Line, or a simple form).
- **`[GOOGLE MAPS LINK]`**: Get directions.
- **`[MARKETS PAGE OR SOCIAL LINK]`**, **`[STORES PAGE LINK]`**, **`[OUR STORY PAGE LINK]`**: link these to pages or social posts, or remove the links until those pages exist.
- **Egg-list form**: set `action` (and the service's hidden fields if it needs them) for the email tool you use (Mailchimp, Kit, Resend, etc.). Keep `name="email"` and `required`. Add a thank-you message or page on success.

## Photos (still needed)

The kraft-coloured boxes are photo slots, and each one has an HTML comment with the replacement `<img>` tag. Use real farm photos only: natural daylight, a bit of straw, no stock or studio-white shots.

1. **Hero (5:4)**: a hand holding a duck egg next to a chicken egg, in morning light.
2. **Chicken egg card (16:9)**: an open carton of chicken eggs.
3. **Duck egg card (16:9)**: a duck egg beside a chicken egg, so the size difference shows.
4. **Our farm (4:3)**: the family with the hens and ducks, outdoors.
5. **Social share image (1200×630)**: save as `assets/img/og-image.jpg`.

Export at about 2× display size as WebP or JPG, under ~300 KB each. Add `loading="lazy"` on everything below the hero, and write real `alt` text for each.

## Brand and claim rules (please don't change these)

- Write the name as **10 Acre Farms**: never "10acre", "Ten Acre" or "10-Acre" in visible text.
- The eggs are **cage-free and free-range**. They are **not organic**. Never add "organic," "pasture-raised," "hormone-free," "antibiotic-free," "non-GMO," or health or nutrition claims.
- Keep the safe-handling line in the footer.
- Colours: barn red `#9E2B25` belongs to the brand and the chicken line, duck blue `#9DBDB8` to the duck line, and yolk `#E0982F` is a small accent only. On the duck-blue band, text stays dark ink, never white.
- The full brand system (logos, colours, type, voice) lives in the 10 Acre Farms design system on Claude. Ask the owner for access if you need other logo versions.
- **Compliance:** before the site goes live, the farm should confirm egg-sales licensing and labeling with the Georgia Department of Agriculture.

## Measure from day one

Please add analytics (GA4 or Plausible) and track these as events, because they're how we'll judge the page:

- Clicks on **Start an order** and on any **Order / Reserve** button
- **Egg-list signups** (successful form submissions)
- Clicks on **Get directions**, and **phone / email** taps
- Clicks on the market and store links

## SEO notes

- The title and meta description already target "farm fresh eggs," "duck eggs" and "Gwinnett County."
- Set up a **Google Business Profile** for the farm stand, using the same name, address and phone as the footer.
- Keep the single H1, and add the canonical URL on the live domain (already set to `https://10acresfarms.com/`).
