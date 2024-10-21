from enum import Enum


class MsEnvironment(str, Enum):
    development = "development"
    staging = "staging"
    production = "production"