import json
import requests

header = ""
user_id = ""


def main():
    session = requests.Session()
    login(session)
    while True:
        mode = input("Menu:\n\t[u]ser\n\t[f]riends\n\t[e]vents\n\t[i]nvites\n\t[s]uggestions\n\t[q]uit\n\n> ")
        if mode == "q":
            break
        elif mode == "f":
            friend_mode = input("[l]ist friends, [d]elete friend, [i]nvite friend, [p]ending invitations, [r]espond to invitation\n> ")
            if friend_mode == "l":
                list_friends(session)
            elif friend_mode == "i":
                invite_friend(session)
            elif friend_mode == "p":
                get_friend_invites(session)
            elif friend_mode == "r":
                respond_friend_invite(session)
            elif friend_mode == "d":
                delete_friend(session)
        elif mode == "e":
            event_mode = input("[c]urrent user's events, [o]wned events, [n]ew, [d]elete, [i]nvite user, [r]emove user, [l]eave event, [g]et members, [q]uit event menu: ")
            if event_mode == "n":
                create_event(session)
            elif event_mode == "o":
                owned_events(session)
            elif event_mode == "c":
                get_events(session)
            elif event_mode == "d":
                delete_event(session)
            elif event_mode == "i":
                invite_user_to_event(session)
            elif event_mode == "r":
                remove_user_from_event(session)
            elif event_mode == "g":
                get_event_members(session)
            elif event_mode == "l":
                leave_event(session)
        elif mode == "i":
            invite_mode = input("[p]ending invitations, [r]espond to invitation\n> ")
            if invite_mode == "p":
                get_invitations(session)
            elif invite_mode == "r":
                respond_to_invitation(session)
        elif mode == "u":
            user_mode = input("[n]ew, [d]elete, [f]ind, [s]witch, set [l]ocation, [i]nfo, [q]uit\n> ")
            if user_mode == "n":
                new_user(session)
            elif user_mode == "d":
                delete_user(session)
            elif user_mode == "s":
                login(session)
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
    response = session.post(f"http://localhost:5000/events/{name}", cookies=session.cookies, headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def delete_event(session):
    event_id = input("Event id: ")
    response = session.delete(f"http://localhost:5000/events/{event_id}", cookies=session.cookies, headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def invite_user_to_event(session):
    event_id = input("Event id: ")
    invite_id = input("User id: ")
    response = session.post(f"http://localhost:5000/events/invite/{event_id}:{invite_id}", cookies=session.cookies, headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def get_invitations(session):
    response = session.get(f"http://localhost:5000/events/invite", cookies=session.cookies, headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def respond_to_invitation(session):
    invitation_id = input("Invitation id: ")
    action = "accept" if input("Accept (y/n): ").lower() == "y" else "reject"
    response = session.post(f"http://localhost:5000/events/invite/{invitation_id}/{action}", cookies=session.cookies, headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def list_friends(session):
    response = session.get(f"http://localhost:5000/friends", cookies=session.cookies, headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def invite_friend(session):
    invite_id = input("Friend's user id: ")
    response = session.post(f"http://localhost:5000/friends/{invite_id}", cookies=session.cookies, headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def delete_friend(session):
    friend_id = input("Friend's user id: ")
    response = session.delete(f"http://localhost:5000/friends/{friend_id}", cookies=session.cookies, headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def get_friend_invites(session):
    response = session.get(f"http://localhost:5000/friends/invites", cookies=session.cookies, headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def respond_friend_invite(session):
    invite_id = input("Invitation id: ")
    action = "accept" if input("Accept (y/n): ").lower() == "y" else "reject"
    response = session.post(f"http://localhost:5000/friends/{action}/{invite_id}", cookies=session.cookies, headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def find_user(session):
    email = input("Email: ")
    response = session.get(f"http://localhost:5000/user/{email}", cookies=session.cookies, headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def leave_event(session):
    event_id = input("Event id: ")
    response = session.delete(f"http://localhost:5000/events/user_event/{event_id}:{user_id}", cookies=session.cookies, headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def remove_user_from_event(session):
    event_id = input("Event id: ")
    user_id = input("User id: ")
    response = session.delete(f"http://localhost:5000/events/user_event/{event_id}:{user_id}", cookies=session.cookies, headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def get_event_members(session):
    event_id = input("Event id: ")
    response = session.get(f"http://localhost:5000/events/{event_id}", cookies=session.cookies, headers=header).json()
    print(json.dumps(response, sort_keys=True, indent=4))


def new_user(session):
    email = input("Email: ")
    password = input("Password (careful, plain text): ")
    screen_name = input("Screen name: ")
    phone = input("Phone number: ")
    response = session.post("http://localhost:5000/user", json={"email": email,
                                                                "password": password,
                                                                "screen_name": screen_name,
                                                                "phone": phone}).json()
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
    global user_id
    email = input("Email: ")
    password = input("Password: ")
    response = session.post("http://localhost:5000/user/login", json={"email": email, "password": password}).json()
    if "error" not in response:
        csrf_token = session.cookies['csrf_access_token']
        header = {"X-CSRF-TOKEN": csrf_token}
        user_id = response["data"]["user_id"]
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
