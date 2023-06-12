import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from .spiders import MainSpider, ProductDetailsSpider
from .settings import *
import pandas as pd
from webcrawler.urls import LINK_FILE
import time

def scrape_product_links():
    """
    Description: Scrapes all product links from flipkart serach page with search key "laptops"
                 Store the product ids and links in productlinks.csv file
    """
    try:
        process = CrawlerProcess(settings=SETTING_MAIN_SPIDER)
        process.crawl(MainSpider)
        process.start()  # the script will block here until all crawling jobs are finished
    
    except:
        # TODO: Write logging in crawling product links
        pass

def scrape_product_details():
    """
    Description: Scrapes all the product links available in productlinks.csv
                 From every product extracts all relevant fields and store the file in data/train.csv file

    """
    try:
        links = pd.read_csv(LINK_FILE)
        urls = links.values[:,1]
        process = CrawlerProcess(settings=SETTING_PRODUCT_SPIDER)
        process.crawl(ProductDetailsSpider, links=list(urls))
        process.start()
    except Exception as e:
        # TODO: Write logging in crawling product links
        pass


   
    