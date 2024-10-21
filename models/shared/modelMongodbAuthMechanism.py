from enum import Enum


class MongodbAuthMechanism(str, Enum):
    Default = "DEFAULT"
    ScramSHA1 = "SCRAM-SHA-1"
    ScramSHA256 = "SCRAM-SHA-256"