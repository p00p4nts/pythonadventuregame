import time
import random

# Utility function to control text display speed
def slow_print(text, speed=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(speed)
    print()

# Character class to manage player stats, inventory, and actions
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

# Class to handle different monsters in the game
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

# Battle system that handles combat
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
                player.gain_xp(monster.xp_reward)
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

# Function to handle the player's choices during battle
def player_turn(player):
    slow_print("\nWhat will you do?", 0.07)
    print("1. Attack")
    print("2. Use item")
    print("3. Run away")
    choice = input("> ")
    return choice

# Use an item during battle
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

# Attempt to escape battle
def try_escape(player, monster):
    slow_print(f"\n{player.name} attempts to run away!", 0.07)
    if random.randint(1, 2) == 1:
        slow_print(f"\n{player.name} successfully escapes from {monster.name}!", 0.07)
        return True
    else:
        slow_print(f"\n{player.name} fails to escape and is forced to fight!", 0.07)
        return False

# Random events that may alter the course of the game
def random_event(player):
    event_chance = random.randint(1, 10)  # 1 in 10 chance for an event
    if event_chance == 1:
        slow_print("\nYou find a strange portal flickering before you...", 0.07)
        portal_to_ww2(player)
    else:
        slow_print("\nYou encounter nothing unusual and continue your journey.", 0.07)

# WWII Portal Event: The player is teleported to Stalingrad
def portal_to_ww2(player):
    slow_print("\nA mysterious force pulls you into a portal...", 0.07)
    slow_print("\nSuddenly, you find yourself on a boat in the middle of a violent river...", 0.07)
    slow_print("\nIt's 1942. You are about to land at Stalingrad during the fiercest battles of WWII!", 0.07)
    slow_print("\nYour fellow soldiers are around you, readying for combat. A gruff sergeant shouts orders.", 0.07)
    slow_print("\nThe boat rocks violently as you approach the shore. The air is thick with gunfire.", 0.07)
    
    # Quick dialogue with comrades
    slow_print("\nA soldier beside you whispers nervously: 'You think we're going to make it out of here?'")
    choice = input("Do you respond?\n1. 'I believe we will.'\n2. 'It doesn't matter. We have to do our duty.'\n> ")
    if choice == "1":
        slow_print("\nThe soldier nods, 'Let's hope you're right...'", 0.07)
    elif choice == "2":
        slow_print("\nThe soldier looks uneasy but nods, 'You're right. We have to keep moving forward.'", 0.07)

    # Start the combat mission in Stalingrad
    mission_outcome(player)

# The Stalingrad mission: survive or get captured
def mission_outcome(player):
    slow_print("\nThe boat finally reaches the shore. You and your comrades rush to the battlefield...", 0.07)
    slow_print("\nMachine guns rattle. Explosions are everywhere. You have to survive!", 0.07)
    
    # Random combat sequence
    enemy_type = random.choice(["German Soldier", "Sniper", "Tank Crew"])
    enemy_health = 100
    enemy_damage = random.randint(10, 20)
    enemy_xp = 50
    enemy = Monster(name=enemy_type, health=enemy_health, strength=enemy_damage, xp_reward=enemy_xp)

    if battle(player, enemy):
        slow_print(f"\n{player.name}, you survived the battle and continue to fight!", 0.07)
        # Further combat or escape options could unfold here based on the choices made
    else:
        slow_print(f"\n{player.name} was captured or killed in the chaos of battle.", 0.07)

# Main function to start the game
def start_game():
    slow_print("Welcome to the Realm of Shadows!", 0.07)
    slow_print("You are a brave adventurer embarking on a journey to save your homeland.", 0.07)
    slow_print("But be warned, dark forces lurk in the shadows, and danger is always near...", 0.07)
    
    name = input("\nWhat is your name, adventurer? ")
    player = Character(name)
    
    slow_print(f"\nWelcome, {player.name}. Your journey begins now.", 0.07)
    
    # Player starts exploring the world
    random_event(player)

# Start the game
start_game()
