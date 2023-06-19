from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from .spiders import MainSpider, ProductDetailsSpider
from .settings import *
import pandas as pd
from urls_and_paths.path import LINK_FILE, RAW_DATA_FILE
from logs.logger import App_Logger
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer


def scrape_data():
    try:
        runner_prod_links = CrawlerRunner(SETTING_MAIN_SPIDER)
        runner_prod_details = CrawlerRunner(SETTING_PRODUCT_SPIDER)

        @defer.inlineCallbacks
        def crawl():
            yield runner_prod_links.crawl(MainSpider)
            num = pd.read_csv(LINK_FILE, encoding='unicode_escape').shape[0]
            App_Logger().log(module='webcrawler', msg_type='success', message=f'total {num} product links scraped and saved to file {LINK_FILE}')

            links = pd.read_csv(LINK_FILE)
            urls = links.values[:,1]
            yield runner_prod_details.crawl(ProductDetailsSpider, links=list(urls))
            num = pd.read_csv(RAW_DATA_FILE,encoding='unicode_escape').shape[0]
            App_Logger().log(module='webcrawler', msg_type='success', message=f'total {num} product details scraped and saved to file {RAW_DATA_FILE}')
            reactor.stop()


        crawl()
        reactor.run()  # the script will block here until the last crawl call is finished
    
    except Exception as e:
        App_Logger().log(module='webcrawler', msg_type='error', message=f'data scraping failed due to - {e}')
        raise Exception(e)
   
    