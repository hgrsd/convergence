import unittest
from unittest.mock import patch
from convergence.utils import validators
from convergence.utils import exceptions

fake_json = {
            "email": "random@email.com",
            "screen_name": "random_screenname",
            "phone": "+4407117128246",
            "password": "secure_password1234",
 }


class TestContainsJsonKeys(unittest.TestCase):

    @patch.object(validators, "request")
    def test_contains_json_keys_true(self, mock_object):
        mock_object.json = fake_json

        @validators.contains_json_keys(["email", "screen_name",
                                        "phone", "password"])
        def func():
            return True
        self.assertTrue(func())

    @patch.object(validators, "request")
    def test_contains_json_keys_false(self, mock_object):
        mock_object.json = fake_json

        @validators.contains_json_keys(["email", "screen_name",
                                        "phone", "password",
                                        "date_of_birth"])
        def func():
            return True
        with self.assertRaises(exceptions.InvalidRequestError):
            func()


class TestIsEmailFormat(unittest.TestCase):

    def test_is_email_format_true(self):
        self.assertTrue(validators.is_email_format("test@case.com"))
        self.assertTrue(validators.is_email_format("test@case.co.uk"))
        self.assertTrue(validators.is_email_format("test@case.dev"))
        self.assertTrue(validators.is_email_format("test@case1114.info"))
        self.assertTrue(validators.is_email_format("t_e.st@case.com"))
        self.assertTrue(validators.is_email_format("te.st@case.com"))
        self.assertTrue(validators.is_email_format("test@case.123.co.uk"))
        self.assertTrue(validators.is_email_format("test@case.99.org"))
        self.assertTrue(validators.is_email_format("t1133est@case.com"))

    def test_is_email_format_false(self):
        self.assertFalse(validators.is_email_format(None))
        self.assertFalse(validators.is_email_format(""))
        self.assertFalse(validators.is_email_format(111))
        self.assertFalse(validators.is_email_format("test@case,com"))
        self.assertFalse(validators.is_email_format("test@case@gov.uk"))
        self.assertFalse(validators.is_email_format("test.case.com"))
        self.assertFalse(validators.is_email_format("a" * 254 + "@test.com"))
        self.assertFalse(validators.is_email_format("@gmail.com"))


class TestIsPhoneFormat(unittest.TestCase):

    def test_is_phone_format_true(self):
        self.assertTrue(validators.is_phone_format("1234567"))
        self.assertTrue(validators.is_phone_format("01147833656"))
        self.assertTrue(validators.is_phone_format("+4401147833656"))
        self.assertTrue(validators.is_phone_format("+44(0)1147833656"))
        self.assertTrue(validators.is_phone_format("+44(0)011-47833-656"))

    def test_is_phone_format_false(self):
        self.assertFalse(validators.is_phone_format(1147833656))
        self.assertFalse(validators.is_phone_format("01234"))
        self.assertFalse(validators.is_phone_format("+44(a)14401234"))
        self.assertFalse(validators.is_phone_format("123456"))
        self.assertFalse(validators.is_phone_format(""))
        self.assertFalse(validators.is_phone_format(None))


if __name__ == "__main__":
    unittest.main()
