import time
import random

# Pause function to control text display speed
def slow_print(text, speed=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(speed)
    print()

# Character class to manage player stats
class Character:
    def __init__(self, name, health, strength, level=1, inventory=None, xp=0):
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

    def add_item(self, item):
        self.inventory.append(item)

    def use_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False

    def gain_xp(self, amount):
        self.xp += amount
        while self.xp >= 100:
            self.xp -= 100
            self.level_up()

    def level_up(self):
        self.level += 1
        self.health = 100  # Reset health when leveling up
        self.strength += 5
        slow_print(f"\n{self.name} has reached level {self.level}! Health and strength have increased.", 0.07)

# A simple battle system
def battle(player, enemy):
    slow_print(f"\nA wild {enemy['name']} appears!", 0.07)
    while player.is_alive() and enemy['health'] > 0:
        slow_print(f"\n{player.name} (Health: {player.health}) vs {enemy['name']} (Health: {enemy['health']})", 0.07)
        
        # Player's turn
        slow_print("\nWhat do you want to do?", 0.07)
        print("1. Attack")
        print("2. Use item")
        print("3. Run away")
        
        choice = input("> ")

        if choice == "1":
            damage = random.randint(10, 20) + player.strength
            slow_print(f"\n{player.name} attacks {enemy['name']} for {damage} damage!", 0.07)
            enemy['health'] -= damage
            if enemy['health'] <= 0:
                slow_print(f"\n{enemy['name']} has been defeated!", 0.07)
                player.gain_xp(50)  # Gain XP for defeating an enemy
                return True
        elif choice == "2":
            if player.inventory:
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
            else:
                slow_print("\nYou have no items in your inventory!", 0.07)
        elif choice == "3":
            slow_print("\nYou attempt to run away!", 0.07)
            if random.randint(1, 2) == 1:
                slow_print(f"\n{player.name} successfully escapes from the battle!", 0.07)
                return False
            else:
                slow_print(f"\n{player.name} fails to escape and is forced to fight!", 0.07)
        else:
            slow_print("\nInvalid choice. You lose your turn!", 0.07)
        
        # Enemy's turn
        if enemy['health'] > 0:
            enemy_damage = random.randint(5, 15)
            slow_print(f"\n{enemy['name']} attacks {player.name} for {enemy_damage} damage!", 0.07)
            player.take_damage(enemy_damage)
            if not player.is_alive():
                slow_print(f"\n{player.name} has been defeated by {enemy['name']}!", 0.07)
                return False
    return True

# Function to display the player's status
def show_status(player):
    slow_print(f"\n{player.name}'s Status:", 0.07)
    slow_print(f"Health: {player.health}/100", 0.07)
    slow_print(f"Strength: {player.strength}", 0.07)
    slow_print(f"Level: {player.level}", 0.07)
    slow_print(f"XP: {player.xp}/100", 0.07)
    slow_print(f"Inventory: {', '.join(player.inventory) if player.inventory else 'Empty'}", 0.07)

# Main game function
def start_game():
    # Introduction to the game
    slow_print("Welcome to the Realm of Shadows!", 0.07)
    slow_print("You are a brave adventurer embarking on a journey to save your homeland.", 0.07)
    slow_print("But be warned, dark forces lurk in the shadows, and danger is always near...", 0.07)
    
    # Create a player character
    name = input("\nWhat is your name, adventurer? ")
    player = Character(name, health=100, strength=10)

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
        slow_print("\nYou take a deep breath and step into the forest...", 0.07)
        time.sleep(1)

        # Encounter with a monster
        monster = {
            "name": "Goblin",
            "health": 50
        }
        if battle(player, monster):
            slow_print(f"\n{player.name}, you have defeated the Goblin!", 0.07)
            slow_print("\nAfter the battle, you find a hidden chest containing a magical sword.", 0.07)
            player.add_item("Magical Sword")
            slow_print("\nYou now have a Magical Sword in your inventory.", 0.07)

            # Second choice
            slow_print("\nAs you venture deeper into the forest, you come across a fork in the path.", 0.07)
            slow_print("Do you wish to take the left path leading to a dark cave, or the right path leading to a village?", 0.07)
            print("1. Left path (Dark Cave)")
            print("2. Right path (Village)")

            choice = input("> ")

            if choice == "1":
                slow_print("\nYou enter the dark cave. It's cold and damp.", 0.07)
                slow_print("Suddenly, a huge rock monster appears!", 0.07)
                monster = {
                    "name": "Rock Monster",
                    "health": 120
                }
                if battle(player, monster):
                    slow_print(f"\n{player.name}, you have defeated the Rock Monster!", 0.07)
                    slow_print("\nInside the cave, you find a treasure chest filled with gold!", 0.07)
                else:
                    slow_print(f"\n{player.name} was defeated in the cave.", 0.07)
                    return

            elif choice == "2":
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
                    # Final encounter with the Dragon
                    monster = {
                        "name": "Dragon",
                        "health": 200
                    }
                    if battle(player, monster):
                        slow_print(f"\n{player.name}, you have slain the Dragon!", 0.07)
                        slow_print("\nYou have saved the village and your homeland. Congratulations!", 0.07)
                    else:
                        slow_print(f"\n{player.name} was defeated by the Dragon.", 0.07)
                        return

                else:
                    slow_print("\nYou decide not to fight the dragon and live a quiet life in the village.", 0.07)
                    slow_print("\nYour adventure ends peacefully in the village.", 0.07)
                    return

    else:
        slow_print("\nYou decide to turn back and leave the adventure behind.", 0.07)
        slow_print("\nYour journey ends before it even begins.", 0.07)
        return

# Start the game
start_game()
