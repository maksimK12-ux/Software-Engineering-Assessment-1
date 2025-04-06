import requests
import json
import os
import tkinter as tk
from tkinter import messagebox

# API Base URL
API_URL = "https://pokeapi.co/api/v2/pokemon/"

# Dictionary to store Pokémon
team = {}

compare_vars = {}

def search_pokemon(pokemon_name):
    """Search for a Pokémon in the PokéAPI and return its details."""

    if pokemon_name is None or not str(pokemon_name).isalnum():
        print("The name of the Pokémon must be all letters or numbers")
        return None

    response = requests.get(API_URL + pokemon_name.lower())

    # with open("t.json", "w") as f:
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
# print(search_pokemon('charizard'))
# print(search_pokemon('zarude'))
# print(search_pokemon('pecharunt'))

# add_pokemon_to_team('charizard')
# add_pokemon_to_team('zarude')
# add_pokemon_to_team('metagross')
# add_pokemon_to_team('conkeldurr')
# save_team()

# add_pokemon_to_team(None)
# add_pokemon_to_team('lakosh')

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


def show_help():
    print('show_help')

def exit_app():
    root.destroy()

team_frame = tk.LabelFrame(root, text="Your Pokémon Team", width=1000, height=650)
team_frame.grid(row=0, column=0, padx = 10, pady = 10)
team_frame.grid_propagate(False)

button_frame = tk.Frame(root)
button_frame.grid(row=1, column=0, pady=10)

tk.Button(button_frame, text="Compare", command=compare_stats).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="Help", command=show_help).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Exit", command=exit_app).grid(row=0, column=2, padx=5)


def put_team_into_UI():
    global compare_vars
    for name in team:
        var = tk.BooleanVar()
        chk = tk.Checkbutton(team_frame, text=name, variable=var, anchor='w')
        chk.pack(anchor='w')
        compare_vars[name] = var


def main(): 
    load_team()
    print(json.dumps(team, indent=2))

    put_team_into_UI()

    root.mainloop()

if __name__ == '__main__':
    main()