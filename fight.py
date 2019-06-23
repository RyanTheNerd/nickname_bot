from config import PREFIX
import asyncio
import random

fight_words = {
    'weapons': [
        'sword', 
        'knife', 
        'garden hose', 
        'electric guitar', 
        'banana',
        'toothbrush',
        'rake',
        'axe',
        'pair of scissors',
        'light saber',
        'umbrella',
    ],
    'actions': [
        "{0} cuts {1}'s legs off with a {2}", 
        "{0} slices {1}'s head clean off with a {2}", 
        "{0} beats {1} in the head with a {2} until they start bleeding",
        "{0} chokes {1} out with a {2}",
        "{0} stabs {1} in the heart with a {2}",
        "{0} penetrates {1}'s asshole with a {2}",
        "{0} skins {1} alive using nothing but a {2}",
        "{0} rips {1}'s arms off and eats them raw",
    ]
}
"""
Weapons and actions should have weights between 1 and 10
Action function combines a weapon and an action and calculates damage multiplier
"""

class Weapon:
    def __init__(self, name, multipler, a_an='a'):
        self.name = name
        self.multiplier = multiplier
        self.a_an = a_an

class action:
    def __init__(self, weapon, multiplier):
        self.name = name
        self.weapon = weapon
        self.multiplier = multiplier * self.weapon.multiplier

class Fighter:
    def __init__(self, name):
        self.health = 100
        self.name = name

    def attack(self, victim):
        weapon = random.choice(fight_words['weapons'])
        action = random.choice(fight_words['actions'])

        damage = victim.take_damage()

        output = ""
        output += action.format(self.name, victim.name, f"***__{weapon}__***")


        output += f" and deals ***__{damage}__*** damage!\n"
        if victim.health <= 0:
            output += f"\n***__{self.name} WINS!__***"

        else:
            output += f"{victim.name} is left with ***__{victim.health}__*** health!"


        return output

    def take_damage(self):
        damage = random.randrange(0, 100)
        self.health -= damage
        return damage

async def fight(message):
    channel = message.channel
    sides = message.content.split(' VS ')
    if len(sides) != 2:
        return
    left = sides[0]
    right = sides[1]

    if not right.endswith(' FIGHT!'):
        return

    fighter_name1 = left

    fighter_name2 = right[:-len(' FIGHT!')].rstrip(':')



    fighter1 = Fighter(fighter_name1)
    fighter2 = Fighter(fighter_name2)

    attacker = fighter1
    victim = fighter2

    while fighter1.health > 0 and fighter2.health > 0:
        await channel.trigger_typing()
        await asyncio.sleep(5)
        await channel.send(attacker.attack(victim))
        prev_attacker = attacker
        attacker = victim
        victim = prev_attacker

