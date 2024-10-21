class StringDescription(str):
    description: str

    @classmethod
    def CreateNew(cls, value: str, description: str):
        inst = super().__new__(cls, value.strip().lower())
        inst.description = description
        return inst