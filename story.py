### story generator
# license: GPL, see https://www.gnu.org/licenses/gpl-3.0.en.html
# (c) 2020 by Max, Simon, Horst JENS.
# Contact: http://spielend-programmieren.at horstjens@gmail.com
# goal: write a text-adventure in python that will eventually become a Discord bot

from dataclasses import dataclass
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

class Decision:

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

    Decision("Choose your weapon wisely...", ["Sword", "Bow", "Pen", "Pebbles", "Stick"],
             intro="Your enemy is famous for",
             introvar = {
            "beating enemies to death with stones":"Pen",
            "swordmanship":"Stick",
            "fantastic aim with a bow and arrow":"Sword",
            "his written lyrics":"Pebbles",
             })
    Decision("wich way to you choose?", ["left", "middle", "right"],
             intro="You halt at a way crossing. Choose your way to the castle of your enemy",
             introvar = {


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
    for decision in Game.decisions.values():
        result = decision.run()
        if not result:
            print("bad")
            break
        print("good")
    else:
        # no break occured, solved all questions correctly!
        print("victory for you!")
    print("Game Over")
