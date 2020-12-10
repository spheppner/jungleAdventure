# magic card game
# each player has a wizard with hitpoints
# the wizards battle against each other until only the sole survivor is victor
# each wizard gets some random cards from a stack, forming his card-deck
# (every wizard can only see his own card-deck)
# type of cards:
# direct-damage (like Flame Bolt), directly damages one enemy figure
# summoning: summons a monster that fights for the wizard
# buffs: improves friendly figures
# nerfs: nerfs enemy figures
# trading of cards:
# each wizard has the option to trade several cards against a unknown card of a higher level
# turns:
# planning phase:
# each player say the server (computer) witch card he wants to play
# execution phase:
# the computer calculates the result of all actions and displays the to the wizards
# Discord Text: https://www.writebots.com/discord-text-formatting/
# Bolded Text = **Example**
# Italized Text = *Example*
# Underlined Text = __Example__
# You can combine the types of texts


import random


class Game:
    monsternumber = 0
    time = 0


class Monster:

    def __init__(self):
        self.number = Game.monsternumber
        Game.monsternumber += 1
        self.hp = 100
        self.attack = "2d6"
        self.defense = "1d10"
        self.damage = "1d4"
        self.buffs = []
        # ----- resitances ------
        self.resist_fire = 0
        self.resist_cold = 0
        self.resist_poision = 0
        self.resist_electro = 0
        # ---- elemental damage ----
        self.damage_fire = 0
        self.damage_cold = 0
        self.damage_poision = 0
        self.damage_electro = 0
        # ---- other ---
        self.age = 0
        self.__post_init__()
        self.history = []
        self.revenge = []

    def __post_init__(self):
        pass

    def ai(self):
        pass

    @property
    def shortname(self):
        return f"{self.__class__.__name__} (#{self.number})"

    def __repr__(self):
        return f"{self.__class__.__name__} hp: {self.hp} att: {self.attack} def: {self.defense} dmg: {self.damage} special: {None}"


class Wizard(Monster):

    def __post_init__(self):
        self.hp = 150
        self.attack = "4d4"
        self.defense = "2d6"
        self.damage = "2d4"
        self.deck = []
        self.i = None
        self.army = [self]
        self.text = []

    def show_army(self):
        # print("-=-=- your army -=-=-")
        for soldier in self.army:
            print(f"..........{soldier}")

    def show_deck(self):
        print("-=-=- your card deck -=-=-")
        for index, card in enumerate(self.deck):
            print("index:", index, "card:", card)


class Minion(Monster):

    def __post_init__(self):
        self.hp = 50
        self.attack = "2d4"
        self.defense = "1d4"
        self.damage = "1d4"


class HellHound(Monster):

    def __post_init__(self):
        self.hp = 80
        self.attack = "1d20"
        self.defense = "1d6"
        self.damage = "3d4"
        self.resist_fire = 20
        self.resist_cold = -10
        self.damage_fire = 5


class Hornet(Monster):

    def __post_init__(self):
        self.hp = 40
        self.attack = "1d6"
        self.defense = "1d20"
        self.damage = "1d2"
        self.damage_poison = 10


class DirectDamage:

    def __init__(self):
        self.damage = "1d4"
        self.victims = 1
        # ---- elemental damage ----
        self.damage_fire = 0
        self.damage_cold = 0
        self.damage_poision = 0
        self.damage_electro = 0
        self.__post_init__()

    def __post_init__(self):
        pass


class Thunderbolt(DirectDamage):

    def __post_init__(self):
        self.damage = "1d6"
        self.damage_electro = "4d6"


class Fireball(DirectDamage):

    def __post_init__(self):
        self.damage = "2d6"
        self.damage_fire = "2d6"
        self.victims = "1d3+2"


class PoisonCloud(DirectDamage):
    pass


class Dwarf(Monster):
    pass


class Card:
    cards = {
        0: Thunderbolt,
        25: Fireball,  # 46-25 = 20%
        46: PoisonCloud,  # 50-46 = 1%
        50: Hornet,
        80: Minion,
        85: Dwarf,  # up-low = 90-85 = 5%
        90: HellHound,
    }

    def __init__(self):
        self.r = random.randint(1, 100)
        cardranks = Card.cards.keys()
        for x in range(100):
            if x <= self.r and x in cardranks:
                self.effect = Card.cards[x]
                self.lower_limit = x
            if x > self.r and x in cardranks:
                self.upper_limit = x
                break
        else:
            self.upper_limit = 100
        self.percentage = self.upper_limit - self.lower_limit

    def __repr__(self):
        return f"Effect: {self.effect.__name__:>20} | Card ID: {self.r:>3} | P(Card): {self.percentage:>5.1f}%"


def dicethrow(dicestring="1d6+0"):
    if "+" in dicestring:
        fix = int(dicestring.split("+")[1])
        rest = dicestring.split("+")[0]
    else:
        fix = 0
        rest = dicestring
    if not "d" in rest.lower():
        raise ValueError("dicestring must have a 'd' like '1d6+2'")
    if "D" in dicestring:
        rerolling = True
    else:
        rerolling = False
    throws = int(rest.lower().split("d")[0])
    die = int(rest.lower().split("d")[1])
    # --- roll ---
    # print("rolling " + dicestring + ": ", end="")
    total = 0
    for number in range(throws):
        if rerolling:
            roll = reroll(die)
        else:
            roll = random.randint(1, die)
            # print(roll, end="")
        # print("+", end="")
        total += roll
    # print(fix, end="")
    # print("=", total + fix)
    return total + fix


def reroll(sides):
    """
    dicestring must have a capital D like '1D6'
    the part before the 'D' is number of dice
    the parte after 'D' is number of sides per die
    when a die rolls the highest number, it is counted as
    (sides -1) and rolls again (this can repeated theoretically endless)
    """
    total = 0
    roll = random.randint(1, sides)
    # print(roll, end="")
    if roll == sides:
        # print("-1+", end="")
        total += (sides - 1) + reroll(sides)
    else:
        total += roll
    return total


# -----

def ask_players(players):
    """
    show for each player: horstile armies and own army
    show for each player: own deck of cards
    ask each player: to select card
    ask each player: to select opponent
    """
    for player in players:
        print(f"--- this is your turn, player {player.name} -----")
        input("press enter to continue")
        for enemy in [p for p in players if p != player]:
            print(f" ----- hostile army of {enemy.name}: -----")
            enemy.show_army()
        print(f"\n ====== friendly army of {player.name}: ======= ")
        player.show_army()
        # ------- choose victim ----
        # --- auto-choose victim if only 2 players exist ---
        if len(players) <= 1:
            raise ValueError("You need at last 2 2players")
        elif len(players) == 2:
            players[0].victim = players[1]
            players[1].victim = players[0]
        else:
            # ask to choose a victim among the surviving enemies
            while True:
                for enemy in [p for p in players if p != player and p.hp > 0]:
                    print(f"# {enemy.number}  {enemy.name} ({enemy.hp} hp)")
                number = input("please enter the number (#) of the enemy you want to attack >>>")
                try:
                    number = int(number)
                except ValueError:
                    print("This was not a number. please try again")
                    continue
                if number in [p.number for p in players if p != player and p.hp > 0]:
                    player.victim = [p for p in players if p.number == number][0]
                    break

        # ------- choose card ------
        # print(player.name, "your deck of cards:")
        player.show_deck()
        try:
            i = int(input("Card Index? >>> "))
        except ValueError:
            print("Please enter an integer, NOT a string\n")
            continue
        player.i = i
        print(f"{player.name}'s choice is {player.deck[player.i].effect.__name__}.")
    print("battle")


def clean_armies(players):
    # ----- CLEANSING of the army -----
    for player in players:
        # if player.hp <= 0:
        #    print("You are so bad at this game", player.name)
        player.army = [m for m in player.army if m.hp > 0]


# ----------------------------
def main():
    # ---------- get player names ----------
    players = []
    while True:
        c = input(f"Enter name of player{len(players) + 1} >>> ")
        if c == "":
            break
        p = Wizard()
        p.name = c
        players.append(p)
    print("Each player gets 5 cards")
    for p in players:
        for _ in range(5):
            p.deck.append(Card())  # TODO make card stack

    # ======= ----- turns , main loop ----- ====================
    while True:
        if len([p for p in players if p.hp > 0]) <= 1:
            # -------------- less than two players survived -------
            print("===== GAME OVER =====")
            survivors = [p for p in players if p.hp > 0]
            if len(survivors) == 0:
                print("result: DRAW. No player survived")
            elif len(survivors) == 1:
                print(f"result: VICTORY for {[p.name for p in players if p.hp > 0]}")
            break
        # ---- the battle continues ----
        ask_players(players)  # get played card and victim from each player
        # ----- ...TO BATTLE!!! -----
        print("Calculating Battle Consequences...")  # ;)
        for player in players:
            print("----------------------------")
            print(f"processing {player.name}...")
            # --- write for each player the actions (played card) of his enemies ---
            player.text.append("actions of your enemies....")
            for enemy in [p for p in players if p != player]:
                card = enemy.deck[enemy.i]
                victim = enemy.victim.name if enemy.victim.name != player.name else "YOU"
                prefix = "HOSTILE ACTION:     " if victim == "YOU" else ".....neutral action:"
                if Monster in card.effect.__bases__:
                    player.text.append(f"A {card.effect.__name__} joins the army of {enemy.name}!")
                elif DirectDamage in card.effect.__bases__:
                    player.text.append(f"{prefix} {enemy.name} cast {card.effect.__name__} against {victim}!")
                player.text.append(f"{prefix} {enemy.name}'s army attacks {victim}!")
        #  ---- write and process for each player his own actions (played card) ----
        for player in players:
            card = player.deck[player.i]
            player.text.append("....your own actions...")
            # ------- process monster cards
            if Monster in card.effect.__bases__:
                player.army.append(card.effect())
                player.text.append(f"A {card.effect.__name__} joins your army")
        # ----------- magic phase of combat ---------
        # ------ process damages from direct damage card
        for player in players:
            card = player.deck[player.i]
            # ------- process direct damages --------
            if DirectDamage in card.effect.__bases__:
                victim_monster = random.choice(player.victim.army)
                effect = card.effect()
                damage = dicethrow(effect.damage)
                victim_monster.history.append([damage, effect, player])
                # victim_monster.hp -= damage
                player.text.append(f"You cast {card.effect.__name__} against {player.victim.name}' army")
                player.text.append(
                    f"---> {victim_monster.shortname} of {player.victim.name}'s army suffers {damage} damage. ({victim_monster.hp - damage} left)")
                # ----- process recived direct damage -----
        for player in players:
            player.text.append("recived direct damage effects for your own army")
            for soldier in player.army:
                for damage, effect, enemy in soldier.history:
                    player.text.append(
                        f"Your {soldier.shortname} looses {damage} hp ({soldier.hp - damage}hp left) from direct damage {effect.__class__.__name__} of  {enemy.name}")
                    # --- actually subtract hitpoints because of magic damage ----
                    soldier.hp -= damage
                soldier.history = []
            player.text.append("end of direct damage phase")
        # remove dead monsters
        clean_armies(players)
        # ----------------- melee phase (attack) ----------
        ## ----- Army vs. Army, Monster vs. Monster  -----
        for player in players:
            enemy = player.victim
            player.text.append("melee phase: your army attacks....")
            #  ---- dishing out damage -----
            for soldier in player.army:
                victim_monster = random.choice(player.victim.army)
                player.text.append(
                    f"Your {soldier.shortname} attacks {victim_monster.shortname} of {player.victim.name}")
                attack = dicethrow(soldier.attack)
                defense = dicethrow(victim_monster.defense)
                damage = dicethrow(soldier.damage)
                result = "fail, defense too hight, zero damage" if defense >= attack else f"sucess, damage: {soldier.damage}={damage} ({victim_monster.hp - damage} hp left)"
                player.text.append(
                    f"attack: {soldier.attack}={attack} vs. defense {victim_monster.defense}={defense}: {result}")
                if attack > defense:
                    victim_monster.history.append([damage, soldier, enemy])
                # the victim remembers for counter-attacking later
                victim_monster.revenge.append(soldier)

        # ----- reciving damage from melee attack phase
        for player in players:
            player.text.append("melee phase: your army is  attacked...")
            for soldier in player.army:
                for damage, opponent, enemy in soldier.history:
                    player.text.append(
                        f"your {soldier.shortname} gets {damage} hp damage from {opponent.shortname} of {enemy.name}")
                soldier.history = []
            # player.text.append("melee phase: end of attack  attacks")

        # ------ your army counterattacks -----
        for player in players:
            player.text.append("melee phase: your army counterattacks...")
            for solider in player.army:
                for enemy in soldier.revenge:
                    attack = dicethrow(soldier.attack)
                    defense = dicethrow(enemy.defense)
                    damage = dicethrow(soldier.damage)
                    # result =    # TODO hier weitermachen

        # ------ output for each player ------
        for player in players:
            print("===== history for ", player.name, "=======")
            input("press enter")
            for line in player.text:
                print(line)
            # if len(player.text) == 0:
            #    print("you suffered no direct damage in this round")
            player.text = []


if __name__ == "__main__":
    main()
    # for _ in range(10):
    #    print(Card())

# ---- testing ----
# dicethrow("3d6")
# dicethrow("4d4+2")
# for _ in range(20):
#    dicethrow("1d20")



