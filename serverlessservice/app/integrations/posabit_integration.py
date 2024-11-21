from datetime import datetime, timedelta
 
import json
from uuid import UUID

import requests
 
from models.inventory_intake_job_model import InventoryIntakeJobModel
from models.inventory_product_snapshot_model import InventoryProductSnapshotCreateModel, InventoryProductSnapshotModel, InventoryProductSnapshotSearchModel
from models.pos_integration_model import PosIntegrationModel
 
from models.product_model import ProductCreateModel, ProductModel, ProductVendorConfirmationStatuses
from models.retailer_location_model import RetailerLocationModel 

class PosabitInventoryObject:
    def __init__(self, 
        id: int | None = None, 
        product_id: int | None = None,
        name: str | None = None,
        unit: str | None = None,
        price: int | None = None,
        med_price: int | None = None,
        last_price: int | None = None,
        quantity_on_hand: str | None = None,
        sellable_quantity: str | None = None,
        ecomm_quantity: str | None = None,
        vendor: str | None = None,
        vendor_license: str | None = None,
        brand: str | None = None,
        category: str | None = None,
        compliance_type: str | None = None,
        flower_type: str | None = None,
        concentrate_type: str | None = None,
        product_type: str | None = None,
        product_family: str | None = None,
        tags: list[str] | None = None, 
        description: str | None = None,
        description_html: str | None = None,
        image: list[str] | None = None,
        active: bool | None = None,
        bulk_item: bool | None = None,
        strain: str | None = None,
        thc_measure: str | None = None,
        cbd_measure: str | None = None,
        sku: str | None = None,
        discountable: bool | None = None,
        tier_name: str | None = None,
        doh_compliant: bool | None = None,
        created_at: datetime | None = None,
        updated_at:  datetime | None= None,
        rooms: list[tuple[str,str]] | None = None
    ) -> None:
        
        self.id = id
        self.product_id = product_id
        self.name = name
        self.unit = unit
        self.price = price
        self.med_price = med_price
        self.last_price = last_price
        self.quantity_on_hand = quantity_on_hand
        self.sellable_quantity = sellable_quantity
        self.ecomm_quantity = ecomm_quantity
        self.vendor = vendor
        self.vendor_license = vendor_license
        self.brand = brand
        self.category = category
        self.compliance_type = compliance_type
        self.flower_type = flower_type
        self.concentrate_type = concentrate_type
        self.product_type = product_type
        self.product_family = product_family
        self.tags = tags
        self.description = description
        self.description_html = description_html
        self.image = image
        self.active = active
        self.bulk_item = bulk_item
        self.strain = strain
        self.thc_measure = thc_measure
        self.cbd_measure = cbd_measure
        self.sku = sku
        self.discountable = discountable
        self.tier_name = tier_name
        self.doh_compliant = doh_compliant
        self.created_at = created_at
        self.updated_at = updated_at
        self.rooms = rooms        
 
class PosabitInventoryResponse:
    def __init__(
        self,
        total_records: int,
        current_page: int,
        total_pages: int,
        per_page: int,
        inventory: list[PosabitInventoryObject] | None = None,
    ) -> None:
        self.total_records = total_records
        self.current_page = current_page
        self.total_pages = total_pages
        self.per_page = per_page
         
        self.inventory = inventory
        
class PosabitIntegration:
  
    def get_all_pages_of_inventory_items(
        self,
        pos_integration_key: str, 
        start_date : datetime,
        end_date : datetime
    ) -> list[PosabitInventoryObject]:
        
        running_list_of_inventory_items: list[PosabitInventoryObject] = []
 
        url = f"https://app.posabit.com/api/v2/venue/inventories?q[updated_at_gt]={start_date.isoformat(timespec='milliseconds').replace('+00:00','Z')}&q[updated_at_lt]={end_date.isoformat(timespec='milliseconds').replace('+00:00','Z')}"
        
        print("Posabit integration calling url: " + url)
        
        posabit_results = requests.get(
            url,
            headers = {
                "Authorization": f"Bearer {pos_integration_key}"
            }
        )
       
        posabit_inventories =  PosabitInventoryResponse(**posabit_results.json())
        
        running_list_of_inventory_items += [PosabitInventoryObject(**item) for item in posabit_inventories.inventory]
        
        total_pages = posabit_inventories.total_pages
        current_page = 2
        
        while current_page <= total_pages:
             
            url = f"https://app.posabit.com/api/v2/venue/inventories?q[updated_at_gt]={start_date.isoformat()}&q[updated_at_lt]={end_date.isoformat()}&page={current_page}"
            
            print("Posabit integration calling url: " + url)
                
            next_page_of_results = requests.get(
                url, 
                headers = {
                    "Authorization": f"Bearer {pos_integration_key}"
                }
            )  
            
            next_page_of_posabit_inventories =  PosabitInventoryResponse(**next_page_of_results.json())
            running_list_of_inventory_items += next_page_of_posabit_inventories.inventory
            current_page = next_page_of_posabit_inventories.current_page + 1
            total_pages = next_page_of_posabit_inventories.total_pages
            
        return running_list_of_inventory_items
        
    def get_inventory_snapshot(
        self, 
        job: InventoryIntakeJobModel, 
        retailer_location: RetailerLocationModel,
        pos_integration: PosIntegrationModel
    ) -> list[InventoryProductSnapshotCreateModel] | None:
        return_list: list[InventoryProductSnapshotCreateModel] = [] 
        
        start_date : datetime = datetime(
            year=job.snapshot_hour.year,
            month=job.snapshot_hour.month,
            day=job.snapshot_hour.day,
            hour=job.snapshot_hour.hour,
            minute=0,
            second=0,
            microsecond=0,
        )
        
        end_date : datetime = start_date + timedelta(hours=1,milliseconds= -1)
         
        inventory_items = self.get_all_pages_of_inventory_items(pos_integration.key, start_date, end_date)
         
        for inventory_item in inventory_items:
            
            connected_samson_product = self.check_for_recognized_product_and_add_if_none(inventory_item=inventory_item, retailer_location=retailer_location)
            
            samson_inventory_snapshot_item = self.convert_from_posabit_inventory_object_to_inventory_product_snapshot_create_model(
                job= job,
                posabit_inventory_object= inventory_item, 
                retailer_location=retailer_location,
                product_model=connected_samson_product
            )
            
            return_list.append(samson_inventory_snapshot_item)
        
        return return_list 

    def convert_from_posabit_inventory_object_to_inventory_product_snapshot_create_model(
        self, 
        job: InventoryIntakeJobModel,
        posabit_inventory_object: PosabitInventoryObject,
        retailer_location: RetailerLocationModel,
        product_model: ProductModel,
 
    ) -> InventoryProductSnapshotCreateModel:
        return InventoryProductSnapshotCreateModel(
            inventory_intake_job_id= job.id,
            product_id= product_model.id,
            retailer_location_id = retailer_location.id, 
            snapshot_hour = job.snapshot_hour,
            sku = posabit_inventory_object.sku,
            stock_on_hand= posabit_inventory_object.quantity_on_hand,
            price = posabit_inventory_object.price, 
            vendor_id = product_model.vendor_id,
            retailer_id= retailer_location.retailer_id
        ) 