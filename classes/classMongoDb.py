from typing import TYPE_CHECKING, Any


from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorClientSession,
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
    AsyncIOMotorCursor,
    AsyncIOMotorCommandCursor,
    AsyncIOMotorLatentCommandCursor,
    AsyncIOMotorChangeStream,
    AsyncIOMotorClientEncryption
)

if TYPE_CHECKING:
    TMongoClient = AsyncIOMotorClient[dict[str, Any]]
    TMongoClientSession = AsyncIOMotorClientSession
    TMongoDatabase = AsyncIOMotorDatabase[dict[str, Any]]
    TMongoCollection = AsyncIOMotorCollection[dict[str, Any]]
    TMongoCursor = AsyncIOMotorCursor[dict[str, Any]]
    TMongoCommandCursor = AsyncIOMotorCommandCursor[dict[str, Any]]
    TMongoLatentCommandCursor = AsyncIOMotorLatentCommandCursor[dict[str, Any]]
    TMongoChangeStream = AsyncIOMotorChangeStream[dict[str, Any]]
    TMongoClientEncryption = AsyncIOMotorClientEncryption[dict[str, Any]]
else:
    TMongoClient = AsyncIOMotorClient
    TMongoClientSession = AsyncIOMotorClientSession
    TMongoDatabase = AsyncIOMotorDatabase
    TMongoCollection = AsyncIOMotorCollection
    TMongoCursor = AsyncIOMotorCursor
    TMongoCommandCursor = AsyncIOMotorCommandCursor
    TMongoLatentCommandCursor = AsyncIOMotorLatentCommandCursor
    TMongoChangeStream = AsyncIOMotorChangeStream
    TMongoClientEncryption = AsyncIOMotorClientEncryption
