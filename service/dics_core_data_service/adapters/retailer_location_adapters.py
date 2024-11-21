from typing import Any
from models.retailer_location_model import (
    RetailerLocationCreateModel,
    RetailerLocationDatabaseModel,
    RetailerLocationInboundCreateModel,
    RetailerLocationInboundSearchModel,
    RetailerLocationInboundUpdateModel,
    RetailerLocationModel,
    RetailerLocationOutboundModel,
    RetailerLocationSearchModel,
    RetailerLocationUpdateModel,
)
from util.common import CommonUtilities
from util.database import (
    ExactMatchSearchTerm,
    InListSearchTerm,
    LikeComparatorModes,
    LikeSearchTerm,
    SearchTerm,
)


class RetailerLocationDataAdapter:
 
    def __init__(
        self,
        common_utilities: CommonUtilities = CommonUtilities()
    ) -> None:
        
        self.common_utilities = common_utilities
        
    def convert_from_inbound_create_model_to_create_model(
        self, inbound_create_model: RetailerLocationInboundCreateModel
    ) -> RetailerLocationCreateModel:
        model = RetailerLocationCreateModel(
            name=inbound_create_model.name,
            retailer_id=inbound_create_model.retailer_id,
            pos_integration_id=inbound_create_model.pos_integration_id,
            location_state=inbound_create_model.location_state,
            location_city=inbound_create_model.location_city,
            location_country=inbound_create_model.location_country,
            contact_email=inbound_create_model.contact_email,
            contact_phone=inbound_create_model.contact_phone,
        )

        return model

    def convert_from_inbound_update_model_to_create_model(
        self, inbound_update_model: RetailerLocationInboundUpdateModel
    ) -> RetailerLocationUpdateModel:
        model = RetailerLocationUpdateModel(
            name=inbound_update_model.name,
            pos_integration_id=inbound_update_model.pos_integration_id,
            location_state=inbound_update_model.location_state,
            location_city=inbound_update_model.location_city,
            location_country=inbound_update_model.location_country,
            contact_email=inbound_update_model.contact_email,
            contact_phone=inbound_update_model.contact_phone,
        )

        return model

    def convert_from_inbound_search_model_to_search_model(
        self, inbound_search_model: RetailerLocationInboundSearchModel
    ) -> RetailerLocationSearchModel:
        model = RetailerLocationSearchModel(
            ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(
                    inbound_search_model.ids)
                if inbound_search_model.ids is not None else None),
            retailer_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(
                    inbound_search_model.retailer_ids)
                if inbound_search_model.retailer_ids is not None else None),
            pos_integration_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(
                    inbound_search_model.pos_integration_ids)
                if inbound_search_model.pos_integration_ids is not None else
                None),
            name=inbound_search_model.name,
            name_like=inbound_search_model.name_like,
            location_state=inbound_search_model.location_state,
            location_city=inbound_search_model.location_city,
            location_country=inbound_search_model.location_country,
        )

        return model

    def convert_from_search_model_to_search_terms(
            self, model: RetailerLocationSearchModel) -> list[SearchTerm]:
        search_terms: list[SearchTerm] = []

        if model.ids is not None:
            search_terms.append(InListSearchTerm('id', model.ids))
        if model.retailer_ids is not None:
            search_terms.append(
                InListSearchTerm('retailer_id', model.retailer_ids))
        if model.pos_integration_ids is not None:
            search_terms.append(
                InListSearchTerm('pos_integration_id',
                                 model.pos_integration_ids))
        if model.name is not None:
            search_terms.append(ExactMatchSearchTerm('name', model.name, True))
        if model.name_like is not None:
            search_terms.append(
                LikeSearchTerm('name', model.name_like,
                               LikeComparatorModes.Like, True))
        if model.location_state is not None:
            search_terms.append(
                ExactMatchSearchTerm('location_state', model.location_state,
                                     True))
        if model.location_city is not None:
            search_terms.append(
                ExactMatchSearchTerm('location_city', model.location_city,
                                     True))
        if model.location_country is not None:
            search_terms.append(
                ExactMatchSearchTerm('location_country',
                                     model.location_country, True))

        return search_terms

    def convert_from_create_model_to_database_model(
            self, model: RetailerLocationCreateModel) -> dict[str, Any]:
        database_model: dict[str, Any] = {
            'name': model.name,
            'retailer_id': model.retailer_id,
            'pos_integration_id': model.pos_integration_id,
            'location_state': model.location_state,
            'location_city': model.location_city,
            'location_country': model.location_country,
            'contact_email': model.contact_email,
            'contact_phone': model.contact_phone,
        }

        return database_model

    def convert_from_update_model_to_database_model(
            self, model: RetailerLocationUpdateModel) -> dict[str, Any]:
        database_model: dict[str, Any] = {
            'name': model.name,
            'pos_integration_id': model.pos_integration_id,
            'location_state': model.location_state,
            'location_city': model.location_city,
            'location_country': model.location_country,
            'contact_email': model.contact_email,
            'contact_phone': model.contact_phone,
        }

        return database_model

    def convert_from_database_model_to_model(
            self, database_model: dict[str, Any]) -> RetailerLocationModel:
        model = RetailerLocationModel(
            id=database_model['id'],
            name=database_model['name'],
            retailer_id=database_model['retailer_id'],
            pos_integration_id=database_model['pos_integration_id'],
            location_state=database_model['location_state'],
            location_city=database_model['location_city'],
            location_country=database_model['location_country'],
            contact_email=database_model['contact_email'],
            contact_phone=database_model['contact_phone'],
            created_at=database_model['created_at'],
            updated_at=database_model['updated_at'],
        )

        return model

    def convert_from_model_to_outbound_model(
            self,
            model: RetailerLocationModel) -> RetailerLocationOutboundModel:
        outbound_model = RetailerLocationOutboundModel(
            id=model.id,
            retailer_id=model.retailer_id,
            pos_integration_id=model.pos_integration_id,
            name=model.name,
            location_state=model.location_state,
            location_city=model.location_city,
            location_country=model.location_country,
            contact_email=model.contact_email,
            contact_phone=model.contact_phone,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

        return outbound_model
