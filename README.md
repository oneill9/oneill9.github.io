# oneill9.github.io

The portfolio and shared crawler configuration for <https://oneill9.github.io/>.
Each project site continues to deploy from its own repository.

## Contents

- `index.html` presents six projects, including Phrase Flip at <https://phraseflip.com/>
  and RedditViewer at <https://www.syntacticbrownsugar.tech/RedditViewer/>.
- `assets/fonts` contains locally hosted Instrument Sans and Instrument Serif fonts and their licenses.
- `assets/previews` contains screenshots of the project pages, cropped inside
  the coloured thumbnail panels. These are static images, not embedded sites.
- GitHub icons link to the four public project repositories. Phrase Flip and
  RedditViewer have private repositories and do not have source links.
- `assets/icons` contains the GitHub mark from [Octicons](https://github.com/primer/octicons)
  and its MIT license, plus the "AO" favicon. `apple-touch-icon.png` is rendered from
  `favicon.svg` without the rounded corners:
  `sed 's/ rx="14"//' assets/icons/favicon.svg | rsvg-convert -w 180 -h 180 -o assets/icons/apple-touch-icon.png`.
- `assets/images/social-preview.jpg` is the 1200 × 630 link-preview image, cropped from the portrait.
- `404.html` is served for missing pages. It uses root-relative asset paths so it renders at any depth.
- `sitemap.xml` is a sitemap index for the existing project sitemaps and `pages-sitemap.xml`.
- `pages-sitemap.xml` covers this homepage and Print to Notes, which has no sitemap of its own.
- `robots.txt` allows crawling and advertises the sitemap index for the entire host.

## Publishing

Enable GitHub Pages in the repository settings with **GitHub Actions** as its
source. The workflow tests every pull request and deploys successful pushes to
`main`. It uploads the six public site files and assets, excluding tests and this README.
No build dependencies are required.

After deployment, submit `https://oneill9.github.io/sitemap.xml` in Google Search
Console for a verified property covering `https://oneill9.github.io/`. This advertises the sitemaps to Google; it does not guarantee indexing.

## Adding a project

1. Add its project link and description to `index.html`.
2. If it has a sitemap on `oneill9.github.io`, add the sitemap URL to `sitemap.xml`.
   Otherwise, add its homepage URL to `pages-sitemap.xml`.
3. For external domains like Phrase Flip, link from the portfolio but leave their
   sitemaps on their own domains.
4. Update the expected projects in `tests/test_site.py` and run the tests.

If Print to Notes adds its own sitemap later, reference that sitemap from the
index and remove its homepage from `pages-sitemap.xml`.

## Testing

```sh
python3 -m unittest discover -s tests -v
```

The tests check project links, copy, metadata, icons, link previews, structured data, the 404 page, Google Analytics tracking, local assets,
font licenses, screenshot dimensions, sitemap coverage, and crawler discovery.

To refresh a thumbnail, capture the relevant page at a 1000 × 680 viewport and
replace its PNG in `assets/previews`. Phrase Flip clips the hero. RedditViewer
uses a 1280 × 800 capture of a loaded kintsugi pottery-repair video from
`r/artisanvideos`, paused at 00:54 with the controls visible. In Season uses the UK calendar table.
Update the image's HTML width and height if the captured crop changes dimensions.
The CSS controls the crop and framing inside the portfolio.

Typography: [Instrument Serif](https://github.com/Instrument/instrument-serif)
and [Instrument Sans](https://github.com/Instrument/instrument-sans), both under
the SIL Open Font License included with the assets.

Reference: [sitemap indexes](https://developers.google.com/search/docs/crawling-indexing/sitemaps/large-sitemaps).
