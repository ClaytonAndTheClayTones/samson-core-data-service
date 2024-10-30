# api-stack/src/api.py

import os
from mangum import Mangum
from fastapi import FastAPI
import uvicorn

from routes.pos_integration_call_routes import set_pos_integration_call_routes
from routes.user_routes import set_user_routes
from routes.utility_routes import set_utility_routes
from routes.pos_integration_routes import set_pos_integration_routes
from routes.vendor_routes import set_vendor_routes
from routes.retailer_routes import set_retailer_routes
from routes.retailer_location_routes import set_retailer_location_routes

from util.environment import Environment
 
enviroment: Environment = Environment() 
 
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../.env')

enviroment.setup_environment(env_path)

app = FastAPI(
    title="DICS Core Api",
    description="Core Data Service for the DICS system.",
    version="0.0.1",
    docs_url='/docs',
    openapi_url='/openapi.json', 
)

if(enviroment.configuration.STAGE != 'local'):
    app.root_path = "/prod"
 
set_utility_routes(app)
set_retailer_routes(app)
set_retailer_location_routes(app)
set_user_routes(app)
set_vendor_routes(app)
set_pos_integration_routes(app)
set_pos_integration_call_routes(app)

if __name__ == '__main__' and enviroment.configuration.STAGE == 'local':
    uvicorn.run(app, host='0.0.0.0', port=8001)
    
else:
    handler = Mangum(app, lifespan="off")