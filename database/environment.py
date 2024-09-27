import json
from pprint import pprint
from lib.configuration import Configuration, set_global_configuration
import builtins

from lib.connection import PGConnection

class Environment:

    pg_connection = PGConnection()
    configuration = Configuration()

    def setup_environment(self, configuration_path: str):

        self.configuration.populate_configuration(configuration_path)

        pprint(f"Configuration Loaded: {vars(self.configuration)}")

        # Database Connection

        self.pg_connection.create_connection(
            host = self.configuration.POSTGRES_HOST,
            port = self.configuration.POSTGRES_PORT,
            database = self.configuration.POSTGRES_DB,
            username = self.configuration.POSTGRES_USER,
            password = self.configuration.POSTGRES_PASSWORD
        )

        print(f"Database Connection Created: { self.pg_connection.connection.get_dsn_parameters()['port'] }")
