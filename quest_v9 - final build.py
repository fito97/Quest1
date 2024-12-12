# -*- coding: utf-8 -*-
"""Quest_v6.ipynb"""

import time
import pygame

# Initialize the pygame mixer
pygame.mixer.init()

# Function to load and play sound for the intro
def play_sound_intro(sound_file):
    sound = pygame.mixer.Sound(sound_file)
    sound.play()


# Function to load and play sound for piano game
def play_sound(sound_file):
    sound = pygame.mixer.Sound(sound_file)
    sound.play()
    # Wait for the sound to finish before proceeding
    time.sleep(sound.get_length())

# Load sounds for piano game
sounds = {
    'a': pygame.mixer.Sound(r"C:\Users\xavie\Downloads\piano notes\c4-shorten.wav"),
    's': pygame.mixer.Sound(r"C:\Users\xavie\Downloads\piano notes\d4-shorten.wav"),
    'd': pygame.mixer.Sound(r"C:\Users\xavie\Downloads\piano notes\e4-shorten.wav"),
    'f': pygame.mixer.Sound(r"C:\Users\xavie\Downloads\piano notes\f4-shorten.wav"),
    'g': pygame.mixer.Sound(r"C:\Users\xavie\Downloads\piano notes\g4-shorten.wav"),
    'h': pygame.mixer.Sound(r"C:\Users\xavie\Downloads\piano notes\a4-shorten.wav"),
    'j': pygame.mixer.Sound(r"C:\Users\xavie\Downloads\piano notes\b4-shorten.wav"),
    'k': pygame.mixer.Sound(r"C:\Users\xavie\Downloads\piano notes\c5-shorten.wav"),
    " ": pygame.mixer.Sound(r"C:\Users\xavie\Downloads\piano notes\silence.wav"),
}









# Function to print text letter by letter (only start and finish text)
def print_typing(text, delay=0.1):
    for letter in text:
        print(letter, end='', flush=True)
        time.sleep(delay)
    print()

# GameRoom

couch = {
    "name": "couch",
    "type": "furniture",
}

door_a = {
    "name": "door a",
    "type": "door",
}

key_a = {
    "name": "key for door a",
    "type": "key",
    "target": door_a,
}

master_key = {
    "name": "master key",
    "type": "key",
    "target": "all",
}

piano = {
    "name": "piano",
    "type": "furniture",
}

game_room = {
    "name": "game room",
    "type": "room",
}

outside = {
  "name": "outside"
}

# BEEDROOM 1

queen_bed = {
    "name": "queen bed",
    "type": "furniture",
}
door_b = {
    "name": "door b",
    "type": "door",
}
door_c = {
    "name": "door c",
    "type": "door",
}
key_b = {
    "name": "key for door b",
    "type": "key",
    "target": door_b,
}
bedroom_1 = {
    "name": "bedroom 1",
    "type": "room",
}

# LIVING ROOM
dining_table = {
    "name": "dining table",
    "type": "furniture",
}

door_d = {
    "name": "door d",
    "type": "door"
}

livingroom = {
    "name": "livingroom",
    "type": "room",
}

# BEDROOM 2

key_c = {
    "name": "key for door c",
    "type": "key",
    "target": door_c,
}
key_d = {
    "name": "key for door d",
    "type": "key",
    "target": door_d,
}
double_bed = {
    "name": "double bed",
    "type": "furniture",
}

dresser = {
    "name": "dresser",
    "type": "furniture",
}

bedroom_2 = {
    "name": "bedroom 2",
    "type": "room",
}

all_rooms = [game_room, outside, bedroom_1, livingroom, bedroom_2]

all_doors = [door_a, door_b, door_c, door_d]

# define which items/rooms are related

object_relations = {
    "game room": [couch, piano, door_a],
    "couch": [master_key],
    "piano": [key_a],
    "outside": [door_d],
    "door a": [game_room, bedroom_1],
    "bedroom 1": [queen_bed, door_b, door_c, door_a],
    "queen bed": [key_b],
    "bedroom 2": [double_bed, dresser, door_b],
    "door b": [bedroom_1, bedroom_2],
    "double bed": [key_c],
    "dresser": [key_d],
    "door c": [bedroom_1, livingroom],
    "livingroom": [door_c, door_d, dining_table],
    "door d": [outside, livingroom]
}

# define game state. Do not directly change this dict.
# Instead, when a new game starts, make a copy of this
# dict and use the copy to store gameplay state. This
# way you can replay the game multiple times.

INIT_GAME_STATE = {
    "current_room": game_room,
    "keys_collected": [],
    "target_room": outside,
    "previa_room": None  # Keep track of the previous room
}

def linebreak():
    """
    Print a line break
    """
    print("\n\n")

def start_game():
    """
    Start the game
    """
    typing_text = (
        "\033[1mYou wake up on a couch and find yourself in a strange house with no windows "
        "which you have never been to before. You don't remember why you are here and what "
        "had happened before. You feel some unknown danger is approaching and you must get out "
        "of the house, NOW!\033[0m"
    )
    play_sound_intro(r"C:\Users\xavie\Downloads\man waking up - sound effect.wav") # Play sound waking up
    print_typing(typing_text, delay=0.01)  # Adjust delay time of letters rendering
    play_room(game_state["current_room"])

def play_room(room):
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let the player either
    explore (list all items in this room) or examine an item found here.
    """
    game_state["previa_room"] = game_state["current_room"]
    game_state["current_room"] = room

    if game_state["current_room"] == game_state["target_room"]:
        end_text = (
            "\033[1mCongrats! You escaped the room!\033[0m"
        )
        print_typing(end_text, delay=0.05)  # Adjust delay time of letters rendering
    else:
        if game_state["previa_room"] != game_state["current_room"]:
            print("You are now in " + room["name"])
        intended_action = input("What would you like to do? Type 'explore' or 'examine'? ").strip()
        if intended_action == "explore":
            explore_room(room)
            play_room(room)
        elif intended_action == "examine":
            examine_item(input("What would you like to examine?").strip())
        else:
            print("Not sure what you mean. Type 'explore' or 'examine'. ")
            play_room(room)
        linebreak()

def explore_room(room):
    """
    Explore a room. List all items belonging to this room.
    """
    items = [i["name"] for i in object_relations[room["name"]]]
    print("You explore the room. This is " + room["name"] + ". You find " + ", ".join(items))

def get_next_room_of_door(door, current_room):
    """
    From object_relations, find the two rooms connected to the given door.
    Return the room that is not the current_room.
    """
    connected_rooms = object_relations[door["name"]]
    for room in connected_rooms:
        if not current_room == room:
            return room

def examine_item(item_name):
    """
    Examine an item which can be a door or furniture.
    First make sure the intended item belongs to the current room.
    Then check if the item is a door. Tell player if key hasn't been
    collected yet. Otherwise ask player if they want to go to the next
    room. If the item is not a door, then check if it contains keys.
    Collect the key if found and update the game state. At the end,
    play either the current or the next room depending on the game state
    to keep playing.
    """
    current_room = game_state["current_room"]
    next_room = ""
    output = None

    for item in object_relations[current_room["name"]]:
        if item["name"] == item_name:
            output = "You examine " + item_name + ". "
            if item["name"] == "piano":
                while True:
                    user_input = input("Press keys (a, s, d, f, g, h, j, k): Type exit to stop paying: ")
                    if user_input.lower() == 'exit':
                        break # Stop playing piano
                    for char in user_input:
                        if char in sounds:
                            play_sound(sounds[char]) # Play the note
                        else:
                            print(f"Key '{char}' not recognized. Please use a, s, d, f, g, h, j, k. ")






            if item["type"] == "door":
                have_key = False
                master_key_found = False
                # Check if player has the master key
                for key in game_state["keys_collected"]:
                    if key["target"] == "all":
                        master_key_found = True
                        break
                # If master key is found, unlock the door
                if master_key_found:
                    output += "The master key opens the door."
                    next_room = get_next_room_of_door(item, current_room)
                else:
                    # Otherwise, check for specific key for the door
                    for key in game_state["keys_collected"]:
                        if key["target"] == item:
                            have_key = True
                    if have_key:
                        output += "You unlock it with a key you have."
                        play_sound(r"C:\Users\xavie\Downloads\locking door - sound effect.wav")  # Play spund opening
                        next_room = get_next_room_of_door(item, current_room)
                    else:
                        output += "It is locked but you don't have the key."
            else:
                if item["name"] in object_relations and len(object_relations[item["name"]]) > 0:
                    item_found = object_relations[item["name"]].pop()
                    game_state["keys_collected"].append(item_found)
                    output += "You find " + item_found["name"] + "."
                else:
                    output += "There isn't anything interesting about it."
            print(output)
            break

    if output is None:
        print("The item you requested is not found in the current room. ")

    if next_room and input("Do you want to go to the next room? Enter 'yes' or 'no': ").strip() == 'yes':
        play_room(next_room)
    else:
        play_room(current_room)

game_state = INIT_GAME_STATE.copy()

start_game()
