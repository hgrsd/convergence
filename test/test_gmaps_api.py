import unittest

from convergence.apis import google_maps

valid_json = {
    "results": [
        {
            "geometry": {
                "location": {
                    "lat": 51.114,
                    "lng": 1.1236
                }
            },
            "name": "Fake Place",
            "types": ["bar", "restaurant"],
            "vicinity": "A fake address, 19141AB",
            "place_id": "fake_place_id",
            "price_level": 2.5,
            "rating": 3
        },
        {
            "geometry": {
                "location": {
                    "lat": 51.114,
                    "lng": 1.1236
                }
            },
            "name": "Fake Place 2",
            "types": ["bar"],
            "vicinity": "A fake address, 19141AB",
            "place_id": "fake_place_id",
        }
    ]
}

invalid_json = {
    "results": [
        {
            "geometry": {
                "location": {
                    "lat": 51.114,
                    "lng": 1.1236
                }
            },
            "name": "Fake Place",
            "types": ["bar", "restaurant"],
            "vicinity": "A fake address, 19141AB",
            "place_id": "fake_place_id",
            "price_level": 2.5,
            "rating": 3
        },
        {
            "geometry": {
                "location": {  # missing long
                    "lat": 51.114,
                }
            },
            "types": ["bar"],
            "vicinity": "A fake address, 19141AB",
            "place_id": "fake_place_id",  # missing name
        }
    ]
}


class TestJsonExtractPlaces(unittest.TestCase):

    def test_json_extract_places_valid(self):
        places = google_maps._json_extract_places(valid_json)
        self.assertEqual(len(places), 2)
        self.assertEqual(places[0]["name"], "Fake Place")
        self.assertEqual(places[0]["lat"], 51.114)
        self.assertEqual(places[0]["long"], 1.1236)
        self.assertEqual(places[0]["price_level"], 2.5)
        self.assertEqual(places[0]["types"], ["bar", "restaurant"])
        self.assertEqual(places[0]["gm_rating"], 3)
        self.assertEqual(places[1]["name"], "Fake Place 2")
        self.assertEqual(places[1]["lat"], 51.114)
        self.assertEqual(places[1]["long"], 1.1236)
        self.assertEqual(places[1]["price_level"], None)
        self.assertEqual(places[1]["gm_rating"], None)
        self.assertEqual(places[1]["types"], ["bar"])

    def test_json_extract_places_invalid(self):
        places = google_maps._json_extract_places(invalid_json)
        self.assertEqual(len(places), 1)
        self.assertEqual(places[0]["name"], "Fake Place")
        self.assertEqual(places[0]["lat"], 51.114)
        self.assertEqual(places[0]["long"], 1.1236)
        self.assertEqual(places[0]["price_level"], 2.5)
        self.assertEqual(places[0]["types"], ["bar", "restaurant"])
        self.assertEqual(places[0]["gm_rating"], 3)


if __name__ == "__main__":
    unittest.main()
