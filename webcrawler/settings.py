from .pipelines import BufferProductLinks, SaveProductDetails

SETTING_MAIN_SPIDER = {
    "DOWNLOAD_DELAY" : 2,
    "ITEM_PIPELINES" : {BufferProductLinks: 300}
}

SETTING_PRODUCT_SPIDER = {
    "DOWNLOAD_DELAY" : 0.1,
    "ITEM_PIPELINES" : {SaveProductDetails: 300}
}