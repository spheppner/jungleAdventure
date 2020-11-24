import random

class Game:
    deck1 = []
    deck2 = []
    hp1 = 100
    hp2 = 100
    zoo1 = []
    zoo2 = []


class Card:
    def __init__(self):
        self.effect = ("nothing", 0)
        r = random.randint(1,80)
        self.direct_damage = {0:  ("fizzle", 0),
                              20: ("spark", 10),
                              40: ("fireball", 20),
                              60: ("iceball", 35)}
        for v in self.direct_damage.keys():
            if r > v:
                self.effect = self.direct_damage[v]

    def __repr__(self):
        return str(self.effect)

if __name__ == "__main__":

    for _ in range(7):
        Game.deck1.append(Card())
        Game.deck2.append(Card())
    while Game.hp1 > 0 and Game.hp2 > 0:

        print("deck1:", [str(i) +":"+  str(card) for i, card in enumerate(Game.deck1)])
        print("deck2:", [str(i) +":"+  str(card) for i, card in enumerate(Game.deck2)])

        print("-----------------------------")
        print("player1, choose your card:")
        c1 = int(input(">>>"))
        card1 = Game.deck1.pop(c1)
        print("-----------------------------")
        print("player2, choose your card:")
        c2 = int(input(">>>"))
        card2 = Game.deck1.pop(c2)

        print("------- execute ------")
        Game.hp1 -= card2.effect[1]
        Game.hp2 -= card1.effect[1]


        print("------ hp left: ----")
        print("player 1 ", Game.hp1)
        print("player 2 ", Game.hp2)
    print("game over")








