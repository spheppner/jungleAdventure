### story generator
# license: GPL, see https://www.gnu.org/licenses/gpl-3.0.en.html
# (c) 2020 by Max, Simon, Horst JENS.
# Contact: http://spielend-programmieren.at horstjens@gmail.com
# goal: write a text-adventure in python that will eventually become a Discord bot

from dataclasses import dataclass
from collections import namedtuple
import random

names_gender = ["female", "male"]
names_male = ["Hans", "Simon", "Max", "Benjamin", "Oliver", "Isaak", "Peter",
              "Stefan", "Anton", "Maurice", "Martin", "Heinrich", 
              "Carl-Constantin", "Paul", "Mustafa", "Hakan", "Carlos", "Elias",
              "Daniel", "Javier", "Karl", "Juan", "David"]
names_female = ["Gretl", "Sophie", "Amelie", "Esmaralda", "Anna", 
                "Charlotte", "Sabine", "Barbara", "Julia", "Katja", "Katharina", 
                "Lisa", "Sonja", "Emma", "Dilara", "Fatima", "Theresa"
                "Lara", "Sarah", "Tamara", "Lauren"]
names_age = ["young", "very young", "far too young", "old", "ancient",
             "middle-aged", "not even born yet"]
names_role = ["vagabound", "farmer", "merchant", "soldier",
             "dog breeder", "youtuber", "influcencer",
             "social-media-troll", "boomer", "netflix viewer",
             "pizza deliverer", "dog food taster",
             "sleeper", "software-developer", "discord-mod",
             "athlete", "minecraft-speedrunner", "streamer",
             "memepage-admin", "teacher", "musician", "painter",
             "graphic-designer"]
names_adj = ["ugly", "rich", "glorious", "innocent",
             "cheeky", "popular", "influential",
             "beautiful", "shy", "small", "tall",
             "heavy", "fat", "skinny", "funny",
             "discombobulated", "professional",
             "dumb", "smart", "happy", "sad", 
             "exhausted", "stressed", "depressed",
             "fascinated", "drunk", "high"]

protagonist = random.choice(("a young hero",
                             "Hans, the vagabound",
                             "Simon the wise old man",
                             "Max, the rich merchant",
                             "Gretl, the farmers daughter"
                             ))


class Game:
    person_number = 0
    people = {}
    decision_number = 0
    decisions = {}
    you = None
    enemy = None
    love = None
    npc1 = None
    deck = []

class Decision:
    # TODO: typing.namedtuple ?

    def __init__(self, question, answers, intro="", introvar={} ):
        self.number = Game.decision_number
        Game.decision_number += 1
        Game.decisions[self.number] = self
        self.question = question
        self.answers = answers
        self.correct_answer = answers[0]
        self.intro = intro
        self.introvar = introvar

    def run(self):
        print("-------")
        print(self.intro)
        iv = random.choice(list(self.introvar.keys()))
        print(iv)
        self.correct_answer = self.introvar[iv]
        print("-------")
        print(self.question)
        random.shuffle(self.answers)
        for i, answer in enumerate(self.answers):
            print(i, answer)
        command = int(input("please enter number:"))
        if self.answers[command] == self.correct_answer:
            return True
        else:
            return False


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





        #self.damage =




@dataclass
class Person:
    name: str = None
    age: str = None
    adjectives = []
    gender: str = None
    role: str = None
    number: int = None

    def __post_init__(self):
        """mix the person"""
        self.number = Game.person_number
        Game.person_number += 1
        Game.people[self.number] = self

        if self.gender is None:
            self.gender = random.choice(names_gender)
        if self.name is None:
            if self.gender == "male":
                self.name = random.choice(names_male)
            else:
                self.name = random.choice(names_female)
        if self.role is None:
            self.role = random.choice(names_role)
        if self.age is None:
            self.age = random.choice(names_age)
        if self.adjectives is None:
            number_of_adj = random.choice((0,0,0,0,1,1,1,1,1,2,2,3))
            for _ in range(number_of_adj):
                self.adjectives.append(random.choice(names_adj))


if __name__ == "__main__":
    Game.you = Person()
    gay_chance = 0.1
    if random.random() < gay_chance:
        other_gender = Game.you.gender
        print("you are gay")
    else:
        other_gender = "female" if Game.you.gender == "male" else "male"
    Game.love = Person(gender=other_gender)
    Game.enemy = Person()
    Game.npc1 = Person()
    Decision("Dou you want to save your love?", ["Yes", "No", "Maybe", "Later, i'm busy right now"],
             intro="first question",
             introvar={"":"Yes"})

    Decision("Choose your weapon wisely...", ["Sword", "Bow", "Pen", "Pebbles"],
             intro="Your enemy is famous for",
             introvar = {
            "beating enemies to death with stones":"Pen",
            "swordmanship":"Bow",
            "fantastic aim with a bow and arrow":"Sword",
            "his written lyrics":"Pebbles",
             })
    Decision("wich way do you choose?", ["through the giant toaster", "through the forest of super cool snakes", "through the forest of tasty trees "],
             intro="You halt at a way crossing. Due to the current situation you have to choose wisely to survive.",
             introvar = {
            "In the land of giant butterflies there was a Power failure. Choose a way to take benefit from this disaster" : "through the giant toaster",
            "It is very hot right now, your body needs to get cooler fast. Which one is the right way" : "through the forest of super cool snakes",
            "You are very hungry and any food will help you. Choose the right way to not die of hunger" : "through the forest of tasty trees"

             }
             )
    Decision("what do you do?", ["hit him with a toaster",
                                                  "walk through him",
                                                  "eat him"],
             intro="A ghost appears, made out of :",
             introvar = {"smoke": "walk through him",
                         "pizza-dough": "eat him",
                         "dirt": "hit him with a toaster"
             })



    print("you are:",Game.you )
    print("you search your lost love:", Game.love)
    print("who was kidnapped by your enemy:", Game.enemy)
    print("you see at the moment:", Game.npc1)
    print("----- oll persons in this game: -------")
    for p in Game.people.values():
        print(p)
    # --------------- game loop ----------------------------
    decs = [d for d in Game.decisions.values()]
    d1 = decs.pop(0) # remove the first item
    random.shuffle(decs)
    decs.insert(0, d1)
    for decision in Game.decisions.values():
        result = decision.run()
        if not result:
            print("bad")
            break
        print("good")

        if random.random() < 0.33:
            while True:
                print("you have a chance to fight the enemy directly. do you...")
                command=input("(f)ight or (r)un ?")
                if command.lower() in ["f", "r"]:
                    break
            if command == "f":
                bossfight()
        else:
            print("You get a new card!")
            Game.deck.append(Card())
            print("your deck of cards:", Game.deck)
    else:
        # no break occured, solved all questions correctly!
        print("victory for you!")
    print("Game Over")
