import requests
import json
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

# API Base URL
API_URL = "https://pokeapi.co/api/v2/pokemon/"

# Dictionary to store Pokémon
team = {}

compare_vars = {}
checkbuttons = {}

def search_pokemon(pokemon_name):
    """Search for a Pokémon in the PokéAPI and return its details."""

    if pokemon_name is None or not str(pokemon_name).isalnum():
        print("The name of the Pokémon must be all letters or numbers")
        return None

    response = requests.get(API_URL + pokemon_name.lower())

    # with open("sample.json", "w") as f:
    #     json.dump(response.json(), f)

    if response.status_code == 200:
        data = response.json()
        return {
            "name": data["name"].capitalize(),
            "id": data["id"],
            "type": [t["type"]["name"] for t in data["types"]],
            "hp": data["stats"][0]["base_stat"],  # HP stat,
            "attack": data["stats"][1]["base_stat"],  # attack stat,
            "defense": data["stats"][2]["base_stat"],  # defense stat,
            "special_attack": data["stats"][3]["base_stat"],  # special-attack stat,
            "special_defense": data["stats"][4]["base_stat"],  # special-defense stat,
            "speed": data["stats"][5]["base_stat"],  # speed stat,

        }
    else:
        print("Pokémon not found.")
        return None

def add_pokemon_to_team(pokemon_name):
    """Add a Pokémon to the team if it exists in the API."""
    pokemon = search_pokemon(pokemon_name)
    if pokemon:
        team[pokemon["name"]] = pokemon
        print(f"{pokemon['name']} added to your team!")
        return True
    else:
        return False

def save_team():
    with open("team.json", "w") as f:
        json.dump(team, f, indent=2)

def load_team():
    if os.path.exists("team.json"):
        print('exists')
        with open("team.json", "r") as f:
            global team
            team = json.load(f)

# print('yes')

# print(search_pokemon('ditto'))
# print(search_pokemon('bulbasaur'))

# add_pokemon_to_team('zarude')
# add_pokemon_to_team('metagross')
# add_pokemon_to_team('conkeldurr')
# save_team()

# load_team()
# print(json.dumps(team, indent=2))


root = tk.Tk()
root.title("Pokedex")


def compare_stats():
    selected = []
    for pokemon_name, tick_flag in compare_vars.items():
        if tick_flag.get(): # Means checkbox is ticked
            selected.append(pokemon_name)

    # print(selected) 

    if len(selected) != 2:
        messagebox.showwarning("Selection Problem", "Please pick exactly two Pokémon")
        return 
    
    p1 = selected[0]
    p2 = selected[1]

    stats_to_compare = ["hp", "attack", "defense", "special_attack", "special_defense", "speed"]
    stat_labels = ["HP", "Attack", "Defense", "Spec Attack", "Spec Defense", "Speed"]

    message = "Comparison: " + p1 + " vs " + p2 + "\n\n"
    message += "Stat: " + p1 + " vs " + p2 + "\n"
    message += "--------------------------\n"

    for i in range(len(stats_to_compare)):
        stat = stats_to_compare[i]
        label = stat_labels[i]
        v1 = team[p1][stat]
        v2 = team[p2][stat]
        line = label + ": " + str(v1) + " vs " + str(v2) + "\n"
        message += line

    messagebox.showinfo("Stat Comparison", message)

def remove_pokemon():
    selected = []
    for pokemon_name, tick_flag in compare_vars.items():
        if tick_flag.get(): # Means checkbox is ticked
            selected.append(pokemon_name)

    # print(selected) 

    if len(selected) != 1:
        messagebox.showwarning("Selection Problem", "Please pick one Pokémon to remove")
        return 

    p1 = selected[0]
    confirm = messagebox.askyesno("Confirm Removal", "Remove " + p1 + " from the team? \n WARNING: You will need relaunch the program to see the updated team.")
    if confirm:
        del team[p1]
        save_team()
        messagebox.showinfo("Removed", "The Pokémon " + p1 + " has been removed from the team successfully.\n WARNING: Exiting...")  
        exit_app()

def add_pokemon():

    if len(team) >= 6:
        messagebox.showinfo("Info", "The team already has 6 Pokémon and is therefore full.")
        return None

    name = simpledialog.askstring("Add Pokémon", "Enter name of the new Pokémon to add \n WARNING: You will need relaunch the program to see the updated team once added.")

    # TODO
    # check if added already :  team

    if name is None or not str(name).isalnum():
        messagebox.showinfo("Info", "The name of the Pokémon must be all letters or numbers")
        return None
    name = name.lower()

    result = add_pokemon_to_team(name)
    if result:
        save_team()
        messagebox.showinfo("Added", "The Pokémon " + name + " has been added to the team successfully.\n WARNING: Exiting...")  
        exit_app()
    else:
        messagebox.showinfo("Info", "The Pokémon " + name + " has NOT been found")     

def show_help():
    help_text = (
        "Pokédex Explorer - Help\n\n"
        "- Add Pokémon:\n"
        "  Click 'Add Pokémon' to enter a name (e.g. pikachu). If found online, it will be added to your team.\n\n"
        "- View Team:\n"
        "  Your current team appears as a list with checkboxes. You can store up to 6 Pokémon.\n\n"
        "- Compare Stats:\n"
        "  Tick exactly two Pokémon, then click 'Compare' to view their stats side by side.\n\n"
        "- Remove Pokémon:\n"
        "  Enter a name in the input field and click 'Remove' to delete it from your team.\n\n"
        "- Save and Load:\n"
        "  Your team is saved automatically. It will load again when you reopen the application.\n\n"
        "- Exit:\n"
        "  Click 'Exit' to close the application.\n\n"
    )
    messagebox.showinfo("Help", help_text)

def exit_app():
    root.destroy()

team_frame = tk.LabelFrame(root, text="Your Pokémon Team", width=1000, height=650)
team_frame.grid(row=0, column=0, padx = 10, pady = 10)
team_frame.grid_propagate(False)

""" For some reason the following did not work -- empty space.. """
# name_frame = tk.Frame(root)
# name_frame.grid(row=1, column=0, padx = 10, pady = 10)
# tk.Label(name_frame, text="Enter name of new Pokemon").grid(row=0, column=0, padx=10)

button_frame = tk.Frame(root)
button_frame.grid(row=1, column=0, pady=10)

tk.Button(button_frame, text="Compare", command=compare_stats).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="Add", command=add_pokemon).grid(row=0, column=1, padx=10)
tk.Button(button_frame, text="Remove", command=remove_pokemon).grid(row=0, column=2, padx=10)
tk.Button(button_frame, text="Help", command=show_help).grid(row=0, column=3, padx=5)
tk.Button(button_frame, text="Exit", command=exit_app).grid(row=0, column=4, padx=5)


def put_team_into_UI():
    global compare_vars
    for name in team:
        var = tk.BooleanVar()
        chk = tk.Checkbutton(team_frame, text=name, variable=var, anchor='w')
        chk.pack(anchor='w')
        compare_vars[name] = var
        checkbuttons[name] = chk


def main(): 
    load_team()
    # print(json.dumps(team, indent=2))

    put_team_into_UI()

    root.mainloop()

if __name__ == '__main__':
    main()