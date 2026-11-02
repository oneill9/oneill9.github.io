# oneill9.github.io

The directory and shared crawler configuration for <https://oneill9.github.io/>.
Each project site continues to deploy from its own repository.

## Contents

- `index.html` links to the four published project sites and their source repositories.
- `sitemap.xml` is a sitemap index for the existing project sitemaps and `pages-sitemap.xml`.
- `pages-sitemap.xml` covers this homepage and Print to Notes, which has no sitemap of its own.
- `robots.txt` allows crawling and advertises the sitemap index for the entire host.

## Publishing

Enable GitHub Pages in the repository settings with **GitHub Actions** as its
source. The workflow tests every pull request and deploys successful pushes to
`main`. It uploads only the five public site files, excluding tests and this README.
No build dependencies are required.

After deployment, submit `https://oneill9.github.io/sitemap.xml` in Google Search
Console for a verified property covering `https://oneill9.github.io/`. This advertises the sitemaps to Google; it does not guarantee indexing.

## Adding a project

1. Add its project and source links to `index.html`.
2. If it has a sitemap on `oneill9.github.io`, add the sitemap URL to `sitemap.xml`.
   Otherwise, add its homepage URL to `pages-sitemap.xml`.
3. Update the expected projects in `tests/test_site.py` and run the tests.

If Print to Notes adds its own sitemap later, reference that sitemap from the
index and remove its homepage from `pages-sitemap.xml`.

## Testing

```sh
python3 -m unittest discover -s tests -v
```

The tests check project links, metadata, local assets, sitemap coverage, crawler
discovery.

Reference: [sitemap indexes](https://developers.google.com/search/docs/crawling-indexing/sitemaps/large-sitemaps).
