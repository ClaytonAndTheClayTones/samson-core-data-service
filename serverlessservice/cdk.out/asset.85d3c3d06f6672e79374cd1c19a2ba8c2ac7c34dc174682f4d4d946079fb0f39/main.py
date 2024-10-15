# api-stack/src/api.py

import os
from mangum import Mangum
from fastapi import FastAPI
import uvicorn

from routes.utility_routes import set_routes as set_utility_routes
from util.environment import Environment
 

enviroment: Environment = Environment() 
 
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../.env')

enviroment.setup_environment(env_path)

app = FastAPI(
    title="Example Test API",
    description="Describe API documentation to be served; types come from "
    "pydantic, routes from the decorators, and docs from the fastapi internal",
    version="0.0.1",
)
 
set_utility_routes(app)


if __name__ == '__main__' and enviroment.configuration.STAGE == 'local':
    uvicorn.run(app, host='0.0.0.0', port=8001)
    
else:
    handler = Mangum(app, lifespan="off")