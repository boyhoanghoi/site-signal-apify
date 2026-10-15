# SiteSignal Store artwork

The artwork uses the existing vector mark from `dist/favicon.svg`. No Actor
code, pricing or website hosting audience is changed by adding these assets.

## Upload the Actor icon

1. Open [SiteSignal Publishing](https://console.apify.com/actors/KgxuXmLMsWUuA8Jkw/publication).
2. Expand **Display information** and find the Actor logo/image upload control.
3. Choose `assets/brand/sitesignal-icon-512.png` from this repository.
4. Save the display information and refresh the public Store page.

The 1024px PNG is available as a larger original; the SVG is the editable vector
source. The Actor logo is separate from the owner's personal profile avatar.
Apify documents the logo control under
[Publishing → Display information](https://docs.apify.com/actors/publishing/publish).

## Product preview

`assets/brand/sitesignal-store-preview.png` is a 1600×900 illustration of the
output fields. Its records are clearly labeled fictional samples, and it makes
no claim about email deliverability, customer counts or revenue. It is embedded
in the Actor README using the public GitHub asset URL. It is separate from the
square Actor icon and does not replace it.

The preview's HTML source and a rendering script are supplied with the artwork.
The script uses Playwright and Chrome to export deterministic SVG/HTML assets;
it does not require an image-generation service or an API key.
