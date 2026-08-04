# Scrape Routes

The skill runs in four host environments with different capabilities. Route A is
host-native and works everywhere. Routes B and C need a shell and are strictly
faster/richer fallbacks, not requirements.

| Host | Native fetch | Native vision | Shell + network | Python |
|---|---|---|---|---|
| Claude Code | yes (WebFetch) | yes (Read on image files) | yes | yes |
| Codex CLI | yes | yes (image input) | yes | yes |
| Claude.ai | yes | yes (attached/fetched images) | no outbound network | sandboxed |
| Cowork | yes | yes | varies | yes |

Confirm shell + outbound network before using Route B or C. If either is missing,
Route A alone is sufficient — do not report failure because curl was unavailable.

## Route A — host-native fetch (default, all hosts)

Use the host's own page-fetching capability against the product URL and extract:

- Product title (exact) and brand name
- Price, and sale price if shown
- Top 5 benefits or features as short phrases
- Full product description paragraph
- 3-5 customer review quotes if visible
- Star rating and review count
- Brand voice cues (playful, clinical, premium, casual)
- Ingredient list, materials, or spec sheet
- CTA text on the page
- Every product image URL visible in the markup

Native fetch returns processed text and is reliable for the copy layer. Image URLs
come back inconsistently — if fewer than 3 usable image URLs surface, escalate to
Route B or C, or ask the user to paste image URLs.

## Route B — Shopify product JSON (shell, best quality)

Most DTC product pages are Shopify. Appending `.json` to the product path returns
clean structured data with full-resolution image URLs and no HTML parsing:

```bash
curl -s -L -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36' \
  "https://SITE/products/SLUG.json" | head -c 200000
```

Yields `title`, `vendor`, `body_html`, `variants[].price`, `images[].src`.
If it 404s or returns HTML, the site is not Shopify — fall through to Route C.

## Route C — raw HTML image sweep (shell)

```bash
curl -s -L -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36' \
  "PRODUCT_URL" \
  | grep -oE 'https?://[^"'"'"' ]+\.(jpg|jpeg|png|webp)[^"'"'"' ]*' \
  | grep -viE 'logo|icon|favicon|sprite|badge|payment|placeholder' \
  | sed 's/[?&]width=[0-9]*//g; s/[?&]v=[0-9]*//g' \
  | sort -u | head -20
```

Prefer full-resolution URLs. Skip anything matching `100x100`, `_small`, `_thumb` —
low-res inputs produce vague analysis, and `validate_analysis.py` will fail the run
on thin prose rather than let it through.

## Getting images in front of the model

The analysis step requires actually seeing the photos. In order of preference:

1. **Download, then read** (Claude Code, Codex, Cowork with shell):
   ```bash
   mkdir -p output/SLUG/images
   curl -s -L -o output/SLUG/images/img-1.jpg "IMAGE_URL_1"
   ```
   Then open each file with the host's image-reading capability. Files live under
   `output/[slug]/images/` — per-run, so a previous product's photos can never
   contaminate this analysis.

2. **Fetch the image URL directly** if the host can view a remote image without a
   local copy.

3. **Ask the user to paste the images** into the conversation.

## Total scrape failure

If Route A returns nothing and B/C are unavailable or blocked (JS-rendered SPA,
Cloudflare, bot detection), stop and ask:

> This page is JS-rendered and I can't extract content. Please paste: title, price,
> top 5 benefits, and the product images (or their URLs).

Do not proceed on empty data.
