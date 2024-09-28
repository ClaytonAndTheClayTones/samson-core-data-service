import datetime
from typing import Any, Self

from requests import Response 
from tests.qdk.operators.retailers import RetailerCreateModel, create_retailer
from tests.qdk.qa_requests import qa_get, qa_patch, qa_post
from tests.qdk.types import PagedResponseItemList, PagingResponseModel, PagingRequestModel, RequestOperators, TestContext
from tests.qdk.utils import assert_object_was_updated, assert_objects_are_equal, copy_object_when_appropriate, generate_random_string
 
class VendorCreateModel():  

    def __init__(self,
                unregistered_vendor_retailer_id: str | None = None,
                unregistered_vendor_retailer: RetailerCreateModel | None = None,
                create_unregistered_vendor_retailer_if_null: bool | None = False,
                registered_replacement_vendor_id: str | None = None,
                registered_replacement_vendor : Self | None = None,
                create_registered_replacement_vendor_if_null: bool | None = False,
                name: str | None = None,
                is_registered: bool | None = None,
                contact_email: str | None = None,
                contact_phone: str | None = None,
                hq_city: str | None = None,
                hq_state: str | None = None,
                hq_country: str | None = None) -> None: 
        
        self.name = name 
        self.unregistered_vendor_retailer_id = unregistered_vendor_retailer_id 
        self.unregistered_vendor_retailer = unregistered_vendor_retailer 
        self.create_unregistered_vendor_retailer_if_null = create_unregistered_vendor_retailer_if_null
        self.registered_replacement_vendor_id = registered_replacement_vendor_id 
        self.registered_replacement_vendor = registered_replacement_vendor 
        self.create_registered_replacement_vendor_if_null = create_registered_replacement_vendor_if_null 
        self.is_registered = is_registered 
        self.contact_email = contact_email
        self.contact_phone = contact_phone
        self.hq_city = hq_city
        self.hq_state = hq_state
        self.hq_country = hq_country  
        
class VendorUpdateModel():  

    def __init__(self,
                name: str | None = None,
                is_registered: bool | None = None,
                contact_email: str | None = None,
                contact_phone: str | None = None,
                hq_city: str | None = None,
                hq_state: str | None = None,
                hq_country: str | None = None) -> None:
        
        self.name = name
        self.is_registered = is_registered
        self.contact_email = contact_email
        self.contact_phone = contact_phone
        self.hq_city = hq_city
        self.hq_state = hq_state
        self.hq_country = hq_country 

class VendorModel():  

    def __init__(self, 
                id: str, 
                name: str,
                registered_replacement_vendor_id: str,
                unregistered_vendor_retailer_id: str,
                is_registered: str,
                created_at: datetime.datetime,
                contact_email: str | None = None, 
                contact_phone: str | None = None, 
                hq_city: str | None = None,
                hq_state: str | None = None,
                hq_country: str | None = None,
                updated_at: datetime.datetime | None = None) -> None:
        
        self.id = id
        self.registered_replacement_vendor_id = registered_replacement_vendor_id
        self.unregistered_vendor_retailer_id = unregistered_vendor_retailer_id
        self.is_registered = is_registered
        self.created_at = created_at
        self.updated_at = updated_at
        self.name = name
        self.contact_email = contact_email
        self.contact_phone = contact_phone
        self.hq_city = hq_city
        self.hq_state = hq_state
        self.hq_country = hq_country
        
class VendorSearchModel(PagingRequestModel):  

    def __init__(self, 
                ids: str | None = None, 
                registered_replacement_vendor_ids: str | None = None, 
                unregistered_vendor_retailer_ids: str | None = None,  
                is_registered: bool | None = None,  
                name: str | None = None,
                name_like: str | None = None,
                hq_city: str | None = None,
                hq_state: str | None = None,
                hq_country: str | None = None,
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
        self.registered_replacement_vendor_ids = registered_replacement_vendor_ids 
        self.unregistered_vendor_retailer_ids = unregistered_vendor_retailer_ids 
        self.name = name
        self.name_like = name_like
        self.is_registered = is_registered
        self.hq_city = hq_city
        self.hq_state = hq_state
        self.hq_country = hq_country
 
def mint_default_vendor(
    context: TestContext, 
    overrides: VendorCreateModel | None = None, 
    request_operators: RequestOperators | None = None
) -> VendorCreateModel: 
    random_string = generate_random_string()

    overrides = overrides or VendorCreateModel()
     
    if(overrides.unregistered_vendor_retailer_id is None and overrides.create_unregistered_vendor_retailer_if_null):

        new_retailer = create_retailer(context, overrides.unregistered_vendor_retailer, request_operators = request_operators)
        overrides.unregistered_vendor_retailer_id = new_retailer.id

        del overrides.unregistered_vendor_retailer
        del overrides.create_unregistered_vendor_retailer_if_null
        
    if(overrides.registered_replacement_vendor_id is None and overrides.create_registered_replacement_vendor_if_null):

        new_vendor = create_vendor(context, overrides.registered_replacement_vendor, request_operators = request_operators)
        overrides.registered_replacement_vendor_id = new_vendor.id

        del overrides.registered_replacement_vendor
        del overrides.create_registered_replacement_vendor_if_null
    
    default_vendor: VendorCreateModel = VendorCreateModel(
        name = random_string + '_name',
        hq_city = 'cityville',
        hq_state = 'north new stateplace',
        hq_country = 'CK',
        contact_email = 'madeupemailaddress@example.com',
        contact_phone = '+12345678901'
    )
        
    copy_object_when_appropriate(default_vendor, overrides)
     
    return default_vendor

def create_vendor(
        context: TestContext,
        overrides: VendorCreateModel | None = None, 
        request_operators: RequestOperators | None = None,
        allow_failures: bool = False
        ) -> VendorModel:
    
    post_object: VendorCreateModel = mint_default_vendor(context = context, overrides = overrides, request_operators = request_operators)

    result: Response = qa_post(context.api_url + "/vendors", post_object, request_operators)

    if(allow_failures == False):
        assert result.status_code == 201
 
        result_dict = result.json()

        assert_objects_are_equal(result_dict, post_object.__dict__, ["id", "created_at", "updated_at", "is_registered"])

        assert result_dict['id'] is not None
        assert result_dict['created_at'] is not None
        assert result_dict['updated_at'] is None
        
        if(post_object.is_registered is None):
            assert result_dict['is_registered'] is False
        else:
            assert result_dict['is_registered'] == post_object.is_registered
    
    return_object = VendorModel(**result.json())
    
    return return_object 
 
def get_vendor_by_id(
        context: TestContext, 
        id: str,
        request_operators: RequestOperators | None = None,
        allow_failures: bool = False
        ) -> VendorModel:

    url: str = f"{context.api_url}/vendors/{id}"
    
    result: Response = qa_get(url)
     
    return_object = VendorModel(**result.json())
    
    return return_object 

def get_vendors(
        context: TestContext, 
        search_model: VendorSearchModel | None,
        request_operators: RequestOperators | None = None 
    ) -> PagedResponseItemList[VendorModel]: 

    url: str = f"{context.api_url}/vendors"
    
    result: Response = qa_get(
        url = url, 
        query_params = search_model if search_model is not None else {},
        request_operators = request_operators
    )
    
    result_dict = result.json()

    return_paging_object = PagingResponseModel(**result_dict['paging'])
     
    return_items: list[VendorModel] = [VendorModel(**obj) for obj in result_dict['items']]

    return_object = PagedResponseItemList[VendorModel](
        items = return_items, paging = return_paging_object
    )
    
    return return_object 

def update_vendor(
        context: TestContext,
        id: str,
        update_model: VendorUpdateModel | None = None, 
        request_operators: RequestOperators | None = None,
        allow_failures: bool = False
    ) -> VendorModel:
    
    original_object: VendorModel = get_vendor_by_id(context, id, request_operators)

    result: Response = qa_patch(f"{context.api_url}/vendors/{id}", update_model, request_operators)

    if(allow_failures == False):
        assert result.status_code == 200
 
        result_dict = result.json()

        assert_object_was_updated(original_object.__dict__, update_model.__dict__, result_dict, ["updated_at"])
 
        assert result_dict['updated_at'] is not None
    
    return_object = VendorModel(**result.json())
    
    return return_object