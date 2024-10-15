# api-stack/src/api.py

import os

from fastapi import FastAPI
import uvicorn

from mangum import Mangum
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
    title="Example Test API",
    description="Describe API documentation to be served; types come from "
    "pydantic, routes from the decorators, and docs from the fastapi internal",
    version="0.0.1",
)
 
set_utility_routes(app)
set_retailer_routes(app)
set_retailer_location_routes(app)
set_vendor_routes(app)
set_pos_integration_routes(app)

if __name__ == '__main__' and enviroment.configuration.STAGE == 'local':
    uvicorn.run(app, host='0.0.0.0', port=8001)
    
else:
    handler = Mangum(app, lifespan="off")