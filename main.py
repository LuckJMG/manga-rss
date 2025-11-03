from datetime import datetime

import feedgenerator  # pyright: ignore[reportMissingTypeStubs]
import requests
from bs4 import BeautifulSoup

class Chapter:
    def __init__(self, title: str, link: str, upload_date: datetime):
        self.title: str = title
        self.link: str = link
        self.upload_date: datetime = upload_date

class MangaPage:
    def __init__(
            self, 
            name: str, 
            url: str, 
            title: str, 
            schedule: int, 
            list_select: str, 
            title_select: str, 
            skip_first: bool = False
    ) -> None:
        self.name: str = name
        self.url: str = url
        self.title: str = title
        self.schedule: int = schedule
        self.list_select: str = list_select
        self.title_select: str = title_select
        self.skip_first: bool = skip_first

    def get_chapters(self, max_chapters: int) -> list[Chapter]:
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            chapters = soup.select(self.list_select)

            curated_chapters: list[Chapter] = []
            bias = int(self.skip_first)
            for chapter in chapters[bias:max_chapters+bias]:
                title_el = chapter.select_one(self.title_select)
                link_el = chapter.find("a")

                if not title_el or not link_el:
                    continue

                title: str = title_el.text.strip()  # pyright: ignore[reportAny]
                link: str = link_el.get("href", "")  # pyright: ignore[reportAssignmentType]
                date = datetime.now()

                curated_chapters.append(Chapter(title, link, date))

            return curated_chapters

        except requests.RequestException as e:
            print(f"[ERROR] Failed to fetch {self.name}: {e}")
            return[]

    def generate_feed(self, max_chapters: int):
        feed = feedgenerator.Rss201rev2Feed(
            title=self.title,
            link=self.url,
            description=f"Feed de {self.title}"
        )

        chapters: list[Chapter] = self.get_chapters(max_chapters)
        if not chapters:
            print(f"[WARN] No chapters found for {self.title}")
            return

        for chapter in chapters:
            feed.add_item(  # pyright: ignore[reportUnknownMemberType]
                title=chapter.title,
                link=chapter.link,
                pubdate=chapter.upload_date,
                description=""
            )

        with open(f"feeds/{self.name}.xml", "w", encoding="utf-8") as f:
            feed.write(f, "utf-8")  # pyright: ignore[reportUnknownMemberType]
        print(f"[INFO] Updated {self.title} Feed")

MANGA_PAGES = [
    MangaPage("blue-lock", "https://ww2.bluelockread.com/manga/blue-lock/", "Blue Lock", 2, ".col-span-4", "a"),
    MangaPage("infinite-mage", "https://asuracomic.net/series/infinite-mage-513dbdec", "Infinite Mage", 2, ".py-2", "h3"),
    MangaPage("karou-hana", "https://kaoruhana.org/", "Kaoru Hana wa Rin to Saku", 3, ".item", "span", True),
    MangaPage("my-bias", "https://mybiasgetsonthelasttrain.com/", "My Bias Gets On The Last Train", 4, ".item", "span", True),
]

def main():
    today = datetime.now().weekday()
    for manga_page in MANGA_PAGES:
        if manga_page.schedule == today:
            manga_page.generate_feed(10)

if __name__ == "__main__":
    main()

