import unittest

from convergence.point import Point


class TestInitPoint(unittest.TestCase):

    def test_init_invalid_coordinates_point(self):
        with self.assertRaises(ValueError):
            point = Point(3.114, 9999999)
        with self.assertRaises(ValueError):
            point = Point(3.11414, -9999999)
        with self.assertRaises(ValueError):
            point = Point(99999999, 11.14)
        with self.assertRaises(ValueError):
            point = Point(-999999, 11.14)
        with self.assertRaises(ValueError):
            point = Point(53.1114, -180.00001)
        with self.assertRaises(ValueError):
            point = Point(53.1114, 180.00001)
        with self.assertRaises(ValueError):
            point = Point(-90.00001, 1.1314)
        with self.assertRaises(ValueError):
            point = Point(90.00001, 1.1314)

    def test_init_invalid_type_points(self):
        with self.assertRaises(TypeError):
            point = Point("Invalid", "Input")
        with self.assertRaises(TypeError):
            point = Point("3.a1155", "3.1114")
        with self.assertRaises(TypeError):
            point = Point(3.1115, None)

    def test_init_valid_points(self):
        point = Point(90, 180)
        point = Point(90, -180)
        point = Point(-90, 180)
        point = Point(-90, -180)
        point = Point("3.111115", "51.333")
        point = Point("-11.1114", "11.2225")
        point = Point("-3.14", 51.1314)


class TestPointMethods(unittest.TestCase):

    def test_str(self):
        point = Point(90, 180)
        self.assertEqual(str(point), "90.000000, 180.000000")
        point = Point(53.1144216, 3.1141537)
        self.assertEqual(str(point), "53.114422, 3.114154")

    def test_eq(self):
        point_a = Point(90, 180)
        point_b = Point("90", "180")
        self.assertEqual(point_a, point_a)
        self.assertEqual(point_a, point_b)
        point_a = Point(3.14441, 13.92145)
        point_b = Point(3.14441, 13.92145)
        self.assertEqual(point_a, point_b)
        point_a = Point(89.99999, 50)
        point_b = Point(90, 50)
        self.assertNotEqual(point_a, point_b)

    def test_distance_to(self):
        point_a = Point(53.434721, -0.244350)  # Stainton le Vale
        point_b = Point(54.761073, -1.564506)  # Durham
        self.assertEqual(point_a.distance_to(point_b), 170759.65855588287)
        self.assertEqual(point_a.distance_to(point_b),
                         point_b.distance_to(point_a))
        self.assertEqual(point_a.distance_to(point_a), 0)

if __name__ == "__main__":
    unittest.main()
