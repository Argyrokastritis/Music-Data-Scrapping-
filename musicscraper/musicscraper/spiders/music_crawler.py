import scrapy
from ..items import MusicscraperItem
import sys
import re
from bs4 import BeautifulSoup
import os


def clean_text(text):
    # Αφαιρεί ακολουθίες τύπου [23], [72][73], κλπ.
    return re.sub(r'\[(\d+)\]+', '', text)


class MusicSpider(scrapy.Spider):
    name = 'music'

    start_urls = [
        'https://en.wikipedia.org/wiki/Music',
        'https://en.wikipedia.org/wiki/Musical_note',
        'https://en.wikipedia.org/wiki/Clef'
    ]

    def __init__(self, paragraph_name=None, *args, **kwargs):
        super(MusicSpider, self).__init__(*args, **kwargs)
        self.paragraph_name = paragraph_name
        self.scraped_titles = set()

    url_suffix_mapping = {
        'https://en.wikipedia.org/wiki/Music': 'of Music',
        'https://en.wikipedia.org/wiki/Musical_note': 'of Musical Note',
        'https://en.wikipedia.org/wiki/Clef': 'of Clef'
    }

    @classmethod
    def get_suffix(cls, url):
        for key in cls.url_suffix_mapping:
            if url.strip().lower() == key.lower():
                return cls.url_suffix_mapping[key]
        return ''

    def parse(self, response):
        # Αποθήκευσε το HTML για debugging
        debug_html_path = "debug_music.html"
        with open(debug_html_path, "w", encoding="utf-8") as f:
            f.write(response.text)

        section_id = self.paragraph_name  # π.χ. "History"
        items = MusicscraperItem()

        self.logger.info("Parsing: %s", response.url)

        # --- Ενσωμάτωση της λογικής debug_extract_ids μέσα στην parse ---

        if not os.path.exists(debug_html_path):
            self.logger.warning("File not found: %s", debug_html_path)
            # Αν δεν βρεθεί το αρχείο, επέστρεψε κενά δεδομένα
            items['title'] = section_id or ''
            items['text'] = []
            items['urls'] = []
            yield items
            return

        with open(debug_html_path, "r", encoding="utf-8") as f:
            html = f.read()

        soup = BeautifulSoup(html, "html.parser")

        # Βρες το <h2> με το συγκεκριμένο id
        h2 = soup.find("h2", id=section_id)

        if not h2:
            self.logger.info(f"No <h2 id='{section_id}'> found in the document")
            items['title'] = section_id or ''
            items['text'] = []
            items['urls'] = []
            yield items
            return

        self.logger.info(f"Found <h2 id='{section_id}'> with text: {h2.get_text(strip=True)}")

        section_text = []
        section_urls = []

        # Πήγαινε στα επόμενα αδερφά στοιχεία μέχρι το επόμενο <h2>
        for sibling in h2.find_all_next():
            if sibling.name and sibling.name.startswith("h2"):
                break  # Τέλος section

            if sibling.name == "p":
                text = clean_text(sibling.get_text(strip=True))
                section_text.append(text)

                # Βρες URLs μέσα στο <p>
                for a in sibling.find_all("a", href=True):
                    section_urls.append(a["href"])

        self.logger.info(f"Extracted {len(section_text)} paragraphs and {len(section_urls)} URLs")

        # Εκτύπωσε τις παραγράφους
        for i, paragraph in enumerate(section_text, 1):
            self.logger.info(f"Paragraph {i}: {paragraph}")

        # Εκτύπωσε τα URLs
        for i, url in enumerate(section_urls, 1):
            self.logger.info(f"URL {i}: {url}")

        # Δημιούργησε τίτλο με suffix
        suffix = self.get_suffix(response.url)
        title = f"{section_id} {suffix}".strip()

        items['title'] = title
        items['text'] = section_text
        items['urls'] = section_urls

        # Εκτύπωσε με ασφάλεια UTF-8 (αν θέλεις μπορείς να αφαιρέσεις αυτή την εκτύπωση)
        try:
            print(*[
                str(arg).encode(sys.stdout.encoding or 'utf-8', errors='replace').decode(sys.stdout.encoding or 'utf-8')
                for arg in ("The extracted title is:", title)
            ])
            print(*[
                str(arg).encode(sys.stdout.encoding or 'utf-8', errors='replace').decode(sys.stdout.encoding or 'utf-8')
                for arg in ("The extracted text is:", section_text)
            ])
            print(*[
                str(arg).encode(sys.stdout.encoding or 'utf-8', errors='replace').decode(sys.stdout.encoding or 'utf-8')
                for arg in ("The extracted urls are:", section_urls)
            ])
        except Exception as e:
            self.logger.warning(f"Error printing UTF-8: {e}")

        yield items

