from enums.roles import Role
from enums.infoType import InfoType

class Info:
    infoType: InfoType
    source: list[int]
    targets: list[int]
    data: list[Role] | int

    def __init__(self, infoType: InfoType, source: list[int], targets: list[int], data: list[Role] | int) -> None:
        self.infoType = infoType
        self.source = source
        self.targets = targets
        self.data = data
    
    def __str__(self) -> str:
        return f"Info Type: {self.infoType.name}, Source: {self.source}, Targets: {self.targets}, Data: {self.data}"
