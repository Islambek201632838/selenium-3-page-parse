Project Structure

    main.py: Entry point of the program. It initializes the web scraper, performs scraping, and saves the results.

    parser/
        web_scraper.py: Defines the WebScraper class responsible for scraping the website.
        
        translator.py: Contains the TextTranslator class for translating text.
        
        storage.py: Implements the JsonStorage class to handle JSON data storage.
        
        utils/
            browser_events.py: Defines the BrowserEvents class for browser-related actions.
            
            page_scraper.py: Contains the PageScraper class responsible for scraping individual pages.
            
            window.py: Implements the HandleWindow class for managing browser windows.
            
            setup.py: Contains the SetUp class for setting up the WebDriver.