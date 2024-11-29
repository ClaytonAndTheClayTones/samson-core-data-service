from typing import Any

from tests.qdk.operators.inventory_intake_jobs import InventoryIntakeJobCreateModel, create_inventory_intake_job, get_inventory_intake_job_by_id, run_inventory_intake_job 
from tests.qdk.operators.pos_simulator_responses import PosSimulatorResponseCreateModel
from tests.qdk.operators.products import ProductSearchModel, get_products
from tests.qdk.types import RequestOperators, TestContext 
from tests.qdk.utils import generate_random_string
from util.configuration import get_global_configuration, populate_configuration_if_not_exists 

def test_intakes_new_products_when_not_recognized() -> None:
     
    populate_configuration_if_not_exists() 
     
    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    random_marker = generate_random_string(12, charset="abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    # Arrange
    
    created_job = create_inventory_intake_job(
        context,
        overrides=InventoryIntakeJobCreateModel( 
            create_simulator_response_if_null=True,
            simulator_response=PosSimulatorResponseCreateModel(
                action_type="GetInventorySnapshots",
                response_body=get_new_products_test_json(random_marker)
            )
        ),
        request_operators=RequestOperators(hydration_properties=["simulator_response"])
    )
    
    # Act
            
    job_run_result = run_inventory_intake_job(
        context,
        id=created_job.id
    )
    
    # Assert Job was run
    
    run_job = get_inventory_intake_job_by_id(
        context,
        id=created_job.id,
        request_operators=RequestOperators(hydration_properties=["simulator_response"])
    )
    
    assert run_job.status == "Complete"
    
    # Assert three new products were created
    product_search_model_1 = ProductSearchModel(
        name=f"{random_marker} - Product Name 1"
    )
    
    product_1 = get_products(context, product_search_model_1)
    
    assert product_1.items is not None
    assert len(product_1.items) == 1
    assert product_1.items[0].name == f"{random_marker} - Product Name 1"
    assert product_1.items[0].id is not None
    assert product_1.items[0].sku == f"{random_marker}-1111-1111"
    assert product_1.items[0].referring_retailer_location_id == created_job.retailer_location_id
    assert product_1.items[0].retailer_id == created_job.retailer_id
    assert product_1.items[0].vendor_confirmation_status == "Candidate"
    
    product_search_model_2 = ProductSearchModel(
        name=f"{random_marker} - Product Name 2"
    )
    
    product_2 = get_products(context, product_search_model_2)
    
    assert product_2.items is not None
    assert len(product_2.items) == 1
    assert product_2.items[0].name == f"{random_marker} - Product Name 2"
    assert product_2.items[0].id is not None
    assert product_2.items[0].sku == f"{random_marker}-2222-2222"
    assert product_2.items[0].referring_retailer_location_id == created_job.retailer_location_id
    assert product_2.items[0].retailer_id == created_job.retailer_id
    assert product_2.items[0].vendor_confirmation_status == "Candidate"
    
    product_search_model_3 = ProductSearchModel(
        name=f"{random_marker} - Product Name 3"
    )
    
    product_3 = get_products(context, product_search_model_3)
    
    assert product_3.items is not None
    assert len(product_3.items) == 1    
    assert product_3.items[0].name == f"{random_marker} - Product Name 3"
    assert product_3.items[0].id is not None
    assert product_3.items[0].sku == f"{random_marker}-3333-3333"
    assert product_3.items[0].referring_retailer_location_id == created_job.retailer_location_id
    assert product_3.items[0].retailer_id == created_job.retailer_id
    assert product_3.items[0].vendor_confirmation_status == "Candidate"
    
def get_new_products_test_json(marker: str) -> dict[str, Any]:

    return {
        "inventory": [
        { 
            "name": f"{marker} - Product Name 1", 
            "price": 1000, 
            "quantity_on_hand": "11.0", 
            "vendor": "Vendor 1", 
            "brand": "Test Brand 1",
            "category": "Test Category 1", 
            "sku": f"{marker}-1111-1111",
        },
        {
            "name": f"{marker} - Product Name 2", 
            "price": 2000, 
            "quantity_on_hand": "22.0", 
            "vendor": "Vendor 2", 
            "brand": "Test Brand 2",
            "category": "Test Category 2", 
            "sku": f"{marker}-2222-2222",
        },
        {
            "name": f"{marker} - Product Name 3", 
            "price": 3000, 
            "quantity_on_hand": "33.0", 
            "vendor": "Vendor 3", 
            "brand": "Test Brand 3",
            "category": "Test Category 3", 
            "sku": f"{marker}-3333-3333",
        }]
    }