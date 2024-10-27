from typing import Any
from models.pos_integration_model import (
    PosIntegrationCreateModel,
    PosIntegrationInboundCreateModel,
    PosIntegrationInboundSearchModel,
    PosIntegrationInboundUpdateModel,
    PosIntegrationModel,
    PosIntegrationOutboundModel,
    PosIntegrationSearchModel,
    PosIntegrationUpdateModel,
)
from util.common import CommonUtilities
from util.database import (
    ExactMatchSearchTerm,
    InListSearchTerm,
    LikeComparatorModes,
    LikeSearchTerm,
    SearchTerm,
)


class PosIntegrationDataAdapter:
    common_utilities: CommonUtilities = CommonUtilities()

    def convert_from_inbound_create_model_to_create_model(
        self, 
        inbound_create_model: PosIntegrationInboundCreateModel
    ) -> PosIntegrationCreateModel:
        
        model = PosIntegrationCreateModel(
            retailer_location_id=inbound_create_model.retailer_location_id,
            name=inbound_create_model.name,
            url=inbound_create_model.url,
            key=inbound_create_model.key,
            description=inbound_create_model.description,
            pos_platform=inbound_create_model.pos_platform,
        )

        return model

    def convert_from_inbound_update_model_to_create_model(
        self, 
        inbound_update_model: PosIntegrationInboundUpdateModel
    ) -> PosIntegrationUpdateModel:
       
        model = PosIntegrationUpdateModel(
            name=inbound_update_model.name,
            url=inbound_update_model.url,
            key=inbound_update_model.key,
            description=inbound_update_model.description,
            pos_platform=inbound_update_model.pos_platform,
        )

        return model

    def convert_from_inbound_search_model_to_search_model(
        self, 
        inbound_search_model: PosIntegrationInboundSearchModel
    ) -> PosIntegrationSearchModel:
        
        model = PosIntegrationSearchModel(
            ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(inbound_search_model.ids)
                if inbound_search_model.ids is not None 
                else 
                    None
            ),
            retailer_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(inbound_search_model.retailer_ids)
                if inbound_search_model.retailer_ids is not None 
                else 
                    None
            ),
            retailer_location_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(inbound_search_model.retailer_location_ids)
                if inbound_search_model.retailer_location_ids is not None 
                else 
                    None
            ),
            name=inbound_search_model.name,
            name_like=inbound_search_model.name_like,
            pos_platform=inbound_search_model.pos_platform,
        )

        return model

    def convert_from_search_model_to_search_terms(
            self, 
            model: PosIntegrationSearchModel
        ) -> list[SearchTerm]:
        
        search_terms: list[SearchTerm] = []

        if model.ids is not None:
            search_terms.append(InListSearchTerm('id', model.ids))
                    
        if model.retailer_ids is not None:
            search_terms.append(InListSearchTerm('retailer_id', model.retailer_ids))
                    
        if model.retailer_location_ids is not None:
            search_terms.append(InListSearchTerm('retailer_location_id', model.retailer_location_ids))
            
        if model.name is not None:
            search_terms.append(ExactMatchSearchTerm('name', model.name, True))
            
        if model.name_like is not None:
            search_terms.append(LikeSearchTerm('name', model.name_like, LikeComparatorModes.Like, True))
            
        if model.pos_platform is not None:
            search_terms.append(ExactMatchSearchTerm('pos_platform', model.pos_platform.value, True))

        return search_terms

    def convert_from_create_model_to_database_model(
            self, 
            model: PosIntegrationCreateModel
        ) -> dict[str, Any]:
       
        database_model: dict[str, Any] = {
            'retailer_id': model.retailer_id,
            'retailer_location_id': model.retailer_location_id,
            'name': model.name,
            'url': model.url,
            'key': model.key,
            'description': model.description,
            'pos_platform': model.pos_platform.value,
        }

        return database_model

    def convert_from_update_model_to_database_model(
            self, model: PosIntegrationUpdateModel) -> dict[str, Any]:
        database_model: dict[str, Any] = {
            'name': model.name,
            'url': model.url,
            'key': model.key,
            'description': model.description,
            'pos_platform': model.pos_platform.value,
            
        }

        return database_model

    def convert_from_database_model_to_model(
            self, database_model: dict[str, Any]) -> PosIntegrationModel:
        model = PosIntegrationModel(
            id=database_model['id'],
            retailer_id=database_model['retailer_id'],
            retailer_location_id=database_model['retailer_location_id'],
            name=database_model['name'],
            url=database_model['url'],
            key=database_model['key'],
            description=database_model['description'],
            pos_platform=database_model['pos_platform'],
            created_at=database_model['created_at'],
            updated_at=database_model['updated_at'],
        )

        return model

    def convert_from_model_to_outbound_model(
            self, 
            model: PosIntegrationModel
        ) -> PosIntegrationOutboundModel:
        
        outbound_model = PosIntegrationOutboundModel(
            id=model.id,
            retailer_id=model.retailer_id,
            retailer_location_id=model.retailer_location_id,
            name=model.name,
            url=model.url,
            key=model.key,
            description=model.description,
            pos_platform=model.pos_platform,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

        return outbound_model
