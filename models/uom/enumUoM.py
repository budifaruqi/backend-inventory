from enum import Enum


class UoMType(str, Enum):
    SMALLER = "SMALLER", "Smaller than the reference Unit of Measure"
    BIGGER      = "BIGGER", "Bigger than the reference Unit of Measure"
    REFERENCE = "REFERENCE", "Reference Unit of Measure for this category"


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