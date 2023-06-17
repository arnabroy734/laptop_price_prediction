from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from .spiders import MainSpider, ProductDetailsSpider
from .settings import *
import pandas as pd
from urls_and_paths.path import LINK_FILE, CRAWL_LOGS
from logs.logger import App_Logger
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer

# def scrape_product_links():
#     """
#     Description: Scrapes all product links from flipkart serach page with search key "laptops"
#                  Store the product ids and links in productlinks.csv file
#     """
#     try:
#         process = CrawlerProcess(settings=SETTING_MAIN_SPIDER)
#         process.crawl(MainSpider)
#         process.start()  # the script will block here until all crawling jobs are finished
#         App_Logger().log(CRAWL_LOGS, "crawler.py:  Product links scraped successfully")
#         process.stop()
    
#     except Exception as e:
#         App_Logger().log(CRAWL_LOGS, f"crawler.py:  Error in product link scraping - {str(e)}")
#         pass

# def scrape_product_details():
#     """
#     Description: Scrapes all the product links available in productlinks.csv
#                  From every product extracts all relevant fields and store the file in data/train.csv file

#     """
#     try:
#         links = pd.read_csv(LINK_FILE)
#         urls = links.values[:,1]
#         process = CrawlerProcess(settings=SETTING_PRODUCT_SPIDER)
#         process.crawl(ProductDetailsSpider, links=list(urls))
#         process.start()
#         App_Logger().log(CRAWL_LOGS, "crawler.py:  Product details scraped successfully")
#         process.stop()
#     except Exception as e:
#         App_Logger().log(CRAWL_LOGS, f"crawler.py:  Error in product details scraping - {str(e)}")
#         pass


def scrape_data():
    try:
        runner_prod_links = CrawlerRunner(SETTING_MAIN_SPIDER)
        runner_prod_details = CrawlerRunner(SETTING_PRODUCT_SPIDER)

        @defer.inlineCallbacks
        def crawl():
            yield runner_prod_links.crawl(MainSpider)
            App_Logger().log(CRAWL_LOGS, "crawler.py:  Product links scraped successfully")

            links = pd.read_csv(LINK_FILE)
            urls = links.values[:,1]
            yield runner_prod_details.crawl(ProductDetailsSpider, links=list(urls))
            App_Logger().log(CRAWL_LOGS, "crawler.py:  Product details scraped successfully")
            reactor.stop()


        crawl()
        reactor.run()  # the script will block here until the last crawl call is finished
    
    except Exception as e:
        App_Logger().log(CRAWL_LOGS, f"crawler.py:  Error in data scraping {e}")
   
    