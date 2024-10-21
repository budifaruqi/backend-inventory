from enum import Enum


class RoleLocation(str, Enum):
    system = "system", "Sistem"
    company = "company", "Perusahaan"
    external= "external", "External"

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