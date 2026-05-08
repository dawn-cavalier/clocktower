import random as r

from enums.roles import Role
from enums.infoType import InfoType
from classes.player import Player
from classes.info import Info
from helpers.scriptInfo import getTypeCounts
from helpers.isCategory import *


def main() -> None:
    # TODO: Assuming constant player count
    playerCount = 7
    # TODO: Assuming limited script
    script = [
        Role.WASHERWOMAN,
        Role.CHEF,
        Role.LIBRARIAN,
        Role.INVESTIGATOR,
        Role.EMPATH,
        Role.VIRGIN,
        Role.RAVENKEEPER,
        Role.SLAYER,
        Role.SCARLET_WOMAN,
        Role.SPY,
        Role.IMP,
    ]

    startGame(playerCount=playerCount, script=script)


def startGame(playerCount: int, script: list[Role]):
    ## Player Construction
    players: list[Player] = []
    for seat in range(playerCount):
        newPlayer = Player()
        newPlayer.seat = seat
        newPlayer.trust = [0.5 for _ in range(playerCount)]
        newPlayer.isAlive = True
        players.append(newPlayer)

    ## Role Assignment
    # TODO: Handle role count modification
    countTownsfolk, countOutsider, countMinion, countDemon = getTypeCounts(
        playerCount=playerCount
    )
    roles: list[Role] = []
    roles += r.sample([role for role in script if isTownsfolk(role)], countTownsfolk)
    roles += r.sample([role for role in script if isOutsider(role)], countOutsider)
    roles += r.sample([role for role in script if isMinion(role)], countMinion)
    roles += r.sample([role for role in script if isDemon(role)], countDemon)
    r.shuffle(roles)

    for player in players:
        # TODO: Add Random Role Assignment
        player.role = roles[player.seat]
        if isMinion(player.role) or isDemon(player.role):
            player.isEvil = True
        else:
            player.isEvil = False

    ## Start of game info
    townsfolk = [player for player in players if isTownsfolk(player.role)]
    outsiders = [player for player in players if isOutsider(player.role)]
    minions = [player for player in players if isMinion(player.role)]
    demons = [player for player in players if isDemon(player.role)]
    bluffs = r.sample(
        [role for role in script if role not in [player.role for player in players]], 3
    )

    # Learn self role
    for player in players:
        player.learn(Info(InfoType.IS_ROLE, [], [player.seat], [player.role]))

    # Minions learn their info
    for minion in minions:
        # Minions learn their demon
        learnedInfo = Info(
            InfoType.IS_ROLE,
            [],
            [demon.seat for demon in demons],
            [role for role in script if isDemon(role)],
        )
        minion.learn(learnedInfo)

        # Minions learn other minions
        # TODO: Test this code
        otherMinionIds = [
            player.seat for player in minions if player.seat != minion.seat
        ]
        if len(otherMinionIds) > 0:
            learnedInfo = Info(
                InfoType.IS_ROLE,
                [],
                otherMinionIds,
                [role for role in script if isMinion(role)],
            )
            minion.learn(learnedInfo)

    # Demons learn their info
    for demon in demons:
        # Demon learns Minions
        learnedInfo = Info(
            InfoType.IS_ROLE,
            [],
            [minion.seat for minion in minions],
            [role for role in script if isMinion(role)],
        )
        demon.learn(learnedInfo)

        # Demon learns Bluffs
        learnedInfo = Info(
            InfoType.IS_NOT_ROLE, [], [player.seat for player in players], bluffs
        )
        demon.learn(learnedInfo)

    # Poisoner act
    # poisoners = [minion for minion in minions if minion.role is Role.POISONER]
    # Spys learn their info
    spies = [minion for minion in minions if minion.role is Role.SPY]
    for spy in spies:
        for player in players:
            if player.seat == spy.seat:
                continue

            learnedInfo = Info(InfoType.IS_ROLE, [], [player.seat], [player.role])
            spy.learn(learnedInfo)

        learnedInfo = Info(
            InfoType.IS_NOT_ROLE, [], [player.seat for player in players], bluffs
        )
        spy.learn(learnedInfo)

    # Washerwoman info
    washerwomen = [folk for folk in townsfolk if folk.role is Role.WASHERWOMAN]
    for washerwoman in washerwomen:
        # TODO: Make this more intelligent
        # TODO: Handle Poisoning
        correctTarget = r.sample(
            [folk.seat for folk in townsfolk if folk.seat != washerwoman.seat], 1
        )
        incorrectTarget = r.sample(
            [
                player.seat
                for player in players
                if player.seat not in correctTarget or player.seat != washerwoman.seat
            ],
            1,
        )
        targets = correctTarget + incorrectTarget
        r.shuffle(targets)
        learnedInfo = Info(
            InfoType.ONE_IS_ROLE,
            [washerwoman.seat],
            targets,
            [player.role for player in players if player.seat in correctTarget],
        )
        washerwoman.learn(learnedInfo)

    # Librarian info
    librarians = [folk for folk in townsfolk if folk.role is Role.LIBRARIAN]
    for librarian in librarians:
        # TODO: Make this more intelligent
        # TODO: Handle Poisoning
        # TODO: Test this in game with outsiders
        learnedInfo = None
        if len(outsiders) > 0:
            correctTarget = r.sample([outsider.seat for outsider in outsiders], 1)
            incorrectTarget = r.sample(
                [player.seat for player in players if player.seat not in correctTarget],
                1,
            )
            targets = correctTarget + incorrectTarget
            r.shuffle(targets)

            learnedInfo = Info(
                InfoType.ONE_IS_ROLE,
                [librarian.seat],
                targets,
                [
                    player.role
                    for player in players
                    if player.seat in correctTarget and player.seat != librarian.seat
                ],
            )
        else:
            learnedInfo = Info(
                InfoType.IS_ROLE,
                [librarian.seat],
                [],
                [role for role in script if isOutsider(role)],
            )
        librarian.learn(learnedInfo)

    # Investigator info
    investigators = [folk for folk in townsfolk if folk.role is Role.INVESTIGATOR]
    for investigator in investigators:
        # TODO: Make this more intelligent
        # TODO: Handle Poisoning
        correctTarget = r.sample([minion.seat for minion in minions], 1)
        incorrectTarget = r.sample(
            [player.seat for player in players if player.seat not in correctTarget],
            1,
        )
        targets = correctTarget + incorrectTarget
        r.shuffle(targets)
        learnedInfo = Info(
            InfoType.ONE_IS_ROLE,
            [investigator.seat],
            targets,
            [
                player.role
                for player in players
                if player.seat in correctTarget and player.seat != investigator.seat
            ],
        )
        investigator.learn(learnedInfo)

    # Chef info
    chefs = [folk for folk in townsfolk if folk.role is Role.CHEF]
    for chef in chefs:
        pairs = 0
        for player in players:
            if not player.isEvil:
                continue

            nextSeat = player.seat + 1
            if nextSeat == playerCount:
                nextSeat = 0

            if [otherPlayer for otherPlayer in players if otherPlayer.seat == nextSeat][
                0
            ].isEvil:
                pairs += 1

        learnedInfo = Info(InfoType.NUMBER_CHEF, [chef.seat], [], pairs)
        chef.learn(learnedInfo)

    # Empath info
    empaths = [folk for folk in townsfolk if folk.role is Role.EMPATH]
    for empath in empaths:
        prevSeat = empath.seat - 1
        if prevSeat < 0:
            prevSeat = playerCount - 1
        while not [player for player in players if player.seat == prevSeat][0].isAlive:
            prevSeat = empath.seat - 1
            if prevSeat < 0:
                prevSeat = playerCount - 1

        nextSeat = empath.seat + 1
        if nextSeat == playerCount:
            nextSeat = 0
        while not [player for player in players if player.seat == nextSeat][0].isAlive:
            nextSeat = empath.seat + 1
            if nextSeat == playerCount:
                nextSeat = 0

        count = 0
        if [player for player in players if player.seat == prevSeat][0].isEvil:
            count += 1

        if [player for player in players if player.seat == nextSeat][0].isEvil:
            count += 1

        learnedInfo = Info(InfoType.NUMBER_EMPATH, [empath.seat], [], count)
        empath.learn(learnedInfo)
        
    # Fortune Teller acts
    # Butler acts

    for player in players:
        print(f"{player.seat} {player.role.name}:")
        for info in player.infoBank:
            print(f"\t{info}")


if __name__ == "__main__":
    main()
