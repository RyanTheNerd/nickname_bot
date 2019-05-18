from config import PREFIX
import asyncio
import random
fight_words = {
    'weapons': ['sword', 'knife', 'garden hose', 'electric guitar', 'banana'],
    'actions': [
        "{0} cuts {1}'s legs off with a {2}", 
        "{0} slices {1}'s head clean off with a {2}", 
        "{0} beats {1} in the head with a {2} until they start bleeding",
    ]
}
    
class Fighter:
    def __init__(self, name):
        self.health = 100
        self.name = name

    def attack(self, victim):
        weapon = random.choice(fight_words['weapons'])
        action = random.choice(fight_words['actions'])

        damage = victim.take_damage()

        output = ""
        output += action.format(self.name, victim.name, weapon)


        output += f" and deals {damage} damage!\n"
        if victim.health <= 0:
            output += f"\n{self.name} WINS!"

        else:
            output += f"{victim.name} is left with {victim.health} health!"


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



