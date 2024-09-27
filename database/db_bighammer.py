import os
import json
from pprint import pprint
from lib.bighammer import BigHammer
from lib.configuration import Configuration, set_global_configuration
import builtins

from lib.connection import PGConnection
from environment import Environment

environment: Environment = Environment()

env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')

environment.setup_environment(env_path)

big_hammer = BigHammer()

big_hammer.hammer(environment)
