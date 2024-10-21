from classes.classMongoDb import TMongoCollection
from mongodb.mongoClient import MGDB
from mongodb.mongoCollectionName import CollectionNames

TbGlobalConfig: TMongoCollection = MGDB[CollectionNames.TbGlobalConfig.value]
TbCompanyCategory: TMongoCollection = MGDB[CollectionNames.TbCompanyCategory.value]
TbCompany: TMongoCollection = MGDB[CollectionNames.TbCompany.value]
TbAccount: TMongoCollection = MGDB[CollectionNames.TbAccount.value]
TbAccountExternal: TMongoCollection = MGDB[CollectionNames.TbAccountExternal.value]
TbMasterData: TMongoCollection = MGDB[CollectionNames.TbMasterData.value]
TbMasterDataFollower: TMongoCollection = MGDB[CollectionNames.TbMasterDataFollower.value]
TbPartner: TMongoCollection = MGDB[CollectionNames.TbPartner.value]
TbLead: TMongoCollection = MGDB[CollectionNames.TbLead.value]
TbLeadTag: TMongoCollection = MGDB[CollectionNames.TbLeadTag.value]
TbUoMCategory: TMongoCollection = MGDB[CollectionNames.TbUoMCategory.value]
TbUoM: TMongoCollection = MGDB[CollectionNames.TbUoM.value]


