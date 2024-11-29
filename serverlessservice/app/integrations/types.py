from datetime import datetime
from uuid import UUID


class GenericInventoryObject: 
    def __init__(
        self,         
        sku: str,
        stock_on_hand: int,
        price: int,    
        product_name: str | None = None,
        listed_vendor: str | None = None,
        listed_brand: str | None = None,
        listed_category: str | None = None,
    ) -> None: 
        self.sku = sku
            
        self.stock_on_hand = stock_on_hand
        self.price = price 
        self.product_name = product_name
        self.listed_vendor = listed_vendor
        self.listed_brand = listed_brand
        self.listed_category = listed_category