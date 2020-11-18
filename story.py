### story generator
# license: GPL, see https://www.gnu.org/licenses/gpl-3.0.en.html
# (c) 2020 by Max, Simon, Horst JENS.
# Contact: http://spielend-programmieren.at horstjens@gmail.com
# goal: write a text-adventure in python that will eventually become a Discord bot

from dataclasses import dataclass
import random

names_gender = ["female", "male"]
names_male = ["Hans", "Simon", "Max", "Benjamin", "Oliver", "Issac"]
names_female = ["Gretl", "Sophie", "Amelie", "Esmaralda"]
names_age = ["young", "very young", "far too young", "old", "ancient",
             "middle-aged"]
names_role = ["vagabound", "farmer", "merchant", "soldier",
             "dog breeder", "youtuber", "influcencer",
             "social-media-troll", "boomer", "netflix viewer",
             "pizza deliverer", "dog food taster",
             "sleeper"]
names_adj = ["ugly", "rich", "glorious", "innocent",
             "cheeky", "popular", "influential",
             "beautiful", "shy", "small", "tall",
             "heavy", "fat", "skinny", "funny",
             "discombobulated","scuba-diving", "professional"]

protagonist = random.choice(("a young hero",
                             "Hans, the vagabound",
                             "Simon the wise old man",
                             "Max, the rich merchant",
                             "Gretl, the farmers daughter"
                             ))


@dataclass
class Person:
    name: str = None
    age: str = None
    adjectives = []
    gender: str = None
    role: str = None

    def __post_init__(self):
        """mix the person"""
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
    you = Person()
    gay_chance = 0.1
    if random.random() < gay_chance:
        other_gender = you.gender
        print("you are gay")
    else:
        other_gender = "female" if you.gender == "male" else "male"
    love = Person(gender=other_gender)
    enemy = Person()
    npc1 = Person()
    print("you are:",you )
    print("you search your lost love:", love)
    print("who was kidnapped by your enemy:", enemy)
    print("you see at the moment:", npc1)