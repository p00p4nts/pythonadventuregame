import time
import random

# Utility function to control text display speed
def slow_print(text, speed=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(speed)
    print()

# Character class to manage player stats and actions
class Character:
    def __init__(self, name, health=100, strength=10, level=1, xp=0, inventory=None):
        if inventory is None:
            inventory = []
        self.name = name
        self.health = health
        self.strength = strength
        self.level = level
        self.xp = xp
        self.inventory = inventory

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def heal(self, amount):
        self.health += amount
        if self.health > 100:
            self.health = 100

    def is_alive(self):
        return self.health > 0

    def gain_xp(self, amount):
        self.xp += amount
        while self.xp >= 100:
            self.xp -= 100
            self.level_up()

    def level_up(self):
        self.level += 1
        self.health = 100  # Reset health on level up
        self.strength += 5
        slow_print(f"\n{self.name} has leveled up to {self.level}! Health and Strength improved.", 0.07)

    def add_item(self, item):
        self.inventory.append(item)

    def use_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False

# Class to manage monster encounters
class Monster:
    def __init__(self, name, health, strength, xp_reward=0):
        self.name = name
        self.health = health
        self.strength = strength
        self.xp_reward = xp_reward

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

# Battle system to handle combat mechanics
def battle(player, monster):
    slow_print(f"\nA wild {monster.name} appears!", 0.07)
    while player.is_alive() and monster.health > 0:
        slow_print(f"\n{player.name} (Health: {player.health}) vs {monster.name} (Health: {monster.health})", 0.07)
        
        # Player's turn
        player_choice = player_turn(player)
        if player_choice == "1":
            damage = random.randint(10, 20) + player.strength
            slow_print(f"\n{player.name} attacks {monster.name} for {damage} damage!", 0.07)
            monster.take_damage(damage)
            if monster.health <= 0:
                slow_print(f"\n{monster.name} has been defeated!", 0.07)
                player.gain_xp(monster.xp_reward)  # Gain XP for defeating monster
                return True
        elif player_choice == "2":
            if player.inventory:
                use_item(player)
            else:
                slow_print("\nYou have no items in your inventory!", 0.07)
        elif player_choice == "3":
            if try_escape(player, monster):
                return False
        else:
            slow_print("\nInvalid choice. You lose your turn.", 0.07)

        # Monster's turn
        if monster.health > 0:
            monster_damage = random.randint(5, 15) + monster.strength
            slow_print(f"\n{monster.name} attacks {player.name} for {monster_damage} damage!", 0.07)
            player.take_damage(monster_damage)
            if not player.is_alive():
                slow_print(f"\n{player.name} has been defeated by {monster.name}!", 0.07)
                return False
    return True

# Function to handle player's turn during battle
def player_turn(player):
    slow_print("\nWhat will you do?", 0.07)
    print("1. Attack")
    print("2. Use item")
    print("3. Run away")
    choice = input("> ")
    return choice

# Use item during battle
def use_item(player):
    slow_print(f"\n{player.name} uses an item!", 0.07)
    slow_print("Which item would you like to use?", 0.07)
    for idx, item in enumerate(player.inventory, 1):
        print(f"{idx}. {item}")
    item_choice = input("> ")
    try:
        item_choice = int(item_choice) - 1
        if item_choice >= 0 and item_choice < len(player.inventory):
            item = player.inventory[item_choice]
            if item == "Healing Potion":
                player.heal(30)
                slow_print(f"\n{player.name} heals 30 health with a Healing Potion.", 0.07)
            elif item == "Strength Elixir":
                player.strength += 5
                slow_print(f"\n{player.name}'s strength increases by 5 with a Strength Elixir.", 0.07)
            player.use_item(item)
        else:
            slow_print("\nInvalid item choice. You lose your turn!", 0.07)
    except ValueError:
        slow_print("\nInvalid choice. You lose your turn!", 0.07)

# Attempt to escape the battle
def try_escape(player, monster):
    slow_print(f"\n{player.name} attempts to run away!", 0.07)
    if random.randint(1, 2) == 1:
        slow_print(f"\n{player.name} successfully escapes from {monster.name}!", 0.07)
        return True
    else:
        slow_print(f"\n{player.name} fails to escape and is forced to fight!", 0.07)
        return False

# Event when the player is victorious and encounters more choices
def after_battle(player, monster):
    slow_print(f"\n{player.name} has defeated the {monster.name}!", 0.07)
    if monster.name == "Goblin":
        slow_print("\nYou find a hidden chest containing a magical sword!", 0.07)
        player.add_item("Magical Sword")
        slow_print(f"\n{player.name} has obtained a Magical Sword.", 0.07)
    # Continue with path choices or other rewards

# Path choices after a successful battle
def next_path(player):
    slow_print("\nAs you venture deeper into the forest, you come across a fork in the path.", 0.07)
    slow_print("Do you wish to take the left path leading to a dark cave, or the right path leading to a village?", 0.07)
    print("1. Left path (Dark Cave)")
    print("2. Right path (Village)")

    choice = input("> ")

    if choice == "1":
        enter_cave(player)
    elif choice == "2":
        enter_village(player)
    else:
        slow_print("\nInvalid choice. The journey ends here.", 0.07)

# Enter the cave path
def enter_cave(player):
    slow_print("\nYou enter the dark cave. It's cold and damp.", 0.07)
    slow_print("Suddenly, a huge rock monster appears!", 0.07)
    rock_monster = Monster("Rock Monster", 120, 10, xp_reward=100)
    if battle(player, rock_monster):
        slow_print(f"\n{player.name} has defeated the Rock Monster!", 0.07)
        slow_print("\nInside the cave, you find a treasure chest filled with gold!", 0.07)
    else:
        slow_print(f"\n{player.name} was defeated in the cave.", 0.07)

# Enter the village path
def enter_village(player):
    slow_print("\nYou walk towards the village. The people seem kind and welcoming.", 0.07)
    slow_print("They offer you food and rest. Afterward, they mention a dangerous dragon to the north.", 0.07)
    slow_print("\nDo you wish to prepare for the dragon fight?", 0.07)
    print("1. Yes")
    print("2. No")

    choice = input("> ")

    if choice == "1":
        player.add_item("Dragon Slayer Sword")
        slow_print("\nThe village blacksmith gives you a Dragon Slayer Sword for your journey.", 0.07)
        slow_print("\nWith your new weapon, you head towards the dragon's lair...", 0.07)
        dragon_battle(player)
    elif choice == "2":
        slow_print("\nYou decide not to fight the dragon and live a quiet life in the village.", 0.07)
        slow_print("\nYour adventure ends peacefully in the village.", 0.07)

# Final battle with the dragon
def dragon_battle(player):
    dragon = Monster("Dragon", 200, 20, xp_reward=200)
    if battle(player, dragon):
        slow_print(f"\n{player.name} has slain the Dragon!", 0.07)
        slow_print("\nYou have saved the village and your homeland. Congratulations!", 0.07)
    else:
        slow_print(f"\n{player.name} was defeated by the Dragon.", 0.07)

# Main game function
def start_game():
    slow_print("Welcome to the Realm of Shadows!", 0.07)
    slow_print("You are a brave adventurer embarking on a journey to save your homeland.", 0.07)
    slow_print("But be warned, dark forces lurk in the shadows, and danger is always near...", 0.07)
    
    # Create a player character
    name = input("\nWhat is your name, adventurer? ")
    player = Character(name)

    # Initial inventory
    player.add_item("Healing Potion")
    player.add_item("Strength Elixir")
    
    slow_print(f"\nWelcome, {player.name}. Your journey begins now.", 0.07)

    # First choice
    slow_print("\nYou stand at the entrance of a dark forest. The trees sway ominously in the wind.", 0.07)
    slow_print("Do you wish to enter the forest or turn back?", 0.07)
    print("1. Enter the forest")
    print("2. Turn back")

    choice = input("> ")

    if choice == "1":
        goblin = Monster("Goblin", 50, 5, xp_reward=50)
        if battle(player, goblin):
            after_battle(player, goblin)
            next_path(player)
    else:
        slow_print("\nYou decide to turn back and leave the adventure behind.", 0.07)
        slow_print("\nYour journey ends before it even begins.", 0.07)

# Start the game
start_game()
