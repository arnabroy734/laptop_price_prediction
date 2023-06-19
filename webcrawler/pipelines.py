from urls_and_paths.urls import PRODUCT_BASE_URL
from  urls_and_paths.path import LINK_FILE, RAW_DATA_FILE, CRAWL_LOGS
from logs.logger import App_Logger
import csv
import re

class BufferProductLinks:
    """
    Description: This class is a pipeline of MainSpider
                 When MainSpider gets a product link the process_item method is called
    """
    def __init__(self):
        """
        Description: This is called during initialisation of CrawlProcess with MainSpider
                     A CSV file is created with designated name to store all the product links.
                     The CSV file has two columns 'PRODUCT_ID', 'PRODUCT_LINK'
                    
        """
        try:
            with open(LINK_FILE, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(['PRODUCT_ID', 'PRODUCT_LINK'])
                f.close()
            App_Logger().log(module="webcrawler", msg_type="success", message=f"File {LINK_FILE} successfully created")
    
        except Exception as e:
            App_Logger().log(module="webcrawler", msg_type="error", message=f"File {LINK_FILE} cannot be opened  - {e}")
            

    def process_item(self, item, spider):
        """
        Description: This function gets item object from MainSpider
                     PRODUCT_ID and PRODUCT_LINK are extracted from item object
                     Then those values are written to CSV file
        """
        try:
            long_url = item['link']
            pid = self.extract_product_id(long_url)
            short_url = self.shorten_url(pid)

            with open(LINK_FILE, 'a') as f:
                writer = csv.writer(f)
                writer.writerow([pid, short_url])
                f.close()
            return item
        except Exception as e:
            App_Logger().log(module="webcrawler", msg_type="error", message=f"product id and url cannot be saved to file {LINK_FILE}")
            

    def extract_product_id(self, url):
        """
        Description: Extracts pid from long product url 
        Parameters: long url of any flipkart product
        Example:
            Input:

            https://www.flipkart.com/asus-vivobook-16x-2023-intel-h-series-core-
            i5-12th-gen-16-gb-512-gb-ssd-windows-11-home-4-graphics-nvidia-geforce-rtx-3050-120-hz-k3605zc-mb542ws-creator-laptop
            /p/itmc4cc015344272?pid=COMGZMKF3UAXVYU9&
            lid=LSTCOMGZMKF3UAXVYU9B0SLXR&marketplace=FLIPKART&q=laptops&store=6bo%2Fb5g
            &srno=s_1_2&otracker=search&iid=en_3aLidsxA89CiW9kJTCp7WGdbSp7jvpEsG0X9yidB%2
            Bo%2FfCOWCbBOchZsHPdoTxQez%2BWJ4thWuHnqUMutIGgj%2BxQ%3D%3D&ssid=vk79u9uvn40000001686457519627&qH=c06ea84a1e3dc3c6

            Output:
            COMGZMKF3UAXVYU9

        """
        res = re.search(r'(?<=pid=)[a-z0-9A-Z]+(?=&)', url)
        return res.group()
    
    def shorten_url(self,pid):
        """
        Description: Creates short product url from product id
        Parameters: flipkart product id
        Example:
            Input: pid = COMGZMKF3UAXVYU9
            Output: https://www.flipkart.com/product/p/item?pid=COMGZMKF3UAXVYU9
        """
        return PRODUCT_BASE_URL+pid


class SaveProductDetails:
    """
    Description: This class is a pipeline of ProductDetailsSpider
                 When ProductDetailsSpider gets a product details the process_item method is called
    """
    def __init__(self):
        """
        Description: This is called during initialisation of CrawlProcess with ProductDetailsSpider
                     A CSV file called train.csv is created with designated name to store all the products with details                    
        """
        self.fieldnames = ['product_id', 'product_link', 'product_description', 'product_image',
                            'Processor_Name', 'Processor_Generation', 
                            'Clock_Speed', 'SSD_Capacity', 'RAM', 
                            'Graphic_Processor', 'Graphic_Memory',
                            'Touchscreen', 'Screen_Size', 'Screen_Resolution',
                            'Refresh_Rate', 'price']
        try:
            with open(RAW_DATA_FILE, 'w', newline='') as f:
                writer = csv.DictWriter(f,self.fieldnames)
                writer.writeheader()
                f.close()
            App_Logger().log(module="webcrawler", msg_type="success", message=f"File {RAW_DATA_FILE} opened successfully")
            
        except Exception as e:
            App_Logger().log(module="webcrawler", msg_type="error", message=f"File {RAW_DATA_FILE} cannot be opened  - {e}")



    def process_item(self, item, spider):
        """
        Description: This function gets item object from ProductDetailsSpider
                     Item is then written to train.csv file
        """
        try:
            if item is not None:
                with open(RAW_DATA_FILE, 'a', newline='') as f:
                    writer = csv.DictWriter(f, self.fieldnames)
                    writer.writerow(dict(item))
                    f.close()

        except Exception as e:
            App_Logger().log(module="webcrawler", msg_type="error", message=f"Product details cannot be saved to file {RAW_DATA_FILE}")

            