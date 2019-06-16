import json
import requests
from requests.auth import HTTPBasicAuth


username = ""
pw = ""

username = input("Username: ")
pw = input("Password: ")

def main():
    mode = input("Mode (g=groups, u=users, l=location, s=suggestions, q=quit: ")
    while mode != "q":
        if mode == "g":
            group_mode = input("[c]reate, [d]elete, [a]dd user, [r]emove user, [g]et members, [q]uit group menu: ")
            if group_mode == "c":
                create_group()
            elif group_mode == "d":
                delete_group()
            elif group_mode == "a":
                add_user_to_group()
            elif group_mode == "r":
                remove_user_from_group()
            elif group_mode == "g":
                get_group_members()
        elif mode == "u":
            user_mode = input("[n]ew user, [d]elete user, [f]ind user, [s]witch user, [a]vailability, user [g]roups, [o]wned groups, [q]uit user menu: ")
            if user_mode == "n":
                new_user()
            elif user_mode == "o":
                owned_groups()
            elif user_mode == "d":
                delete_user()
            elif user_mode == "s":
                switch_user()
            elif user_mode == "a":
                set_availability()
            elif user_mode == "g":
                get_groups()
            elif user_mode == "f":
                find_user()
        elif mode == "l":
            update_location()
        elif mode == "s":
            sug_mode = input("[d]istance, [t]ransit, d[r]iving, [c]ycling, [w]alking, [q]uit suggestions menu: ")
            if sug_mode == "d":
                dist_suggestions()
            elif sug_mode == "t":
                transit_suggestions()
            elif sug_mode == "r":
                driving_suggestions()
            elif sug_mode == "c":
                cycling_suggestions()
            elif sug_mode == "w":
                walking_suggestions()
        mode = input("Mode (g=groups, u=users, l=location, s=suggestions, q=quit: ")

def create_group():
    name = input("Group name: ")
    response = requests.post(f"http://localhost:5000/groups/{name}", auth=(username, pw))
    print(json.dumps(response.json(), sort_keys=True, indent=4))

def delete_group():
    group_id = input("Group id: ")
    response = requests.delete(f"http://localhost:5000/groups/{group_id}", auth=(username, pw))
    print(json.dumps(response.json(), sort_keys=True, indent=4))

def add_user_to_group():
    group_id = input("Group id: ")
    user_id = input("User id: ")
    response = requests.post(f"http://localhost:5000/groups/user_group/{group_id}:{user_id}", auth=(username, pw))
    print(json.dumps(response.json(), sort_keys=True, indent=4))

def find_user():
    user = input("Username: ")
    response = requests.get(f"http://localhost:5000/user/{user}", auth=(username, pw))
    print(json.dumps(response.json(), sort_keys=True, indent=4))

def remove_user_from_group():
    group_id = input("Group id: ")
    user_id = input("User id: ")
    response = requests.delete(f"http://localhost:5000/groups/user_group/{group_id}:{user_id}", auth=(username, pw))
    print(json.dumps(response.json(), sort_keys=True, indent=4))

def get_group_members():
    group_id = input("Group id: ")
    available = int(input("Available members only? 0=No, 1=Yes: "))
    response = requests.get(f"http://localhost:5000/groups/{group_id}:{available}", auth=(username, pw))
    print(json.dumps(response.json(), sort_keys=True, indent=4))

def new_user():
    name = input("Username: ")
    passw = input("Password (careful, plain text): ")
    response = requests.post(f"http://localhost:5000/user/{name}:{passw}")
    print(json.dumps(response.json(), sort_keys=True, indent=4))

def delete_user():
    response = requests.delete(f"http://localhost:5000/user", auth=(username, pw))
    print(json.dumps(response.json(), sort_keys=True, indent=4))

def owned_groups():
    response = requests.get("http://localhost:5000/groups/owned", auth=(username, pw))
    print(json.dumps(response.json(), sort_keys=True, indent=4))

def get_groups():
    response = requests.get("http://localhost:5000/groups", auth=(username, pw))
    print(json.dumps(response.json(), sort_keys=True, indent=4))

def switch_user():
    username = input("Username: ")
    pw = input("Password: ")

def set_availability():
    availability = input("Set availability, 0=unavailable, 1=available: ")
    response = requests.put(f"http://localhost:5000/user/availability/{availability}", auth=(username, pw))
    print(json.dumps(response.json(), sort_keys=True, indent=4))

def update_location():
    lat = input("New latitude: ")
    long = input("New longitude: ")
    response = requests.put(f"http://localhost:5000/loc/{lat}:{long}", auth=(username, pw))
    print(json.dumps(response.json(), sort_keys=True, indent=4))

def dist_suggestions():
    group = input("Group id: ")
    sug_type = input("Type: ")
    response = requests.get(f"http://localhost:5000/suggestions/distance/{group}:{sug_type}", auth=(username, pw))
    print(json.dumps(response.json(), sort_keys=True, indent=4))

def transit_suggestions():
    group = input("Group id: ")
    sug_type = input("Type: ")
    response = requests.get(f"http://localhost:5000/suggestions/transit/{group}:{sug_type}", auth=(username, pw))
    print(json.dumps(response.json(), sort_keys=True, indent=4))
   
def driving_suggestions():
    group = input("Group id: ")
    sug_type = input("Type: ")
    response = requests.get(f"http://localhost:5000/suggestions/driving/{group}:{sug_type}", auth=(username, pw))
    print(json.dumps(response.json(), sort_keys=True, indent=4))

def cycling_suggestions():
    group = input("Group id: ")
    sug_type = input("Type: ")
    response = requests.get(f"http://localhost:5000/suggestions/cycling/{group}:{sug_type}", auth=(username, pw))
    print(json.dumps(response.json(), sort_keys=True, indent=4))

def walking_suggestions():
    group = input("Group id: ")
    sug_type = input("Type: ")
    response = requests.get(f"http://localhost:5000/suggestions/walking/{group}:{sug_type}", auth=(username, pw))
    print(json.dumps(response.json(), sort_keys=True, indent=4))

if __name__ == "__main__":
    main()

