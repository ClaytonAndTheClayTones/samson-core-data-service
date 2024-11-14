from fastapi import Depends, FastAPI, HTTPException, Response
from pydantic import UUID4
import uvicorn

from models.sales_intake_batch_job_model import (
    SalesIntakeBatchJobInboundCreateModel,
    SalesIntakeBatchJobInboundSearchModel,
    SalesIntakeBatchJobInboundUpdateModel,
    SalesIntakeBatchJobOutboundModel,
)
from controllers.sales_intake_batch_job_controller import SalesIntakeBatchJobController
from models.common_model import (
    OutboundItemListResponse, )
from util.environment import Environment

controller: SalesIntakeBatchJobController = SalesIntakeBatchJobController()


def set_sales_intake_batch_job_routes(app: FastAPI):

    @app.post(
        '/sales_intake_batch_jobs',
        response_model=SalesIntakeBatchJobOutboundModel,
        status_code=201,
    )
    def post_retailerlocation(
        inbound_create_model: SalesIntakeBatchJobInboundCreateModel, ):
        result = controller.create(inbound_create_model)

        return result

    @app.get(
        '/sales_intake_batch_jobs',
        response_model=OutboundItemListResponse[SalesIntakeBatchJobOutboundModel],
    )
    def get_sales_intake_batch_jobs(
        inbound_search_model: SalesIntakeBatchJobInboundSearchModel = Depends(),
    ) -> OutboundItemListResponse[SalesIntakeBatchJobOutboundModel]:

        result = controller.search(inbound_search_model)

        return result

    @app.get('/sales_intake_batch_jobs/{id}',
             response_model=SalesIntakeBatchJobOutboundModel)
    def get_sales_intake_batch_job_by_id(id: UUID4):

        result = controller.get_by_id(id)

        return result
    
    @app.post('/sales_intake_batch_jobss/{id}/run',
             response_model=SalesIntakeBatchJobOutboundModel)
    def run_sales_intake_batch_job (id: UUID4):

        result = controller.run(id)

        return result

    @app.patch('/sales_intake_batch_jobs/{id}',
               response_model=SalesIntakeBatchJobOutboundModel)
    def patch_sales_intake_batch_job(
            id: UUID4, inbound_update_model: SalesIntakeBatchJobInboundUpdateModel):
        result = controller.update(id, inbound_update_model)

        return result

    @app.delete('/sales_intake_batch_jobs/{id}',
                response_model=SalesIntakeBatchJobOutboundModel)
    def delete_sales_intake_batch_job(id: UUID4):

        result = controller.delete(id)

        return result
