import sys
import os
import zmq
import json

class Cat:
    def __init__(self, name):
        socket_rng.send_string("generate")
        starting_kibble = socket_rng.recv_string()

        self.name = name
        self.hunger = 10
        self.happiness = 10
        self.max_happiness = 10
        self.energy = 5
        self.max_energy = 10
        self.kibble = int(starting_kibble)
    
    def to_dict(self):
        return {
            "name": self.name,
            "hunger": self.hunger,
            "happiness": self.happiness,
            "max_happiness": self.max_happiness,
            "energy": self.energy,
            "max_energy": self.max_energy,
            "kibble": self.kibble,
        }
    def apply_dict(self, data: dict):
        for k in ("name", "hunger", "happiness", "max_happiness", "energy", "max_energy", "kibble"):
            if k in data:
                setattr(self, k, data[k])

def clear_screen():
    if sys.platform.startswith('win'):
        os.system('cls')
    else:
        os.system('clear')

def draw_cat():
    print("/\_/\ ♥")
    print(">^,^<")
    print(" / \\")
    print("(___)_/")
    print("\n")

def display_welcome():
    clear_screen()
    socket_ascii.send_string(f"ascii:VirtuaCat")
    ascii_art = socket_ascii.recv_string()
    print(ascii_art)
    draw_cat()
    print("Welcome to Virtua-Cat Simulator!")
    print("Adopt and care for your very own pet.\n\n")
    user_input = input("Press enter to continue...")

def adopt_cat(cat):
    clear_screen()
    draw_cat()
    print("Good job! You've adopted your cat.")
    print("You can check the status of your cat at any time from the main menu to make sure it is well cared for.\n")
    print("Before you adopt your cat, let's name it! Please enter its name below.\n")
    cat.name = input("Name: ")

def display_command_screen(cat):
    clear_screen()
    draw_cat()
    print("1: (C)heck Status of cat")
    print("2: (F)eed cat (costs 1 kibble)")
    print("3: (R)ename cat")
    print("4: (Q)uit\n")
    print("5: (S)ave cat")
    print("6: (L)oad cat")
    print("7: (D)elete cat\n")
    choose_action(cat)

def choose_action(cat):
    user_input = input("Input command: ")
    choice = user_input.lower()
    if choice == "1" or choice == "c":
        display_status(cat)
    elif choice == "2" or choice == "f":
        feed_cat(cat)
    elif choice == "3" or choice == "r":
        rename_cat(cat)
    elif choice == "4" or choice == "q":
        quit_program()
    elif choice == "5" or choice == "s":
        save_cat()
    elif choice == "6" or choice == "l":
        load_cat()
    elif choice == "7" or choice == "d":
        delete_save()
        
def display_status(cat):
    clear_screen()
    print(f"Name = {cat.name}")
    print(f"Hunger = {cat.hunger}")
    print(f"Happiness = {cat.happiness}")
    print(f"Energy = {cat.energy}")
    print(f"Kibble = {cat.kibble}")
    socket_noun.send_string(f"1 food")
    food = socket_noun.recv().decode("utf-8")
    print(f"Your cat is thinking about {food}.")
    input(f"\nPress Enter to Continue...")

def feed_cat(cat):
    clear_screen()
    if cat.kibble > 0:
        cat.kibble -= 1
        cat.hunger -= 1
        if cat.hunger < 0: cat.hunger = 0
        print("You feed your cat some kibble. Yum!")
        print(f"Kibble Stock: {cat.kibble} left")
        print(f"Hunger: {cat.hunger}")
        input("Press enter to continue... ")
    else:
        print("You don't have any kibble to feed your cat")
        input("Press enter to continue... ")

def rename_cat(cat):
    clear_screen()
    print("If you'd like to rename your cat, type its new name below.")
    print("Otherwise, leave it blank and press enter to keep its current name.")
    new_name = input("Name: ")

    if new_name != "":
        cat.name = new_name

def quit_program():
    clear_screen()
    print("Are you sure you want to quit?")
    print("Any unsaved cat data will be cleared.")
    user_input = input("\nAre you sure you want to proceed? (Yes/No): ")
    choice = user_input.lower()
    if choice == "yes" or choice == "y":
        quit()

def save_cat():
    request = {"action": "save", "data": cat.to_dict()}
    socket_save.send(json.dumps(request).encode("utf-8"))
    resp = socket_save.recv().decode("utf-8")
    print("SERVER:", resp)
    input("\nPress Enter to continue")

def list_saves():
    request = {"action": "get_all"}
    socket_save.send(json.dumps(request).encode("utf-8"))
    resp = socket_save.recv().decode("utf-8")
    try:
        items = json.loads(resp)
    except Exception:
        items = []
    return items

def load_cat():
    items = list_saves()
    if not items:
        print("No saved cats available.")
        input("\nPress Enter to continue...")
        return

    print("\nSaved Cats:")
    for i, item in enumerate(items):
        # show a brief summary (name + hunger)
        name = item.get("name", "<unknown>")
        hunger = item.get("hunger", "?")
        print(f"[{i}] {name} (hunger={hunger})")

    try:
        idx = int(input("\nEnter index to load: "))
    except ValueError:
        print("Invalid input.")
        input("\nPress Enter to continue...")
        return

    if 0 <= idx < len(items):
        saved = items[idx]
        cat.apply_dict(saved)
        print(f"Loaded save [{idx}] into current cat.")
    else:
        print("Index out of range.")
    input("\nPress Enter to continue...")

def delete_save():
    items = list_saves()
    if not items:
        print("No saved data to delete.")
        input("\nPress Enter to continue...")
        return

    print("\nSaved Items:")
    for i, item in enumerate(items):
        print(f"[{i}] {item.get('name','<no name>')}")

    try:
        idx = int(input("\nEnter index number to delete: "))
    except ValueError:
        print("Invalid input.")
        input("\nPress Enter to continue...")
        return

    request = {"action": "delete", "index": idx}
    socket_save.send(json.dumps(request).encode("utf-8"))
    resp = socket_save.recv().decode("utf-8")
    print("SERVER:", resp)
    input("\nPress Enter to continue...")

if __name__ == "__main__":
    context = zmq.Context()

    socket_ascii = context.socket(zmq.REQ)
    socket_ascii.connect("tcp://localhost:5557")

    socket_rng = context.socket(zmq.REQ)
    socket_rng.connect("tcp://localhost:5558")

    socket_noun = context.socket(zmq.REQ)
    socket_noun.connect("tcp://localhost:5555")

    socket_save = context.socket(zmq.REQ)
    socket_save.connect("tcp://localhost:5556")


    cat = Cat("DefaultName")
    display_welcome()
    adopt_cat(cat)
    while True:
        display_command_screen(cat)
