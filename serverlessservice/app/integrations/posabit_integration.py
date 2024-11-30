from datetime import datetime, timedelta
 
import json
from uuid import UUID

import requests
 
from integrations.common import ServiceCaller
from integrations.types import GenericInventoryObject
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
  
    def __init__(
        self,
        service_caller: ServiceCaller = ServiceCaller()
    ) -> None:
        self.service_caller = service_caller
            
            
    def get_all_pages_of_inventory_items(
        self,
        pos_integration_key: str,  
        simulator_response_id : UUID | None = None,
    ) -> list[PosabitInventoryObject]:
        
        running_list_of_inventory_items: list[PosabitInventoryObject] = []
    
        # note that if we want to restrict the date range, we need to add the following to the url:
        # q[updated_at_gt]={start_date.isoformat(timespec='milliseconds').replace('+00:00','Z')}&q[updated_at_lt]={end_date.isoformat(timespec='milliseconds').replace('+00:00','Z')}
         
        print("Posabit integration retrieving inventory data")
        
        results = self.service_caller.get(
            url = f"https://app.posabit.com/api/v2/venue/inventories", 
            headers = {"Authorization": f"Bearer {pos_integration_key}"},
            simulator_response_id = simulator_response_id
        ) 
       
        var = results.json()
        posabit_inventories =  PosabitInventoryResponse(**results.json())
        
        running_list_of_inventory_items += [PosabitInventoryObject(**item) for item in posabit_inventories.inventory]
        
        total_pages = posabit_inventories.total_pages or 1
        current_page = 2
        
        while current_page <= total_pages and simulator_response_id is None:
             
            next_page_of_results = self.service_caller.get(
                url = f"https://app.posabit.com/api/v2/venue/inventories", 
                headers = {"Authorization": f"Bearer {pos_integration_key}"},
                simulator_response_id = simulator_response_id
            ) 
                
            next_page_of_posabit_inventories =  PosabitInventoryResponse(**next_page_of_results.json())
            running_list_of_inventory_items += next_page_of_posabit_inventories.inventory
            current_page = next_page_of_posabit_inventories.current_page + 1
            total_pages = next_page_of_posabit_inventories.total_pages
                
        return running_list_of_inventory_items
        
    def get_inventory_snapshots(
        self,  
        integration_key: str,
        simulator_response_id: UUID | None = None
    ) -> list[GenericInventoryObject] | None:
        return_list: list[GenericInventoryObject] = [] 
        
        inventory_items = self.get_all_pages_of_inventory_items(integration_key, simulator_response_id = simulator_response_id)
         
        for inventory_item in inventory_items:
              
            samson_inventory_snapshot_item = self.convert_from_posabit_inventory_object_to_generic_inventory_object( 
                posabit_inventory_object= inventory_item
            )
            
            return_list.append(samson_inventory_snapshot_item)
        
        return return_list 

    def convert_from_posabit_inventory_object_to_generic_inventory_object(
        self,  
        posabit_inventory_object: PosabitInventoryObject, 
 
    ) -> GenericInventoryObject:
        return GenericInventoryObject( 
            sku = posabit_inventory_object.sku,
            stock_on_hand= posabit_inventory_object.quantity_on_hand,
            price = posabit_inventory_object.price,  
            product_name= posabit_inventory_object.name,
            listed_vendor = posabit_inventory_object.vendor,
            listed_brand = posabit_inventory_object.brand,
            listed_category = posabit_inventory_object.category,
        )  
    