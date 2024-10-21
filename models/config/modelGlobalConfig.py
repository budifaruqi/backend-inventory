from datetime import datetime
from typing import Any
from models.shared.modelDataType import BaseModel


class MsBaseConfig(BaseModel):
    name: str
    updatedTime: datetime
    data: Any

# -----------------------------------------

class MsBaseConfigBytes(MsBaseConfig):
    data: bytes

# -----------------------------------------

class MsBaseConfigInteger(MsBaseConfig):
    data: int

# -----------------------------------------

class MsBaseConfigRsaKeyData(BaseModel):
    publicKey: bytes
    privateKey: bytes

class MsBaseConfigRsaKey(MsBaseConfig):
    data: MsBaseConfigRsaKeyData

# -----------------------------------------
