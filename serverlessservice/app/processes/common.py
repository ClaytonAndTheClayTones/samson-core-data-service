
class ProcessException(Exception):
    def __init__(self, process_name, process_id, step, message: str):
        concatenated_message = f"Exception occured in process {process_name} with id {process_id} in Step {step}: {message}"
        super().__init__(concatenated_message)