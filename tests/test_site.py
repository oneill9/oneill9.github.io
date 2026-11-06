import unittest
import re
import struct
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://oneill9.github.io/"
NAMESPACE = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
PROJECTS = {"function-keys", "tfl-mcp-server", "trmnl-in-season", "print-to-notes"}
PROJECT_URLS = {f"{BASE_URL}{name}/" for name in PROJECTS} | {
    "https://phraseflip.com/", "https://www.syntacticbrownsugar.tech/RedditViewer/"
}


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


class SiteTests(unittest.TestCase):
    def setUp(self):
        self.page = Page()
        self.page.feed((ROOT / "index.html").read_text())

    def test_portfolio_links_to_every_project(self):
        links = [attrs for tag, attrs in self.page.tags if tag == "a"]
        projects = [attrs["href"] for attrs in links if attrs.get("class") == "project-link"]
        self.assertEqual(set(projects), PROJECT_URLS)
        self.assertEqual(len(projects), len(PROJECT_URLS))
        self.assertEqual(projects[0], "https://phraseflip.com/")
        self.assertEqual(sum(tag == "article" for tag, _ in self.page.tags), len(PROJECT_URLS))

    def test_portfolio_copy_focuses_on_the_work(self):
        html = (ROOT / "index.html").read_text()
        for phrase in ["Built in the open", "Open source projects", "Small tools.", "Source code"]:
            self.assertNotIn(phrase, html)
        self.assertIn("Selected <em>work.</em>", html)

    def test_profile_identifies_the_person_behind_the_work(self):
        html = (ROOT / "index.html").read_text()
        self.assertIn('<span class="wordmark">Alex O\'Neill</span>', html)
        self.assertIn("<title>Alex O'Neill | Selected work</title>", html)
        portraits = [attrs for tag, attrs in self.page.tags
                     if tag == "img" and attrs.get("alt") == "Alex O'Neill"]
        self.assertEqual(len(portraits), 1)
        self.assertLess(html.index(portraits[0]["src"]), html.index("<main>"))
        self.assertEqual((ROOT / portraits[0]["src"]).read_bytes()[:3], b"\xff\xd8\xff")

    def test_repository_links_cover_only_public_projects(self):
        links = [attrs for tag, attrs in self.page.tags
                 if tag == "a" and attrs.get("class") == "repo-link"]
        self.assertEqual({link["href"] for link in links}, {
            f"https://github.com/oneill9/{name}" for name in PROJECTS
        })
        self.assertEqual(len(links), len(PROJECTS))
        for link in links:
            self.assertIn("repository on GitHub", link["aria-label"])

    def test_fonts_are_local_and_licensed(self):
        css = (ROOT / "styles.css").read_text()
        fonts = re.findall(r'url\("([^"]+)"\)', css)
        self.assertEqual(len(fonts), 3)
        for font in fonts:
            self.assertEqual((ROOT / font).read_bytes()[:4], b"wOF2")
        for family in ["InstrumentSans", "InstrumentSerif"]:
            self.assertIn("SIL OPEN FONT LICENSE", (ROOT / f"assets/fonts/{family}-LICENSE.txt").read_text())

    def test_metadata_and_local_assets(self):
        self.assertIn(("html", {"lang": "en"}), self.page.tags)
        self.assertEqual(sum(tag == "h1" for tag, _ in self.page.tags), 1)
        self.assertIn(("link", {"rel": "canonical", "href": BASE_URL}), self.page.tags)
        for tag, attrs in self.page.tags:
            if tag == "meta" and attrs.get("name") == "description":
                self.assertTrue(attrs["content"].strip())
            asset = attrs.get("src") if tag in {"script", "img"} else attrs.get("href") if tag == "link" else None
            if asset and not asset.startswith("https://"):
                self.assertTrue((ROOT / asset.split("?")[0]).is_file(), asset)

    def test_each_project_has_a_local_page_preview(self):
        images = [attrs for tag, attrs in self.page.tags
                  if tag == "img" and attrs.get("src", "").startswith("assets/previews/")]
        self.assertEqual(len(images), len(PROJECT_URLS))
        self.assertEqual(len({image["src"] for image in images}), len(images))
        for image in images:
            self.assertTrue(image["src"].startswith("assets/previews/"))
            data = (ROOT / image["src"]).read_bytes()
            self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
            self.assertEqual(struct.unpack(">II", data[16:24]),
                             (int(image["width"]), int(image["height"])))
            self.assertEqual(image["alt"], "")
            self.assertEqual(image["decoding"], "async")
        self.assertTrue(all(image["loading"] == "lazy" for image in images[2:]))

    def test_sitemap_index_covers_root_and_all_projects(self):
        index = ElementTree.parse(ROOT / "sitemap.xml")
        self.assertEqual(index.getroot().tag, f"{{{NAMESPACE['s']}}}sitemapindex")
        locations = [loc.text for loc in index.findall("s:sitemap/s:loc", NAMESPACE)]
        self.assertEqual(len(locations), len(set(locations)))
        self.assertEqual(set(locations), {f"{BASE_URL}pages-sitemap.xml"} | {
            f"{BASE_URL}{name}/sitemap.xml" for name in PROJECTS - {"print-to-notes"}
        })
        pages = ElementTree.parse(ROOT / "pages-sitemap.xml")
        self.assertEqual(pages.getroot().tag, f"{{{NAMESPACE['s']}}}urlset")
        self.assertEqual({loc.text for loc in pages.findall("s:url/s:loc", NAMESPACE)},
                         {BASE_URL, f"{BASE_URL}print-to-notes/"})

    def test_robots_allows_crawling_and_advertises_index(self):
        lines = (ROOT / "robots.txt").read_text().splitlines()
        self.assertIn("User-agent: *", lines)
        self.assertIn("Allow: /", lines)
        self.assertEqual([line for line in lines if line.startswith("Sitemap:")],
                         [f"Sitemap: {BASE_URL}sitemap.xml"])


if __name__ == "__main__":
    unittest.main()
