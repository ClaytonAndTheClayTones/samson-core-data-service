import datetime

from requests import Response  
from tests.qdk.operators.pos_integrations import PosIntegrationCreateModel, PosIntegrationModel, create_pos_integration
from tests.qdk.operators.retailers import RetailerCreateModel, RetailerModel, create_retailer
from tests.qdk.qa_requests import qa_get, qa_patch, qa_post
from tests.qdk.types import PagedResponseItemList, PagingRequestModel, PagingResponseModel, RequestOperators, TestContext
from tests.qdk.utils import assert_object_was_updated, assert_objects_are_equal, copy_object_when_appropriate, generate_random_string
  
class RetailerLocationCreateModel():  

    def __init__(self,
                retailer_id: str | None = None,
                retailer: RetailerCreateModel | None = None, 
                pos_integration_id: str | None = None,
                pos_integration: PosIntegrationCreateModel | None = None,
                create_pos_integration_if_null: bool | None = False,
                contact_email: str | None = None,
                contact_phone: str | None = None,
                location_city: str | None = None,
                location_state: str | None = None,
                location_country: str | None = None,
                name: str | None = None) -> None:
        
        self.retailer_id = retailer_id
        self.retailer = retailer
        self.pos_integration_id = pos_integration_id
        self.pos_integration = pos_integration
        self.create_pos_integration_if_null = create_pos_integration_if_null
        
        self.contact_email = contact_email
        self.contact_phone = contact_phone
        self.location_city = location_city
        self.location_state = location_state
        self.location_country = location_country

        self.name = name

class RetailerLocationModel():  

    def __init__(self, 
                id: str, 
                created_at: datetime.datetime | None = None, 
                updated_at: datetime.datetime | None = None, 
                retailer_id: str | None = None,
                retailer: RetailerModel | None = None,
                pos_integration_id: str | None = None,
                pos_integration: PosIntegrationModel | None = None,
                name: str | None = None,
                contact_email: str | None = None,
                contact_phone: str | None = None,
                location_city: str | None = None,
                location_state: str | None = None,
                location_country: str | None = None) -> None:
                
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
        self.retailer_id = retailer_id
        self.retailer = retailer
        self.pos_integration_id = pos_integration_id
        self.pos_integration = pos_integration
        
        self.name = name
                
        self.contact_email = contact_email
        self.contact_phone = contact_phone
        self.location_city = location_city
        self.location_state = location_state
        self.location_country = location_country


class RetailerLocationSearchModel(PagingRequestModel):  

    def __init__(self, 
                ids: str | None = None,  
                retailer_ids: str | None = None,  
                pos_integration_ids: str | None = None,  
                name: str | None = None,
                name_like: str | None = None,  
                location_city: str | None = None,
                location_state: str | None = None,
                location_country: str | None = None,
                page: int | None = None,
                page_length: int | None = None,
                is_sort_descending: bool | None = None,
                sort_by: str | None = None) -> None:
        super().__init__(
            page = page,
            page_length = page_length,
            is_sort_descending = is_sort_descending,
            sort_by = sort_by
        )
        
        self.ids = ids 
        self.retailer_ids = retailer_ids 
        self.pos_integration_ids = pos_integration_ids 
        self.name = name
        self.name_like = name_like 
        self.location_city = location_city 
        self.location_state = location_state 
        self.location_country = location_country 
        
class RetailerLocationUpdateModel():  

    def __init__(self, 
                pos_integration_id: str | None = None, 
                name: str | None = None,
                contact_email: str | None = None,
                contact_phone: str | None = None,
                location_city: str | None = None,
                location_state: str | None = None,
                location_country: str | None = None,) -> None: 
        
        self.pos_integration = pos_integration_id
        self.name = name
        self.contact_email = contact_email
        self.contact_phone = contact_phone
        self.location_city = location_city
        self.location_state = location_state
        self.location_country = location_country
 
def mint_default_retailer_location(
    context: TestContext, 
    overrides: RetailerLocationCreateModel | None = None, 
    request_operators: RequestOperators | None = None
) -> RetailerLocationCreateModel: 
    
    overrides = overrides or RetailerLocationCreateModel()

    if(overrides.retailer_id is None):

        new_retailer = create_retailer(context, overrides.retailer, request_operators = request_operators)
        overrides.retailer_id = new_retailer.id

        del overrides.retailer
    
    
    if(overrides.pos_integration_id is None and overrides.create_pos_integration_if_null):

        new_pos_integration = create_pos_integration(context, overrides.pos_integration, request_operators = request_operators)
        overrides.pos_integration_id = new_pos_integration.id

        del overrides.pos_integration

    random_string = generate_random_string()
    
    default_retailer_location: RetailerLocationCreateModel = RetailerLocationCreateModel(
        name = random_string + '_name', 
        location_city = 'cityville',
        location_state = 'north new stateplace',
        location_country = 'CK',
        contact_email = 'madeupemailaddress@example.com', 
        contact_phone = '+12345678901'
    )

    copy_object_when_appropriate(default_retailer_location, overrides)
     
    return default_retailer_location

def create_retailer_location(
        context: TestContext,
        overrides: RetailerLocationCreateModel | None = None, 
        request_operators: RequestOperators | None = None,
        allow_failures: bool = False
        ):
    
    post_object = mint_default_retailer_location(context = context, overrides = overrides, request_operators = request_operators)

    result = qa_post(context.api_url + "/retailer_locations", post_object, request_operators)

    if(allow_failures == False):
        assert result.status_code == 201
 
        result_dict = result.json()

        assert_objects_are_equal(result_dict, post_object.__dict__, ["id", "retailer_location", "created_at", "updated_at"])

        assert result_dict['id'] is not None
        assert result_dict['created_at'] is not None
        assert result_dict['updated_at'] is None
     
    return_object = RetailerLocationModel(**result.json())
    
    return return_object 

def get_retailer_location_by_id(
        context: TestContext, 
        id: str,
        request_operators: RequestOperators | None = None,
        allow_failures: bool = False
        ):

    url = f"{context.api_url}/retailer_locations/{id}"
    
    result = qa_get(url)
 
    return_object = RetailerLocationModel(**result.json())
    
    return return_object 

def get_retailer_locations(
        context: TestContext, 
        search_model: RetailerLocationSearchModel | None,
        request_operators: RequestOperators | None = None 
    ) -> PagedResponseItemList[RetailerLocationModel]: 

    url: str = f"{context.api_url}/retailer_locations"
    
    result: Response = qa_get(
        url = url, 
        query_params = search_model if search_model is not None else {},
        request_operators = request_operators
    )
    
    result_dict = result.json()

    return_paging_object = PagingResponseModel(**result_dict['paging'])
     
    return_items: list[RetailerLocationModel] = [RetailerLocationModel(**obj) for obj in result_dict['items']]

    return_object = PagedResponseItemList[RetailerLocationModel](
        items = return_items, paging = return_paging_object
    )
    
    return return_object 


def update_retailer_location(
        context: TestContext,
        id: str,
        update_model: RetailerLocationUpdateModel | None = None, 
        request_operators: RequestOperators | None = None,
        allow_failures: bool = False
        ):
    
    original_object: RetailerLocationModel = get_retailer_location_by_id(context, id, request_operators)

    result = qa_patch(f"{context.api_url}/retailer_locations/{id}", update_model, request_operators)

    if(allow_failures == False):
        assert result.status_code == 200
 
        result_dict = result.json()

        assert_object_was_updated(original_object.__dict__, update_model.__dict__, result_dict, ["updated_at"])
 
        assert result_dict['updated_at'] is not None
    
    return_object = RetailerLocationModel(**result.json())
    
    return return_object 
    

    
