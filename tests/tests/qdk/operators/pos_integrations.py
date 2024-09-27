import datetime

from requests import Response 
from tests.qdk.qa_requests import qa_get, qa_patch, qa_post
from tests.qdk.types import PagedResponseItemList, PagingResponseModel, PagingRequestModel, RequestOperators, TestContext
from tests.qdk.utils import assert_object_was_updated, assert_objects_are_equal, copy_object_when_appropriate, generate_random_string
 
class PosIntegrationCreateModel():  

    def __init__(self,
                name: str | None = None,
                description: str | None = None,
                pos_platform: str | None = None) -> None:
        
        self.name = name
        self.description = description
        self.pos_platform = pos_platform
         
        
class PosIntegrationUpdateModel():  

    def __init__(self,
            name: str | None = None,
            description: str | None = None,
            pos_platform: str | None = None) -> None:
        
        self.name = name
        self.description = description
        self.pos_platform = pos_platform

class PosIntegrationModel():  

    def __init__(self, 
                id: str, 
                name: str,
                pos_platform: str,
                created_at: datetime.datetime,
                description: str | None = None,  
                updated_at: datetime.datetime | None = None) -> None:
        
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
        self.name = name
        self.pos_platform = pos_platform
        self.description = description 
        
class PosIntegrationSearchModel(PagingRequestModel):  

    def __init__(self, 
                ids: str | None = None,  
                name: str | None = None,
                name_like: str | None = None,
                pos_platform: str | None = None, 
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
        self.name = name
        self.name_like = name_like
        self.pos_platform = pos_platform 
 
def mint_default_pos_integration(
    context: TestContext, 
    overrides: PosIntegrationCreateModel | None = None, 
    request_operators: RequestOperators | None = None
) -> PosIntegrationCreateModel: 
    random_string = generate_random_string()

    overrides = overrides or PosIntegrationCreateModel()
    
    default_pos_integration: PosIntegrationCreateModel = PosIntegrationCreateModel(
        name = random_string + '_name',
        description = 'describe it!!!!!', 
        pos_platform = 'Unknown'
    )

    copy_object_when_appropriate(default_pos_integration, overrides)
     
    return default_pos_integration

def create_pos_integration(
        context: TestContext,
        overrides: PosIntegrationCreateModel | None = None, 
        request_operators: RequestOperators | None = None,
        allow_failures: bool = False
        ) -> PosIntegrationModel:
    
    post_object: PosIntegrationCreateModel = mint_default_pos_integration(context = context, overrides = overrides, request_operators = request_operators)

    result: Response = qa_post(context.api_url + "/pos_integrations", post_object, request_operators)

    if(allow_failures == False):
        assert result.status_code == 201
 
        result_dict = result.json()

        assert_objects_are_equal(result_dict, post_object.__dict__, ["id", "created_at", "updated_at"])

        assert result_dict['id'] is not None
        assert result_dict['created_at'] is not None
        assert result_dict['updated_at'] is None
    
    return_object = PosIntegrationModel(**result.json())
    
    return return_object 
 
def get_pos_integration_by_id(
        context: TestContext, 
        id: str,
        request_operators: RequestOperators | None = None,
        allow_failures: bool = False
        ) -> PosIntegrationModel:

    url: str = f"{context.api_url}/pos_integrations/{id}"
    
    result: Response = qa_get(url)
     
    return_object = PosIntegrationModel(**result.json())
    
    return return_object 

def get_pos_integrations(
        context: TestContext, 
        search_model: PosIntegrationSearchModel | None,
        request_operators: RequestOperators | None = None 
    ) -> PagedResponseItemList[PosIntegrationModel]: 

    url: str = f"{context.api_url}/pos_integrations"
    
    result: Response = qa_get(
        url = url, 
        query_params = search_model if search_model is not None else {},
        request_operators = request_operators
    )
    
    result_dict = result.json()

    return_paging_object = PagingResponseModel(**result_dict['paging'])
     
    return_items: list[PosIntegrationModel] = [PosIntegrationModel(**obj) for obj in result_dict['items']]

    return_object = PagedResponseItemList[PosIntegrationModel](
        items = return_items, paging = return_paging_object
    )
    
    return return_object 

def update_pos_integration(
        context: TestContext,
        id: str,
        update_model: PosIntegrationUpdateModel | None = None, 
        request_operators: RequestOperators | None = None,
        allow_failures: bool = False
    ) -> PosIntegrationModel:
    
    original_object: PosIntegrationModel = get_pos_integration_by_id(context, id, request_operators)

    result: Response = qa_patch(f"{context.api_url}/pos_integrations/{id}", update_model, request_operators)

    if(allow_failures == False):
        assert result.status_code == 200
 
        result_dict = result.json()

        assert_object_was_updated(original_object.__dict__, update_model.__dict__, result_dict, ["updated_at"])
 
        assert result_dict['updated_at'] is not None
    
    return_object = PosIntegrationModel(**result.json())
    
    return return_object