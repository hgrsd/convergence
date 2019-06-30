""" -- seed.py

Seeds database for testing purposes using Faker library to generate data.

Use: seed.py <db_name> <seed>

An empty PostgreSQL database with name <db_name> should be created prior to running this script.
Number of records, country codes to be used, and user password can be specified.

The script sets an env var SQLALCHEMY_DATABASE_URI which will be detected by the convergence app,
in order to ensure the right app_context.

Make sure to set SQLALCHEMY_DATABASE_URI to the location of the generated testing db when running
the app to make use of the data generated by this script.
"""

import os
import sys
import faker
import random
from convergence.convergence_db import ConvergenceDB
from convergence.models import *


def generate_users(n_users=100, password="testing", country_code="GB"):
    print(f"[>] Generating {n_users} fake users, using country code {country_code}...")
    for i in range(n_users):
        user = User()
        user.username = fake.user_name()
        user.hash_password(password)
        user.available = random.choice([False, True])
        user.last_seen_lat, user.last_seen_long = fake.local_latlng(country_code=country_code, coords_only=True)
        db.session.add(user)
    db.session.flush()


def generate_places(n_places=2500, country_code="GB"):
    print(f"[>] Generating {n_places} fake places, using country code {country_code}...")
    for _ in range(2500):
        place = Place()
        place.gm_id = fake.md5(raw_output=False)
        place.name = fake.company()
        place.lat, place.long = fake.local_latlng(country_code=country_code, coords_only=True)
        place.gm_price = random.randint(1, 5)
        place.gm_rating = random.randint(1, 5)
        place.gm_types = [random.choice(["bar", "cafe", "restaurant", "art_gallery", "museum", "night_club", "movie_theater"]) for _ in range(2)]
        place.address = fake.address().replace("\n", ", ")
        place.timestamp = fake.date_time()
        db.session.add(place)
    db.session.flush()


def generate_events(n_events=25, total_users=100):
    print(f"[>] Generating {n_events} fake events...")
    for i in range(n_events):
        event = Event()
        event.name = fake.domain_word()
        event.owner = random.choice(db.session.query(User).all()).id
        event.creation_date = fake.date_time()
        db.session.add(event)
        db.session.flush()
        # add owner of event to UserEvent
        userevent = UserEvent()
        userevent.event_id = event.id
        userevent.user_id = event.owner
        db.session.add(userevent)
        db.session.flush()


def generate_userevents(n_per_user=2, total_users=100, total_events=25):
    print(f"[>] Generating UserEvents, {n_per_user} events per user for a total of {total_users} users...")
    for user in db.session.query(User).all():
        for k in range(n_per_user):
            userevent = UserEvent()
            userevent.user_id = user.id
            userevent.event_id = random.choice(db.session.query(Event).all()).id
            # check if UserEvent already exists
            if db.session.query(UserEvent).filter_by(user_id=user.id, event_id=userevent.event_id).first():
                continue
            db.session.add(userevent)
        db.session.flush()


# -- run the script:


if not len(sys.argv) == 3:
    print(f"Use: {sys.argv[0]} <db_name> <seed>")
    sys.exit(1)
else:
    db_name = sys.argv[1]
    seed = int(sys.argv[2])
if input(f"About to seed database {db_name}. DO NOT use on production database. Continue? (y/n): ") != "y":
    sys.exit(0)

random.seed(seed)
fake = faker.Faker("en-GB")
fake.seed(seed)
db_address = f"postgresql://localhost/{db_name}"
print("[o] Initialising database...")
db = ConvergenceDB(db_address)
db.create_tables()
print("[+] Initial database setup complete.\n")

# Use the following testing data generation parameters:
generate_users(n_users=100, password="testing", country_code="GB")
generate_places(n_places=2500, country_code="GB")
generate_events(n_events=25)
generate_userevents(n_per_user=2, total_users=100)

print("[+] Generation complete.")
print("[o] Committing to database.")
try:
    db.session.commit()
    print("[+] Database write completed. Script finished.")
    print(f"\tSeed used: {seed}. Please note for reproducibility.")
except:
    print("[-] Error writing to database.")
    sys.exit(1)
else:
    sys.exit(0)
