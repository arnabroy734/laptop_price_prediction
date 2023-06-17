from scrapy import Item, Field

class ProductLink(Item):
    link = Field()

class ProductDetails(Item):
    product_description = Field()
    product_image = Field()
    product_id = Field()
    product_link = Field()
    Processor_Name = Field()
    Processor_Generation = Field()
    Clock_Speed = Field()
    SSD_Capacity = Field()
    RAM = Field()
    Graphic_Processor = Field()
    Graphic_Memory = Field()
    Touchscreen = Field()
    Screen_Size = Field()
    Screen_Resolution = Field()
    Refresh_Rate = Field()
    price = Field()

    def initialise_null(self):
        
        self['product_description'] = None
        self['product_image'] = None
        self['product_id'] = None
        self['product_link'] = None
        self['Processor_Name'] = None 
        self['Processor_Generation'] = None 
        self['Clock_Speed'] = None 
        self['SSD_Capacity'] = None 
        self['RAM'] = None 
        self['Graphic_Processor'] = None 
        self['Graphic_Memory'] = None 
        self['Touchscreen'] = None 
        self['Screen_Size'] = None 
        self['Screen_Resolution'] = None 
        self['Refresh_Rate'] = None 
        self['price'] = None 
        return self



