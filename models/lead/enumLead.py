from enum import Enum


class LeadStatus(str, Enum):
    NEW = "NEW", "New"
    PENDING      = "PENDING", "Pending"
    WON = "WON", "Won"
    LOST      = "LOST", "Lost"
    PKS = "PKS", "PKS"
    ORDER      = "ORDER", "Order"
    PAID = "PAID", "Paid"
    IMPLEMENTATION      = "IMPLEMENTATION", "Implementation"
    LIVE = "LIVE", "Live"
    INACTIVE      = "INACTIVE", "Inactive"
    REACTIVATION = "REACTIVATION", "Reactivation"


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
   
class LeadType(str, Enum):
    POTENTIAL_LEAD = "POTENTIAL_LEAD", "Potential Lead"
    LEAD      = "LEAD", "Lead"
    CLIENT = "CLIENT", "Client"

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