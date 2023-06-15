import scrapy
from urls_and_paths.urls import BASE_URL, START_URL, PRODUCT_BASE_URL
from .items import ProductLink, ProductDetails
from logs.logger import App_Logger
from urls_and_paths.path import CRAWL_LOGS

class MainSpider(scrapy.Spider):
    name = "main_spider"
    start_urls = [START_URL]

    def parse(self, response):
        """
        Description: This is an extension of method inside original scrapy.Spider class
                     This is a generator function. Output of this generator goes to next class in ITEM PIPELINE.
                     This method tries to extract Product link of flipkart search page. It takes the url from {start_urls} variable
                     After searching it recursively call same method with next page url.
        """
        try:
            product_links = response.css("._1fQZEK::attr(href)").getall()
            for link in product_links:
                product_link = ProductLink()
                product_link['link'] = BASE_URL + link
                yield product_link

        except Exception as e:
            pass
        
        try:
            nextpage = response.css("._1LKTO3::attr(href)").getall()
            if nextpage is not None:
                nextpage = BASE_URL + nextpage[-1]
                yield response.follow(nextpage, self.parse)

        except:
            pass


class ProductDetailsSpider(scrapy.Spider):
    name = "product_spider"

    def __init__(self, links, *args, **kwargs):
        """
        Paramaters: (start_urls) - links of product page to scrape details
        """
        super(ProductDetailsSpider, self).__init__(*args, **kwargs)
        self.start_urls = links

    def parse(self, response):
        """
        Description: This is an extension of method inside original scrapy.Spider class
                     This is a generator function. Output of this generator goes to next class in ITEM PIPELINE.
                     This method tries to extract product details from product page. It takes the url from {start_urls} variable
        """
        product = ProductDetails().initialise_null() # Create a new product with all fields null
        product['product_link'] = response.request.url
        product['product_id'] = product['product_link'][len(PRODUCT_BASE_URL) : ]

        price = response.css("._30jeq3._16Jk6d::text").get()
        product["price"] = price[1:]

        feature_rows = response.css("._1s_Smc")
        for row in feature_rows:
            feature_name = row.css("._1hKmbr::text").get()
            feature_val = row.css("._21lJbe::text").get()
            
            if feature_name == "Processor Name":
                product["Processor_Name"] = feature_val

            elif feature_name == "Processor Generation":
                product["Processor_Generation"] = feature_val

            elif feature_name == "Clock Speed":
                product["Clock_Speed"] = feature_val

            elif feature_name == "SSD Capacity":
                product["SSD_Capacity"] = feature_val

            elif feature_name == "RAM":
                product["RAM"] = feature_val
            
            elif feature_name == "Graphic Processor":
                product["Graphic_Processor"] = feature_val

            elif feature_name == 'Dedicated Graphic Memory Capacity':
                product["Graphic_Memory"] = feature_val

            elif feature_name == "Touchscreen":
                product["Touchscreen"] = feature_val
     
            elif feature_name == "Screen Size":
                product["Screen_Size"] = feature_val

            elif feature_name == "Screen Resolution":
                product["Screen_Resolution"] = feature_val

            elif feature_name == "Refresh Rate":
                product["Refresh_Rate"] = feature_val

        yield product



 
    
    
    
    
    
    
    
    
    
    
   