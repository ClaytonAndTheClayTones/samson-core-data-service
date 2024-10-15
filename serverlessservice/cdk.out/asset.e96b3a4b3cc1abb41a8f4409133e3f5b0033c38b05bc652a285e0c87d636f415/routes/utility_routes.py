from fastapi import FastAPI
 
def set_utility_routes(app: FastAPI):

    @app.get("/v1/hello")
    def list_items():
        """
        Return a hello hello 
        """
        return {
            'message': 'Hello hello!'
        }

