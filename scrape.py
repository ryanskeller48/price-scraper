import csv
import logging
import os
import pandas

from browser import Browser
from db import PricesDB
from selenium.common.exceptions import NoSuchElementException


LOG = logging.getLogger(__name__)


class PriceScraper:


    def __init__(self, url, driver_path, db_path="./prices.db"):

        self.orig_url = url
        self.browser = Browser(driver_path)
        self.db = PricesDB(db_path)

        self.browser.open(url)
        self.db.create_table("prices")


    def scrape_individual_item(self, url):
        """ Scrape pricing info from one page. """

        # Open product page
        self.browser.open(url)

        # Get data
        # Sale Price
        try:
            sale_price = float(self.browser.get_element('//div[@class="current-price"]/span').get_attribute("content"))
        except NoSuchElementException:
            sale_price = "No Sale"

        # Regular Price
        try:
            price = self.browser.get_element('//span[@class="regular-price"]').text
        except NoSuchElementException:  # no sale
            price = self.browser.get_element('//span[@itemprop="price"]').get_attribute("content")
        if "$" in price:
            price = float(price.split("$")[1].strip())

        # Name
        name = self.browser.get_element('//h1[@class="product-name"]').text

        # Description
        description = self.browser.get_element('//div[@class="product-short-description"]').text
        if description == "":
            description = "[No description]"
        
        # Out of Stock
        out_of_stock_link = self.browser.get_element('//link[@itemprop="availability"]').get_attribute("href")
        out_of_stock = not "InStock" in out_of_stock_link  # If link says "InStock" assume available

        # Add to db
        row = (name, description, price, sale_price, out_of_stock, url)
        self.db.insert_row(row)


    def scrape_listing_page(self, listing_url):
        """ Handle page with listing of products. """

        self.browser.open(listing_url)
        has_next = True
        while has_next:  # Paginate thru product listings

            # Collect links to products
            products = self.browser.get_elements('//*[@id="js-product-list"]/div/article/div/div/a[@class="thumbnail product-thumbnail"]')
            product_urls = [product.get_attribute("href") for product in products]
            for url in product_urls:  # Scrape each product page
                self.scrape_individual_item(url)

            # Go back to original page
            self.browser.open(self.orig_url)  # Return to the listing page

            # Click next button -- the next button exists even if there is no next page, so need to check the URL
            next_button = self.browser.get_elements('//a[@rel="next"]')[0]
            next_url = next_button.get_attribute("href")
            has_next = next_url != self.orig_url  # If the URL of the next button is different, there are more pages
            if has_next:
                self.orig_url = next_url  # Set base URL as the next page
                self.browser.open(next_url)  # Go to next page


    def scrape(self):
        """ Scrape data from site. """

        self.scrape_listing_page(self.orig_url)  # This works recursively to scrape all pages from the root


    def list_inventory(self):
        """ Print out inventory in human-readable format and write to csv. """

        # Get data from DB
        query_sql = "SELECT * FROM prices ORDER BY price DESC, name ASC;"
        rows = self.db.query_db(query_sql)

        # Write csv file
        try:  # Remove file if it exists
            os.remove('prices.csv')
        except FileNotFoundError:
            LOG.info("Existing csv file not found, continuing")
        with open('prices.csv', 'w', newline='') as csvfile:
            price_csv = csv.writer(csvfile, delimiter='|', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)
            # Write header
            price_csv.writerow(["Product ID", "Name", "Description", "Price", "Sale Price", "Out Of Stock", "URL"])
            # Write rows
            for row in rows:
                product_id = row[0]
                name = row[1]
                description = row[2].strip()
                price = row[3]
                sale_price = row[4]
                out_of_stock = bool(row[5])
                url = row[6]

                price_csv.writerow([product_id, name, description, price, sale_price, out_of_stock, url])

        # Write out data to console
        outfile = pandas.read_csv("prices.csv", quotechar="'", delimiter="|")
        print(outfile)


    def clean(self):
        """ Clean up resources. """

        self.browser.quit()
        self.db.close()
