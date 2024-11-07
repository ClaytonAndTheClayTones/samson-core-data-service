from typing import Any
 
from tests.qdk.qa_requests import qa_post
from tests.qdk.types import TestContext
from tests.qdk.utils import generate_random_string
from util.configuration import get_global_configuration, populate_configuration_if_not_exists 
from tests.qdk.operators.inventory_intake_batch_jobs import InventoryIntakeBatchJobCreateModel, create_inventory_intake_batch_job

def test_posts_invalid_inventory_intake_batch_job_missing_fields() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    result = qa_post(context.api_url + "/inventory_intake_batch_jobs", {
 
    })

    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 1
 
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'start_time' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'missing'
    assert error[0]['msg'] == 'Field required'
  

def test_posts_invalid_inventory_intake_batch_job_bad_inputs() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    result = qa_post(context.api_url + "/inventory_intake_batch_jobs", {
        
        'start_time' : 'not a valid time', 
        'end_time' : 'also not a valid time',
        'status_details' : 'not a valid json object',
        'status' : 'not a valid status'
    })
 
    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 4
 
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'start_time' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'datetime_from_date_parsing'
    assert error[0]['msg'] == 'Input should be a valid datetime or date, invalid character in year'
 
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'end_time' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'datetime_from_date_parsing'
    assert error[0]['msg'] == 'Input should be a valid datetime or date, invalid character in year'

    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'status_details' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'dict_type'
    assert error[0]['msg'] == 'Input should be a valid dictionary'
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'status' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'enum'
    assert error[0]['msg'] == "Input should be 'Requested', 'Processing', 'Complete' or 'Failed'"
    
def test_posts_valid_inventory_intake_batch_job() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    create_inventory_intake_batch_job(context)  
    
def test_posts_valid_inventory_intake_batch_job_defaulted_values() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    create_inventory_intake_batch_job(
        context,
        InventoryIntakeBatchJobCreateModel(status=None, status_details=None)
    )  
 
 