from typing import Any

from tests.qdk.operators.historical_sale_items import HistoricalSaleItemCreateModel, create_historical_sale_item
from tests.qdk.qa_requests import qa_post
from tests.qdk.types import TestContext
from tests.qdk.utils import generate_random_string
from util.configuration import get_global_configuration, populate_configuration_if_not_exists 

def test_posts_invalid_historical_sale_item_missing_fields() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    result = qa_post(context.api_url + "/historical_sale_items", {
 
    })

    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 6
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'product_id' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'missing'
    assert error[0]['msg'] == 'Field required'
      
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'historical_sale_id' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'missing'
    assert error[0]['msg'] == 'Field required'
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'sku' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'missing'
    assert error[0]['msg'] == 'Field required'
  
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'sale_count' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'missing'
    assert error[0]['msg'] == 'Field required'
     
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'sale_timestamp' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'missing'
    assert error[0]['msg'] == 'Field required'
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'total' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'missing'
    assert error[0]['msg'] == 'Field required'
 

def test_posts_invalid_historical_sale_item_bad_inputs() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    result = qa_post(context.api_url + "/historical_sale_items", {
        'product_id' : "not an id",  
        'historical_sale_id' : "never an id",
        'sale_timestamp' : 'not a valid datetime',
        'pos_sale_id' : generate_random_string(256), 
        'sku' : generate_random_string(256), 
        'pos_product_id' : generate_random_string(256), 
        'lot_identifier' : generate_random_string(256), 
        'sale_count' : 'not a valid float', 
        'unit_of_weight' : 'not a valid unit of weight',
        'weight_in_units' : 'not a valid float either',
        'sale_item_name' : generate_random_string(256),
        'tax' : 'not a valid integer',
        'discount' : 'also not a valid integer',
        'cost' : 'will it ever be a valid integer',
        'total' : 'no it will not ever be a valid integer',
        'sub_total' : 'ok cmon seriously with the invalid integer',
        
    })
 
    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 16
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'product_id' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'uuid_parsing'
    assert error[0]['msg'] == 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `n` at 1'

    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'historical_sale_id' in error['loc']] 
    assert len(error) == 1
    assert error[0]['type'] == 'uuid_parsing'    
    assert error[0]['msg'] == 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `n` at 1'
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'sale_timestamp' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'datetime_from_date_parsing' 
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'pos_sale_id' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'string_too_long'
    assert error[0]['msg'] == 'String should have at most 255 characters'  
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'pos_product_id' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'string_too_long'
    assert error[0]['msg'] == 'String should have at most 255 characters'  
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'sku' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'string_too_long'
    assert error[0]['msg'] == 'String should have at most 255 characters'  
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'lot_identifier' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'string_too_long'
    assert error[0]['msg'] == 'String should have at most 255 characters'  
  
    error: list[Any] = [error for error in errors['detail'] if  'body' in error['loc'] and 'total' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'int_parsing'
    assert error[0]['msg'] == 'Input should be a valid integer, unable to parse string as an integer'
    
    error: list[Any] = [error for error in errors['detail'] if  'body' in error['loc'] and 'sub_total' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'int_parsing'
    assert error[0]['msg'] == 'Input should be a valid integer, unable to parse string as an integer'

    error: list[Any] = [error for error in errors['detail'] if  'body' in error['loc'] and 'discount' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'int_parsing'
    assert error[0]['msg'] == 'Input should be a valid integer, unable to parse string as an integer'

    error: list[Any] = [error for error in errors['detail'] if  'body' in error['loc'] and 'tax' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'int_parsing'
    assert error[0]['msg'] == 'Input should be a valid integer, unable to parse string as an integer'
    
    error: list[Any] = [error for error in errors['detail'] if  'body' in error['loc'] and 'cost' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'int_parsing'
    assert error[0]['msg'] == 'Input should be a valid integer, unable to parse string as an integer'
    
    error: list[Any] = [error for error in errors['detail'] if  'body' in error['loc'] and 'sale_count' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'float_parsing'
    assert error[0]['msg'] == 'Input should be a valid number, unable to parse string as a number'
    
    error: list[Any] = [error for error in errors['detail'] if  'body' in error['loc'] and 'unit_of_weight' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'enum'
    assert error[0]['msg'] == "Input should be 'Milligrams', 'Grams', 'Kilograms', 'Pounds', 'Ounces', 'FluidOunces', 'Pints', 'Quarts', 'Gallons', 'Liters' or 'Milliliters'"
    
    error: list[Any] = [error for error in errors['detail'] if  'body' in error['loc'] and 'weight_in_units' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'float_parsing'
    assert error[0]['msg'] == 'Input should be a valid number, unable to parse string as a number'
    
    error: list[Any] = [error for error in errors['detail'] if  'body' in error['loc'] and 'sale_item_name' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'string_too_long'
    assert error[0]['msg'] == 'String should have at most 255 characters'
    
def test_posts_valid_historical_sale_item() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    create_historical_sale_item(
        context=context
    )
 
 