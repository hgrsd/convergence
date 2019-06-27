import json
import requests

header = ""


def main():
    login()
    while True:
        mode = input("Menu:\n\t[u]ser\n\t[e]vents\n\t[s]uggestions\n\t[q]uit\n\n> ")
        if mode == "q":
            break
        elif mode == "e":
            event_mode = input("[c]urrent user's events, [o]wned events, [n]ew, [d]elete, [a]dd user, [r]emove user, [g]et members, [q]uit event menu: ")
            if event_mode == "n":
                create_event()
            elif event_mode == "o":
                owned_events()
            elif event_mode == "c":
                get_events()
            elif event_mode == "d":
                delete_event()
            elif event_mode == "a":
                add_user_to_event()
            elif event_mode == "r":
                remove_user_from_event()
            elif event_mode == "g":
                get_event_members()
        elif mode == "u":
            user_mode = input("[n]ew, [d]elete, [f]ind, [s]witch, [a]vailability, set [l]ocation, [i]nfo, [q]uit\n> ")
            if user_mode == "n":
                new_user()
            elif user_mode == "d":
                delete_user()
            elif user_mode == "s":
                login()
            elif user_mode == "a":
                set_availability()
            elif user_mode == "f":
                find_user()
            elif user_mode == "l":
                update_location()
            elif user_mode == "i":
                get_info()
        elif mode == "s":
            sug_mode = input("[d]istance, [t]ransit, d[r]iving, [c]ycling, [w]alking, [q]uit\n> ")
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


def create_event():
    name = input("Event name: ")
    response = requests.post(f"http://localhost:5000/events/{name}", headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def delete_event():
    event_id = input("Event id: ")
    response = requests.delete(f"http://localhost:5000/events/{event_id}", headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def add_user_to_event():
    event_id = input("Event id: ")
    user_id = input("User id: ")
    response = requests.post(f"http://localhost:5000/events/user_event/{event_id}:{user_id}", headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def find_user():
    user = input("Username: ")
    response = requests.get(f"http://localhost:5000/user/{user}", headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def remove_user_from_event():
    event_id = input("Event id: ")
    user_id = input("User id: ")
    response = requests.delete(f"http://localhost:5000/events/user_event/{event_id}:{user_id}", headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def get_event_members():
    event_id = input("Event id: ")
    available = int(input("Available members only? 0=No, 1=Yes: "))
    response = requests.get(f"http://localhost:5000/events/{event_id}:{available}", headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def new_user():
    username = input("Username: ")
    password = input("Password (careful, plain text): ")
    response = requests.post("http://localhost:5000/user", json={"username": username, "password": password}).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def delete_user():
    response = requests.delete(f"http://localhost:5000/user", headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def get_info():
    response = requests.get(f"http://localhost:5000/user", headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def owned_events():
    response = requests.get("http://localhost:5000/events/owned", headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def get_events():
    response = requests.get("http://localhost:5000/events", headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def login():
    username = input("Username: ")
    password = input("Password: ")
    global header
    response = requests.post("http://localhost:5000/user/login", json={"username": username, "password": password}).json()
    if "access_token" in response:
        access_token = response["access_token"]
        header = {"Authorization": f"Bearer {access_token}"}
    print(json.dumps(response, sort_keys=True, indent=4))


def set_availability():
    availability = input("Set availability, 0=unavailable, 1=available: ")
    response = requests.put(f"http://localhost:5000/user/availability/{availability}", headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def update_location():
    lat = input("New latitude: ")
    long = input("New longitude: ")
    response = requests.put(f"http://localhost:5000/loc/{lat}:{long}", headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def dist_suggestions():
    event = input("Event id: ")
    sug_type = input("Type: ")
    response = requests.get(f"http://localhost:5000/suggestions/distance/{event}:{sug_type}", headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def transit_suggestions():
    event = input("Event id: ")
    sug_type = input("Type: ")
    response = requests.get(f"http://localhost:5000/suggestions/transit/{event}:{sug_type}", headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def driving_suggestions():
    event = input("Event id: ")
    sug_type = input("Type: ")
    response = requests.get(f"http://localhost:5000/suggestions/drive/{event}:{sug_type}", headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def cycling_suggestions():
    event = input("Event id: ")
    sug_type = input("Type: ")
    response = requests.get(f"http://localhost:5000/suggestions/cycle/{event}:{sug_type}", headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def walking_suggestions():
    event = input("Event id: ")
    sug_type = input("Type: ")
    response = requests.get(f"http://localhost:5000/suggestions/walk/{event}:{sug_type}", headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


if __name__ == "__main__":
    main()
