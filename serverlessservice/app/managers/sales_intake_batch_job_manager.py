import json
from uuid import UUID
from data_accessors.sales_intake_batch_job_accessor import SalesIntakeBatchJobDataAccessor
from data_accessors.pos_integration_accessor import PosIntegrationDataAccessor
from data_accessors.retailer_location_accessor import RetailerLocationDataAccessor
from integrations.posabit_integration import PosabitIntegration
from models.sales_intake_batch_job_model import (
    SalesIntakeBatchJobCreateModel,
    SalesIntakeBatchJobModel,
    SalesIntakeBatchJobSearchModel,
    SalesIntakeBatchJobStatuses,
    SalesIntakeBatchJobUpdateModel,
)
from models.common_model import ItemList
from models.pos_integration_model import PosIntegrationSearchModel, PosPlatforms
from util.database import PagingModel

accessor: SalesIntakeBatchJobDataAccessor = SalesIntakeBatchJobDataAccessor()
retailer_location_accessor: RetailerLocationDataAccessor = RetailerLocationDataAccessor()
pos_integartion_accessor: PosIntegrationDataAccessor = PosIntegrationDataAccessor()
posabit_integration: PosabitIntegration = PosabitIntegration()


class SalesIntakeBatchJobManager:

    def create(
            self, 
            inboundModel: SalesIntakeBatchJobCreateModel
    ) -> SalesIntakeBatchJobModel | None:
 
        result = accessor.insert(inboundModel)

        return result

    def get_by_id(self, id: UUID):

        result = accessor.select_by_id(id)

        return result

    def search(
        self,
        model: SalesIntakeBatchJobSearchModel,
        paging_model: PagingModel | None = None,
    ) -> ItemList[SalesIntakeBatchJobModel]:

        result = accessor.select(model, paging_model)

        return result

    def update(
        self,
        id: UUID,
        model: SalesIntakeBatchJobUpdateModel,
        explicit_null_set: list[str] | None = None,
    ):

        explicitNullSet = explicit_null_set or []

        result = accessor.update(id, model,explicitNullSet)

        return result

    def delete(self, id: UUID):

        result: None | SalesIntakeBatchJobModel = accessor.delete(id)

        return result
    
    def run(self, id: UUID):
        job_to_run: SalesIntakeBatchJobModel = accessor.select_by_id(id)
        
        if(job_to_run == None):
            return None
        # set job to processing
        
        job_to_run.status = SalesIntakeBatchJobStatuses.Processing
        
        accessor.update(id, job_to_run)
        
        pos_integration_search_model: PosIntegrationSearchModel = PosIntegrationSearchModel(
            retailer_location_ids=[job_to_run.retailer_location_id]
        )
        
        pos_integrations = pos_integartion_accessor.select(pos_integration_search_model)
        
        print("Found the following pos integrations:" + json.dumps([{ "id" : x.id, "name" : x.name} for x in pos_integrations.items], indent=4))
        
        for pos_integration in pos_integrations.items:
            try:
            
                if(pos_integration.pos_platform == PosPlatforms.Posabit):
                    posabit_integration.process_sales_snapshot(job_to_run, pos_integration)
                    
                    job_to_run.status = SalesIntakeBatchJobStatuses.Complete
                    
                    accessor.update(id, job_to_run)
                else:
                    raise Exception(f"Pos Integration Platform {pos_integration.pos_platform} not supported")

            except Exception as e:
                
                info = {"id" : pos_integration.id, "name" : pos_integration.name}
                
                print(f"Pos Integration {json.dumps(info)} failed with error: {e}")
                
                job_to_run.status = SalesIntakeBatchJobStatuses.Failed
                
                accessor.update(id, job_to_run)
                
                return
