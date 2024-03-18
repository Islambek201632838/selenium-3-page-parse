from parser.storage import JsonStorage
from parser.translator import TextTranslator
from parser.web_scraper import WebScraper


def main():
    url = "https://registers.centralbank.ie/FirmSearchPage.aspx"
    translator = TextTranslator(src='en', dest='ru')
    scraper = WebScraper()
    results = scraper.scrape_website(url, translator)
    storage = JsonStorage('data.json')
    storage.save(results)

if __name__ == "__main__":
    main()
