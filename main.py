import sys
import os

class Cat:
    def __init__(self, name):
        self.name = name
        self.hunger = 10
        self.happiness = 10
        self.max_happiness = 10
        self.energy = 5
        self.max_energy = 10
        self.kibble = 10

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
        
def display_status(cat):
    clear_screen()
    print(f"Name = {cat.name}")
    print(f"Hunger = {cat.hunger}")
    print(f"Happiness = {cat.happiness}")
    print(f"Energy = {cat.energy}")
    print(f"Kibble = {cat.kibble}")
    input(f"\nPress Enter to Continue...")

def feed_cat(cat):
    clear_screen()
    if cat.kibble > 0:
        cat.kibble -= 1
        cat.hunger -= 1
        print("You feed your cat some kibble. Yum!")
        print(f"Kibble Stock: {cat.kibble} left")
        print(f"Hunger: {cat.hunger}")
        input("Press enter to continue... ")
    else:
        print("You don't have any kibble to feed your cat")
        input("Press enter to continue... ")

if __name__ == "__main__":
    cat = Cat("Default")
    display_welcome()
    adopt_cat(cat)
    while True:
        display_command_screen(cat)
