from enums.roles import Role
from classes.info import Info

class Player:
    role: Role
    trust: list[float]
    seat: int
    infoBank: list[Info]
    isEvil: bool
    isAlive: bool

    def __init__(self):
        self.role = Role.NONE
        self.trust = []
        self.seat = -1
        self.infoBank = []
        self.isEvil = False
        self.isAlive = False

    def learn(self, info: Info):
        self.infoBank.append(info)
