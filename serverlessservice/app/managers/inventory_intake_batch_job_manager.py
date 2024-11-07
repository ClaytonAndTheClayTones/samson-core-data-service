import json
from uuid import UUID
from data_accessors.inventory_intake_batch_job_accessor import InventoryIntakeBatchJobDataAccessor
from data_accessors.pos_integration_accessor import PosIntegrationDataAccessor
from data_accessors.retailer_location_accessor import RetailerLocationDataAccessor
from integrations.posabit_integration import PosabitIntegration
from models.inventory_intake_batch_job_model import (
    InventoryIntakeBatchJobCreateModel,
    InventoryIntakeBatchJobModel,
    InventoryIntakeBatchJobSearchModel,
    InventoryIntakeBatchJobStatuses,
    InventoryIntakeBatchJobUpdateModel,
)
from models.common_model import ItemList
from models.pos_integration_model import PosIntegrationSearchModel, PosPlatforms
from util.database import PagingModel

accessor: InventoryIntakeBatchJobDataAccessor = InventoryIntakeBatchJobDataAccessor()
retailer_location_accessor: RetailerLocationDataAccessor = RetailerLocationDataAccessor()
pos_integartion_accessor: PosIntegrationDataAccessor = PosIntegrationDataAccessor()
posabit_integration: PosabitIntegration = PosabitIntegration()


class InventoryIntakeBatchJobManager:

    def create(
            self, 
            inboundModel: InventoryIntakeBatchJobCreateModel
    ) -> InventoryIntakeBatchJobModel | None:
 
        result = accessor.insert(inboundModel)

        return result

    def get_by_id(self, id: UUID):

        result = accessor.select_by_id(id)

        return result

    def search(
        self,
        model: InventoryIntakeBatchJobSearchModel,
        paging_model: PagingModel | None = None,
    ) -> ItemList[InventoryIntakeBatchJobModel]:

        result = accessor.select(model, paging_model)

        return result

    def update(
        self,
        id: UUID,
        model: InventoryIntakeBatchJobUpdateModel,
        explicit_null_set: list[str] | None = None,
    ):

        explicitNullSet = explicit_null_set or []

        result = accessor.update(id, model,explicitNullSet)

        return result

    def delete(self, id: UUID):

        result: None | InventoryIntakeBatchJobModel = accessor.delete(id)

        return result
    
    def run(self, id: UUID):
        job_to_run: InventoryIntakeBatchJobModel = accessor.select_by_id(id)
        
        if(job_to_run == None):
            return None
        # set job to processing
        
        job_to_run.status = InventoryIntakeBatchJobStatuses.Processing
        
        accessor.update(id, job_to_run)
        
        pos_integration_search_model: PosIntegrationSearchModel = PosIntegrationSearchModel(
            retailer_location_ids=[job_to_run.retailer_location_id]
        )
        
        pos_integrations = pos_integartion_accessor.select(pos_integration_search_model)
        
        print("Found the following pos integrations:" + json.dumps([{ "id" : x.id, "name" : x.name} for x in pos_integrations.items], indent=4))
        
        for pos_integration in pos_integrations.items:
            try:
            
                if(pos_integration.pos_platform == PosPlatforms.Posabit):
                    posabit_integration.process_inventory_snapshot(job_to_run, pos_integration)
                    
                    job_to_run.status = InventoryIntakeBatchJobStatuses.Complete
                    
                    accessor.update(id, job_to_run)
                else:
                    raise Exception(f"Pos Integration Platform {pos_integration.pos_platform} not supported")

            except Exception as e:
                
                info = {"id" : pos_integration.id, "name" : pos_integration.name}
                
                print(f"Pos Integration {json.dumps(info)} failed with error: {e}")
                
                job_to_run.status = InventoryIntakeBatchJobStatuses.Failed
                
                accessor.update(id, job_to_run)
                
                return
