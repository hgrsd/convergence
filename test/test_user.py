import unittest
from unittest.mock import patch

from convergence.core import user
from convergence.utils import exceptions
from test import fakes


class TestUserLogin(unittest.TestCase):

    @patch.object(user, "user_store")
    def test_user_login_success(self, mock_us):
        mock_us.get_user_by_email = fakes.get_fake_user_by_email_pw
        response = user.login("testuser@gmail.com", "fakepassword")
        self.assertEqual(response, 5)

    @patch.object(user, "user_store")
    def test_user_login_fail(self, mock_us):
        mock_us.get_user_by_email = fakes.get_fake_user_by_email_pw

        with self.assertRaises(exceptions.LoginError):
            user.login("testuser@gmail.com", "wrongpassword")

        mock_us.get_user_by_email = lambda _: None
        with self.assertRaises(exceptions.LoginError):
            user.login("testuser@gmail.com", "fakepassword")  # user not found


class TestUserGetInfo(unittest.TestCase):

    @patch.object(user, "user_store")
    def test_user_get_info_success(self, mock_us):
        mock_us.get_user_by_id = fakes.get_fake_user_by_id
        response = user.get_info(5)
        self.assertEqual(response["user_id"], 5)
        self.assertEqual(response["email"], "fakeuser@gmail.com")
        self.assertEqual(response["screen_name"], "Fake User")
        self.assertEqual(response["phone"], "+44(0)1144728913")
        self.assertEqual(response["latitude"], 50.1444)
        self.assertEqual(response["longitude"], 1.25515)

    @patch.object(user, "user_store")
    def test_user_get_info_fail(self, mock_us):
        mock_us.get_user_by_id = lambda _: None
        with self.assertRaises(exceptions.NotFoundError):
            user.get_info(5)


class TestUserRegister(unittest.TestCase):

    @patch.object(user, "user_store")
    def test_user_register_success(self, mock_us):
        response = user.register_user(
            "fakeuser@gmail.com",
            "fakepassword",
            "Fake User",
            "+44(0)1144728913"
        )
        self.assertEqual(response["email"], "fakeuser@gmail.com")
        self.assertEqual(response["screen_name"], "Fake User")
        self.assertEqual(response["phone"], "+44(0)1144728913")
        self.assertEqual(response["latitude"], None)
        self.assertEqual(response["longitude"], None)

    @patch.object(user, "user_store")
    def test_user_register_fail(self, mock_us):
        with self.assertRaises(exceptions.InputError):
            user.register_user(
                "",
                "fakepassword",
                "Fake User",
                "+44(0)1144728913"
            )
        with self.assertRaises(exceptions.InputError):
            user.register_user(
                "invalid@email@address.com",
                "fakepassword",
                "Fake User",
                "+44(0)1144728913"
            )
        with self.assertRaises(exceptions.InputError):
            user.register_user(
                "fakeuser@gmail.com",
                "",
                "Fake User",
                "+44(0)1144728913"
            )
        with self.assertRaises(exceptions.InputError):
            user.register_user(
                "fakeuser@gmail.com",
                "fakepassword",
                "f" * 65,
                "+44(0)1144728913"
            )
        with self.assertRaises(exceptions.InputError):
            user.register_user(
                "fakeuser@gmail.com",
                "fakepassword",
                "",
                "+44(0)1144728913"
            )
        with self.assertRaises(exceptions.InputError):
            user.register_user(
                "fakeuser@gmail.com",
                "fakepassword",
                "",
                "+not_a_phone"
            )


class TestDeleteUser(unittest.TestCase):

    @patch.object(user, "user_store")
    def test_delete_user(self, mock_us):
        mock_us.get_user_by_id = fakes.get_fake_user_by_id
        self.assertEqual(user.delete_user(7), None)

        mock_us.get_user_by_id = lambda _: None
        with self.assertRaises(exceptions.NotFoundError):
            user.delete_user(7)


class TestFindUser(unittest.TestCase):

    @patch.object(user, "user_store")
    def test_find_user(self, mock_us):
        mock_us.get_user_by_email = fakes.get_fake_user_by_email
        response = user.find_user("fakeuser@gmail.com")
        self.assertEqual(response["email"], "fakeuser@gmail.com")
        self.assertEqual(response["screen_name"], "Fake User")
        self.assertEqual(response["user_id"], 5)

        mock_us.get_user_by_email = lambda _: None
        response = user.find_user("fakeuser@gmail.com")
        self.assertEqual(response, [])


class TestUpdateLocation(unittest.TestCase):

    @patch.object(user, "user_store")
    def test_update_location_success(self, mock_us):
        mock_us.get_user_by_id = fakes.get_fake_user_by_id
        response = user.update_location(7, 1.14, 9.1513)
        self.assertEqual(response, (1.14, 9.1513))

    @patch.object(user, "user_store")
    def test_update_location_fail(self, mock_us):
        mock_us.get_user_by_id = fakes.get_fake_user_by_id
        with self.assertRaises(exceptions.LocationError):
            user.update_location(7, -90.0001, 180)
        with self.assertRaises(exceptions.LocationError):
            user.update_location(7, -3.1151, 180.01)
        with self.assertRaises(exceptions.LocationError):
            user.update_location(7, 90.1, 180)
        with self.assertRaises(exceptions.LocationError):
            user.update_location(7, -3.1151, -180.01)

        mock_us.get_user_by_id = lambda _: None
        with self.assertRaises(exceptions.NotFoundError):
            user.update_location(7, 14.1155, 91.4)


if __name__ == "__main__":
    unittest.main()
