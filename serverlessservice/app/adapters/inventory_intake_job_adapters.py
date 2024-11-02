from typing import Any
from models.inventory_intake_job_model import (
    InventoryIntakeJobCreateModel,
    InventoryIntakeJobInboundCreateModel,
    InventoryIntakeJobInboundSearchModel,
    InventoryIntakeJobInboundUpdateModel,
    InventoryIntakeJobModel,
    InventoryIntakeJobOutboundModel,
    InventoryIntakeJobSearchModel,
    InventoryIntakeJobUpdateModel,
)
from util.common import CommonUtilities
from util.database import (
    ExactMatchSearchTerm,
    InListSearchTerm,
    LikeComparatorModes,
    LikeSearchTerm,
    SearchTerm,
)


class InventoryIntakeJobDataAdapter:
    common_utilities: CommonUtilities = CommonUtilities()

    def convert_from_inbound_create_model_to_create_model(
        self, 
        inbound_create_model: InventoryIntakeJobInboundCreateModel
    ) -> InventoryIntakeJobCreateModel:
        
        model = InventoryIntakeJobCreateModel(
            retailer_id=inbound_create_model.retailer_id,
            retailer_location_id=inbound_create_model.retailer_location_id,
            snapshot_hour=inbound_create_model.snapshot_hour,
            status=inbound_create_model.status,
            status_details=inbound_create_model.status_details,
        )

        return model

    def convert_from_inbound_update_model_to_create_model(
        self, 
        inbound_update_model: InventoryIntakeJobInboundUpdateModel
    ) -> InventoryIntakeJobUpdateModel:
       
        model = InventoryIntakeJobUpdateModel(
            status=inbound_update_model.status,
            status_details=inbound_update_model.status_details,
        )

        return model

    def convert_from_inbound_search_model_to_search_model(
        self, 
        inbound_search_model: InventoryIntakeJobInboundSearchModel
    ) -> InventoryIntakeJobSearchModel:
        
        model = InventoryIntakeJobSearchModel(
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
            snapshot_hour=inbound_search_model.snapshot_hour,
            status=inbound_search_model.status,
        )

        return model

    def convert_from_search_model_to_search_terms(
            self, 
            model: InventoryIntakeJobSearchModel
        ) -> list[SearchTerm]:
        
        search_terms: list[SearchTerm] = []

        if model.ids is not None:
            search_terms.append(InListSearchTerm('id', self.common_utilities.convert_uuid_list_to_string_list(model.ids)))
                    
        if model.retailer_ids is not None:
            search_terms.append(InListSearchTerm('retailer_id', self.common_utilities.convert_uuid_list_to_string_list(model.retailer_ids)))
                    
        if model.retailer_location_ids is not None:
            search_terms.append(InListSearchTerm('retailer_location_id', self.common_utilities.convert_uuid_list_to_string_list(model.retailer_location_ids)))
            
        if model.name is not None:
            search_terms.append(ExactMatchSearchTerm('name', model.name, True))
            
        if model.name_like is not None:
            search_terms.append(LikeSearchTerm('name', model.name_like, LikeComparatorModes.Like, True))
            
        if model.pos_platform is not None:
            search_terms.append(ExactMatchSearchTerm('pos_platform', model.pos_platform.value, True))

        return search_terms

    def convert_from_create_model_to_database_model(
            self, 
            model: InventoryIntakeJobCreateModel
        ) -> dict[str, Any]:
       
        database_model: dict[str, Any] = {
            'retailer_id': str(model.retailer_id) if model.retailer_id is not None else None ,
            'retailer_location_id': str(model.retailer_location_id) if model.retailer_location_id is not None else None ,
            'snapshot_hour': model.snapshot_hour,
            'status': model.status.value if model.status is not None else None,
            'status_details': model.status_details,
        }

        return database_model

    def convert_from_update_model_to_database_model(
            self, 
            model: InventoryIntakeJobUpdateModel
        ) -> dict[str, Any]:
        
        database_model: dict[str, Any] = {
            'status': model.status.value if model.status is not None else None,
            'status_details': model.status_details,
            
        }

        return database_model

    def convert_from_database_model_to_model(
            self, 
            database_model: dict[str, Any]
        ) -> InventoryIntakeJobModel:
        
        model = InventoryIntakeJobModel(
            id=database_model['id'],
            retailer_id=database_model['retailer_id'],
            retailer_location_id=database_model['retailer_location_id'],
            snapshot_hour=database_model['snapshot_hour'],
            status=database_model['status'],
            status_details=database_model['status_details'],
            created_at=database_model['created_at'],
            updated_at=database_model['updated_at'],
        )

        return model

    def convert_from_model_to_outbound_model(
            self, 
            model: InventoryIntakeJobModel
        ) -> InventoryIntakeJobOutboundModel:
        
        outbound_model = InventoryIntakeJobOutboundModel(
            id=model.id,
            retailer_id=model.retailer_id,
            retailer_location_id=model.retailer_location_id,
            snapshot_hour=model.snapshot_hour,
            status=model.status,
            status_details=model.status_details,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

        return outbound_model
