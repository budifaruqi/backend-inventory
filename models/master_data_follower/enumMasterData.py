from enum import Enum


class MasterDataFollowerStatus(str, Enum):
    REQUESTED = "REQUESTED", "Requested"
    APPROVE      = "APPROVE", "Approved"


    def __init__(self, value: str, description: str = "") -> None:
        super().__init__()
        self._value_ = value
        self.description = description

    def __new__(cls, value: str, description: str = ""):
        obj = str.__new__(cls, value)
        obj._value_ = value

        obj.description = description
        return obj
    
    @property
    def Description(self) -> str:
        return self.description
    
class FollowerDataConfig(str, Enum):
    SALES = "SALES", "Sales"
    PARTNER      = "PARTNER", "Partner"
    LEAD      = "LEAD", "Lead"
    LEAD_TAG      = "LEAD_TAG", "Lead Tags"


    def __init__(self, value: str, description: str = "") -> None:
        super().__init__()
        self._value_ = value
        self.description = description

    def __new__(cls, value: str, description: str = ""):
        obj = str.__new__(cls, value)
        obj._value_ = value

        obj.description = description
        return obj
    
    @property
    def Description(self) -> str:
        return self.description
    
class Operation(str, Enum):
    CREATE = "CREATE", "Create"
    READ      = "READ", "Read"
    UPDATE      = "UPDATE", "Update"
    DELETE      = "DELETE", "Delete"


    def __init__(self, value: str, description: str = "") -> None:
        super().__init__()
        self._value_ = value
        self.description = description

    def __new__(cls, value: str, description: str = ""):
        obj = str.__new__(cls, value)
        obj._value_ = value

        obj.description = description
        return obj
    
    @property
    def Description(self) -> str:
        return self.description