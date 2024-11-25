from datetime import datetime
from uuid import UUID


class GenericInventoryObject: 
    def __init__(
        self,         
        sku: str,
        stock_on_hand: int,
        price: int,    
    ) -> None: 
        self.sku = sku
            
        self.stock_on_hand = stock_on_hand
        self.price = price 