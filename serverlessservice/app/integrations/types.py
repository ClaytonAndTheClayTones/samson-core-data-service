from datetime import datetime

from models.historical_sale_item_model import ProductUnitOfMeasurements
 
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

class GenericHistoricalSaleItemObject: 
    def __init__(
        self, 
        sku: str,
        sale_count: float,
        sale_timestamp: datetime, 
        total: int,   
        sale_item_name: str | None = None,
        lot_identifier: str | None = None,
        pos_sale_id: str | None = None,
        pos_product_id: str | None = None,
        unit_of_weight: ProductUnitOfMeasurements | None = None,
        weight_in_units: float | None = None,
        sub_total: int | None = None,
        discount: int | None = None,
        tax: int | None = None,
        cost : int | None = None,
    ) -> None: 
        
        self.sku = sku
        self.sale_count = sale_count
        self.sale_timestamp = sale_timestamp
        self.total = total
        self.sale_item_name = sale_item_name
        self.lot_identifier = lot_identifier
        self.pos_sale_id = pos_sale_id
        self.pos_product_id = pos_product_id
        self.unit_of_weight = unit_of_weight
        self.weight_in_units = weight_in_units
        self.sub_total = sub_total
        self.discount = discount
        self.tax = tax
        self.cost = cost

class GenericHistoricalSaleObject: 
    def __init__(
        self, 
        pos_sale_id: str,
        sale_timestamp: datetime, 
        total: float, 
        sub_total: float | None = None,
        discount: float | None = None,
        tax: float | None = None,
        cost: float | None = None,
        sale_items: list[GenericHistoricalSaleItemObject] | None = None
    ) -> None: 
        
        self.pos_sale_id = pos_sale_id
        self.sale_timestamp = sale_timestamp
        self.total = total 
        self.sub_total = sub_total
        self.discount = discount
        self.tax = tax
        self.cost = cost
        self.sale_items = sale_items or []
        