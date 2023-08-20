# Price Scraper

This tool scrapes price data from https://glacial.com.uy/8-vegetales, reads it into a database,
formats it into a csv file, and prints the info to the command line, ordered by price and name.

---------------------

To run:

## Install requirements

(Best done in a virtual environment)

    >>> pip3 install -r requirements.txt

## Download Chrome

Below instructions are for Linux (tested using Windows Subsystem for Linux).  If not using Linux/WSL, find an installation appropriate for your operating system.

https://www.linuxcapable.com/install-google-chrome-on-ubuntu-linux/

## Download Chromedriver

The chromedriver is used with Selenium to run a Chrome web browser for scraping.  Download the version corresponding to the version of your installed Chrome and operating system at the below links, unzip the file, and add the "chromedriver" file to the root of the folder.

https://sites.google.com/chromium.org/driver/?pli=1

https://googlechromelabs.github.io/chrome-for-testing/#stable

## Run Scraper

    >>> python3 run_scraper.py
