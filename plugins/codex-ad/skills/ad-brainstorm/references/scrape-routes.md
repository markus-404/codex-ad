# Scrape Routes

The skill supports ChatGPT, ChatGPT Work, Codex, and Claude hosts through the
tools actually available in the session. Browser access, Python execution,
Python networking, vision, and shell access are separate capabilities.

| Available capability | Route |
|---|---|
| Native page fetching/browsing | Route A |
| Shell with outbound network | Routes B/C if needed |
| No usable page fetch | Ask for product details and original images tied to the URL |
| Image attachments or remote/local image viewer | Inspect actual images |
| Python execution but no terminal | Run validators using host-runtime.md |

Confirm shell + outbound network before using Route B or C. If either is missing,
use Route A if available — do not report failure just because curl was unavailable.

## Route A — host-native fetch (when available)

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

Inspect what the fetch actually returns; search snippets alone are not the
product page. Record only visible facts, and mark unavailable prices/reviews as
unavailable rather than inventing them. Image URLs can be missing — if fewer
than 3 usable image URLs surface, use available Routes B/C or ask for original
image attachments. A pasted URL helps only if the host can fetch and view it.

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

1. **Download, then view** (any host with file-fetch and image-viewing tools):
   ```bash
   mkdir -p output/SLUG/images
   curl -s -L -o output/SLUG/images/img-1.jpg "IMAGE_URL_1"
   ```
   Then open each file with the host's image-reading capability. Files live under
   `output/[slug]/images/` — per-run, so a previous product's photos can never
   contaminate this analysis.

2. **Fetch the image URL directly** if the host can view a remote image without a
   local copy.

3. **Use original image attachments** supplied in the conversation. Keep their
   source/attachment identifiers in the analysis; do not fabricate local paths.

## Total scrape failure

If Route A returns nothing and B/C are unavailable or blocked (JS-rendered SPA,
Cloudflare, bot detection), stop and ask:

> I couldn't retrieve the product details in this session. Please supply the
> title, price, top benefits, and original product images for this URL.

Describe an observed error when available; do not diagnose JavaScript rendering
without evidence. Identify supplied inputs as user-provided. Do not proceed on
empty data.
