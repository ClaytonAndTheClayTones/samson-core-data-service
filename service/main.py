import os
from fastapi import Depends, FastAPI, HTTPException, Response
import uvicorn

from models.retailer_model import RetailerInboundCreateModel, RetailerInboundSearchModel, RetailerInboundUpdateModel, RetailerOutboundModel
from controllers.retailer_controller import RetailerController
from models.common_model import CommonOutboundResponseModel, OutboundItemListResponse
from routes.retailer_routes import set_routes as set_retailer_routes 
from routes.retailer_location_routes import set_routes as set_retailer_location_routes 
from routes.pos_integration_routes import set_routes as set_pos_integration_routes 
from util.environment import Environment

enviroment: Environment = Environment()

env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')

enviroment.setup_environment(env_path)

app = FastAPI()

# set routes 
set_retailer_routes(app)
set_retailer_location_routes(app)
set_pos_integration_routes(app) 

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
