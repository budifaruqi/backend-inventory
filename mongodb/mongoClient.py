import asyncio
from typing import Any
from urllib.parse import quote_plus

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import WriteConcern

from classes.classMongoDb import TMongoClientSession, TMongoDatabase, TMongoClient
from config.config import settings


def CreateConnectionString() -> str:
    if not settings.project.use_localdb:
        database_name = settings.mongodb.database_name
        username = settings.mongodb.username
        password = settings.mongodb.password
        host = settings.mongodb.host
        port = settings.mongodb.port
        authMechanism = settings.mongodb.authMechanism
        directConnection = settings.mongodb.directConnection
        replica_set_name = settings.mongodb.replica_set_name
    else:
        database_name = settings.mongodb.localdb_database_name
        username = settings.mongodb.localdb_username
        password = settings.mongodb.localdb_password
        host = settings.mongodb.localdb_host
        port = settings.mongodb.localdb_port
        authMechanism = settings.mongodb.localdb_authMechanism
        directConnection = settings.mongodb.localdb_directConnection
        replica_set_name = settings.mongodb.localdb_replica_set_name

    connectionString = "mongodb://"
    if username is not None:
        connectionString += quote_plus(username)
        if password is not None:
            connectionString += ":" + quote_plus(password)
        connectionString += "@"
    connectionString += host
    if port is not None:
        connectionString += ":" + str(port)
    connectionString += "/?authSource=" + database_name
    if directConnection is not None:
        directConnectionStr = "true" if directConnection else "false"
        connectionString += "&directConnection=" + directConnectionStr
    if authMechanism is not None:
        connectionString += "&authMechanism=" + authMechanism.value
    if replica_set_name is not None:
        connectionString += "&replicaSet=" + replica_set_name
    
    return connectionString

def CreateMongoDbClient(loop: asyncio.AbstractEventLoop | None = None) -> TMongoClient:
    connectionString = CreateConnectionString()
    if loop:
        return AsyncIOMotorClient(connectionString, document_class=dict[str, Any], tz_aware=True, io_loop=loop)
    else:
        return AsyncIOMotorClient(connectionString, document_class=dict[str, Any], tz_aware=True)

MGDB_CLIENT: TMongoClient = CreateMongoDbClient(asyncio.get_running_loop())

MGDB: TMongoDatabase = MGDB_CLIENT.get_database(
    settings.mongodb.database_name if not settings.project.use_localdb else settings.mongodb.localdb_database_name,
    write_concern=WriteConcern(w="majority", wtimeout=1000)
)

async def MongoDbStartDefaultSession() -> TMongoClientSession:
    return await MGDB_CLIENT.start_session()

async def MongoDbStartSession(client: TMongoClient) -> TMongoClientSession:
    return await client.start_session()
