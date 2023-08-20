from scrape import PriceScraper

scraper = PriceScraper("https://glacial.com.uy/8-vegetales", "./chromedriver", "./prices.db")
scraper.scrape()
scraper.list_inventory()
scraper.clean()
