import json
import requests

header = ""


def main():
    session = requests.Session()
    login(session)
    while True:
        mode = input("Menu:\n\t[u]ser\n\t[e]vents\n\t[s]uggestions\n\t[q]uit\n\n> ")
        if mode == "q":
            break
        elif mode == "e":
            event_mode = input("[c]urrent user's events, [o]wned events, [n]ew, [d]elete, [a]dd user, [r]emove user, [g]et members, [q]uit event menu: ")
            if event_mode == "n":
                create_event(session)
            elif event_mode == "o":
                owned_events(session)
            elif event_mode == "c":
                get_events(session)
            elif event_mode == "d":
                delete_event(session)
            elif event_mode == "a":
                add_user_to_event(session)
            elif event_mode == "r":
                remove_user_from_event(session)
            elif event_mode == "g":
                get_event_members(session)
        elif mode == "u":
            user_mode = input("[n]ew, [d]elete, [f]ind, [s]witch, [a]vailability, set [l]ocation, [i]nfo, [q]uit\n> ")
            if user_mode == "n":
                new_user(session)
            elif user_mode == "d":
                delete_user(session)
            elif user_mode == "s":
                login(session)
            elif user_mode == "a":
                set_availability(session)
            elif user_mode == "f":
                find_user(session)
            elif user_mode == "l":
                update_location(session)
            elif user_mode == "i":
                get_info(session)
        elif mode == "s":
            sug_mode = input("[d]istance, [t]ransit, d[r]iving, [c]ycling, [w]alking, [q]uit\n> ")
            if sug_mode == "d":
                dist_suggestions(session)
            elif sug_mode == "t":
                transit_suggestions(session)
            elif sug_mode == "r":
                driving_suggestions(session)
            elif sug_mode == "c":
                cycling_suggestions(session)
            elif sug_mode == "w":
                walking_suggestions(session)


def create_event(session):
    name = input("Event name: ")
    print(session.cookies)
    response = session.post(f"http://localhost:5000/events/{name}", cookies=session.cookies, headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def delete_event(session):
    event_id = input("Event id: ")
    response = session.delete(f"http://localhost:5000/events/{event_id}", cookies=session.cookies, headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def add_user_to_event(session):
    event_id = input("Event id: ")
    user_id = input("User id: ")
    response = session.post(f"http://localhost:5000/events/user_event/{event_id}:{user_id}", cookies=session.cookies, headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def find_user(session):
    user = input("Username: ")
    response = session.get(f"http://localhost:5000/user/{user}", cookies=session.cookies, headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def remove_user_from_event(session):
    event_id = input("Event id: ")
    user_id = input("User id: ")
    response = session.delete(f"http://localhost:5000/events/user_event/{event_id}:{user_id}", cookies=session.cookies, headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def get_event_members(session):
    event_id = input("Event id: ")
    available = int(input("Available members only? 0=No, 1=Yes: "))
    response = session.get(f"http://localhost:5000/events/{event_id}:{available}", cookies=session.cookies, headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def new_user(session):
    username = input("Username: ")
    password = input("Password (careful, plain text): ")
    response = session.post("http://localhost:5000/user", json={"username": username, "password": password}).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def delete_user(session):
    response = session.delete(f"http://localhost:5000/user", cookies=session.cookies, headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def get_info(session):
    response = session.get(f"http://localhost:5000/user", cookies=session.cookies, headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def owned_events(session):
    response = session.get("http://localhost:5000/events/owned", cookies=session.cookies, headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def get_events(session):
    response = session.get("http://localhost:5000/events", cookies=session.cookies, headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def login(session):
    global header
    username = input("Username: ")
    password = input("Password: ")
    response = session.post("http://localhost:5000/user/login", json={"username": username, "password": password}).json()
    if "error" not in response:
        csrf_token = session.cookies['csrf_access_token']
        header = {"X-CSRF-TOKEN": csrf_token}
    print(json.dumps(response, sort_keys=True, indent=4))


def set_availability(session):
    availability = input("Set availability, 0=unavailable, 1=available: ")
    response = session.put(f"http://localhost:5000/user/availability/{availability}", cookies=session.cookies, headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def update_location(session):
    lat = input("New latitude: ")
    long = input("New longitude: ")
    response = session.put(f"http://localhost:5000/user/location/{lat}:{long}", cookies=session.cookies, headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def dist_suggestions(session):
    event = input("Event id: ")
    sug_type = input("Type: ")
    response = session.get(f"http://localhost:5000/suggestions/distance/{event}:{sug_type}", cookies=session.cookies, headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def transit_suggestions(session):
    event = input("Event id: ")
    sug_type = input("Type: ")
    response = session.get(f"http://localhost:5000/suggestions/transit/{event}:{sug_type}", cookies=session.cookies, headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def driving_suggestions(session):
    event = input("Event id: ")
    sug_type = input("Type: ")
    response = session.get(f"http://localhost:5000/suggestions/drive/{event}:{sug_type}", cookies=session.cookies, headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def cycling_suggestions(session):
    event = input("Event id: ")
    sug_type = input("Type: ")
    response = session.get(f"http://localhost:5000/suggestions/cycle/{event}:{sug_type}", cookies=session.cookies, headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def walking_suggestions(session):
    event = input("Event id: ")
    sug_type = input("Type: ")
    response = session.get(f"http://localhost:5000/suggestions/walk/{event}:{sug_type}", cookies=session.cookies, headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


if __name__ == "__main__":
    main()
