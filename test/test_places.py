import unittest
import datetime

from convergence.core import places
from convergence.data.models import Place, User
from convergence.utils.point import Point

fake_users = [
    User(
        id=1,
        email="fakeuser@gmail.com",
        screen_name="Fake User",
        phone="+44(0)1144728913",
        latitude=50.1444,
        longitude=1.25515
    ),
    User(
        id=2,
        email="fakeuser@gmail.com",
        screen_name="Fake User",
        phone="+44(0)1144728913",
        latitude=51.1444,
        longitude=0.25515
    ),
]

fake_places = [
    Place(
        id=1,
        gm_id="fake_gm_id",
        name="Place A",
        lat=51.423096,
        long=-0.056820,
        gm_price=2,
        gm_rating=3.5,
        gm_types=["bar", "restaurant"],
        address="Fake Address A",
        timestamp=datetime.datetime.utcnow()
    ),
    Place(
        id=2,
        gm_id="fake_gm_id",
        name="Place B",
        lat=51.506007,
        long=-0.252850,
        gm_price=2,
        gm_rating=4.5,
        gm_types=["bar", "restaurant"],
        address="Fake Address B",
        timestamp=datetime.datetime.utcnow()
    ),
    Place(
        id=3,
        gm_id="fake_gm_id",
        name="Place C",
        lat=51.606007,
        long=0.15530,
        gm_price=2,
        gm_rating=2,
        gm_types=["bar", "restaurant", "cafe"],
        address="Fake Address C",
        timestamp=datetime.datetime.utcnow()
    ),
    Place(
        id=4,
        gm_id="fake_gm_id",
        name="Place D",
        lat=51.628366,
        long=-0.175970,
        gm_price=2,
        gm_rating=5,
        gm_types=["bar", "restaurant", "cafe"],
        address="Fake Address D",
        timestamp=datetime.datetime.utcnow()
    )
]


class TestSortPlacesByRating(unittest.TestCase):

    def test_sort_places_by_rating(self):
        places_sorted = places.sort_places_by_rating(
            [fake_place.as_dict() for fake_place in fake_places]
        )
        self.assertEqual(places_sorted[0]["id"], 4)
        self.assertEqual(places_sorted[1]["id"], 2)
        self.assertEqual(places_sorted[2]["id"], 1)
        self.assertEqual(places_sorted[3]["id"], 3)


class TestSortPlacesByTravelTotal(unittest.TestCase):

    def test_sort_places_by_travel_total(self):
        places_sorted = [place.as_dict() for place in fake_places]
        places_sorted[0]["travel_total"] = 1149
        places_sorted[1]["travel_total"] = 577
        places_sorted[2]["travel_total"] = 9114
        places_sorted[3]["travel_total"] = 791
        places_sorted = places.sort_places_by_travel_total(places_sorted)
        self.assertEqual(places_sorted[0]["travel_total"], 577)
        self.assertEqual(places_sorted[1]["travel_total"], 791)
        self.assertEqual(places_sorted[2]["travel_total"], 1149)
        self.assertEqual(places_sorted[3]["travel_total"], 9114)


class TestGetDistanceForPlaces(unittest.TestCase):

    def test_get_distance_for_places(self):
        user_coordinates = [Point(*user.get_location())
                            for user in fake_users]
        places_dicts = [place.as_dict() for place in fake_places]
        response = places.get_distance_for_places(
            user_coordinates,
            places_dicts
        )
        self.assertEqual(response[0]["travel_total"], 207304.52645943288)
        self.assertEqual(response[1]["travel_total"], 238273.00225216942)
        self.assertEqual(response[2]["travel_total"], 231703.34971067737)
        self.assertEqual(response[3]["travel_total"], 254710.84480953924)


if __name__ == "__main__":
    unittest.main()
