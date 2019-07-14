import unittest

from convergence import location
from convergence import point


class TestFindCentroid(unittest.TestCase):

    def test_find_centroid_close(self):
        point_a = point.Point(51.449457, -0.149099)  # Balham
        point_b = point.Point(51.399944, 0.016419)  # Bromley
        point_c = point.Point(51.316882, -0.143389)  # Coulsdon
        point_d = point.Point(51.403266, -0.303545)  # Kingston u/t
        coordinates = [point_a, point_b, point_c, point_d]
        self.assertEqual(location.find_centroid(coordinates),
                         point.Point(51.392441720782934, -0.14489879977683245))

    def test_find_centroid_mid(self):
        point_a = point.Point(53.434721, -0.244350)  # Stainton le Vale
        point_b = point.Point(54.761073, -1.564506)  # Durham
        point_c = point.Point(55.608358, -3.007014)  # Scottish Borders
        point_d = point.Point(55.213541, -4.518828)  # South Ayrshire
        coordinates = [point_a, point_b, point_c, point_d]
        self.assertEqual(location.find_centroid(coordinates),
                         point.Point(54.76499345622335, -2.307015824636315))

    def test_find_centroid_far(self):
        point_a = point.Point(49.258071, 4.310359)  # near Reims, FR
        point_b = point.Point(47.176878, 6.130848)  # near Besancon
        point_c = point.Point(45.002795, 5.631141)  # near Grenoble
        point_d = point.Point(43.360261, -0.213497)  # near Pau
        point_e = point.Point(48.049537, -1.970780)  # near Rennes
        coordinates = [point_a, point_b, point_c, point_d, point_e]
        self.assertEqual(location.find_centroid(coordinates),
                         point.Point(46.61597667033897, 2.7632532505451315))

    def test_find_centroid_identical(self):
        point_a = point.Point(49.258071, 4.310359)  # near Reims, FR
        point_b = point.Point(49.258071, 4.310359)  # near Reims, FR
        point_c = point.Point(49.258071, 4.310359)  # near Reims, FR
        point_d = point.Point(49.258071, 4.310359)  # near Reims, FR
        coordinates = [point_a, point_b, point_c, point_d]
        self.assertEqual(location.find_centroid(coordinates),
                         point_a)


class TestMeanDistFromCentroid(unittest.TestCase):

    def test_mean_dist_from_centroid_close(self):
        point_a = point.Point(51.449457, -0.149099)  # Balham
        point_b = point.Point(51.399944, 0.016419)  # Bromley
        point_c = point.Point(51.316882, -0.143389)  # Coulsdon
        point_d = point.Point(51.403266, -0.303545)  # Kingston u/t
        coordinates = [point_a, point_b, point_c, point_d]
        centroid = location.find_centroid(coordinates)
        self.assertEqual(location.mean_dist_from_centroid(coordinates,
                                                          centroid),
                         9260.933838113526)

    def test_mean_dist_from_centroid_mid(self):
        point_a = point.Point(53.434721, -0.244350)  # Stainton le Vale
        point_b = point.Point(54.761073, -1.564506)  # Durham
        point_c = point.Point(55.608358, -3.007014)  # Scottish Borders
        point_d = point.Point(55.213541, -4.518828)  # South Ayrshire
        coordinates = [point_a, point_b, point_c, point_d]
        centroid = location.find_centroid(coordinates)
        self.assertEqual(location.mean_dist_from_centroid(coordinates,
                                                          centroid),
                         125240.97021434733)

    def test_mean_dist_from_centroid_far(self):
        point_a = point.Point(49.258071, 4.310359)  # near Reims, FR
        point_b = point.Point(47.176878, 6.130848)  # near Besancon
        point_c = point.Point(45.002795, 5.631141)  # near Grenoble
        point_d = point.Point(43.360261, -0.213497)  # near Pau
        point_e = point.Point(48.049537, -1.970780)  # near Rennes
        coordinates = [point_a, point_b, point_c, point_d, point_e]
        centroid = location.find_centroid(coordinates)
        self.assertEqual(location.mean_dist_from_centroid(coordinates,
                                                          centroid),
                         337243.52725888294)

    def test_mean_dist_from_centroid_identical(self):
        point_a = point.Point(49.258071, 4.310359)  # near Reims, FR
        point_b = point.Point(49.258071, 4.310359)  # near Reims, FR
        point_c = point.Point(49.258071, 4.310359)  # near Reims, FR
        coordinates = [point_a, point_b, point_c]
        centroid = point.Point(45.002795, 5.631141)  # near Grenoble
        self.assertEqual(location.mean_dist_from_centroid(coordinates,
                                                          centroid),
                         point_a.distance_to(centroid))


if __name__ == "__main__":
    unittest.main()
