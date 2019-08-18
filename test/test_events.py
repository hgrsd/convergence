import unittest
import datetime
from unittest.mock import patch

from convergence.core import events
from convergence.utils import exceptions
from test import fakes


class TestCreateEvent(unittest.TestCase):

    @patch.object(events, "userevent_store")
    @patch.object(events, "event_store")
    def test_create_event(self, mock_es, mock_ues):
        response = events.create_event(
            7,
            "Fake Event",
            datetime.datetime.utcnow().strftime("%d/%m/%Y %H:%M")
        )
        self.assertEqual(response["event_name"], "Fake Event")
        self.assertEqual(response["event_owner_id"], 7)
        mock_es.add_event.assert_called_once()
        mock_ues.add_userevent.assert_called_once()


class TestDeleteEvent(unittest.TestCase):

    @patch.object(events, "event_store")
    def test_delete_event_success(self, mock_es):
        mock_es.get_event_by_id = fakes.get_fake_event
        self.assertEqual(events.delete_event(3, 7), None)
        mock_es.delete_event.assert_called_once()

    @patch.object(events, "event_store")
    def test_delete_event_fail(self, mock_es):
        mock_es.get_event_by_id = fakes.get_fake_event
        with self.assertRaises(exceptions.NotFoundError):
            events.delete_event(1, 7)
        mock_es.get_event_by_id = lambda _: None
        with self.assertRaises(exceptions.NotFoundError):
            events.delete_event(3, 7)
        mock_es.delete_event.assert_not_called()


class TestAddUserToEvent(unittest.TestCase):

    @patch.object(events, "event_store")
    @patch.object(events, "userevent_store")
    @patch.object(events, "user_store")
    def test_add_user_to_event_success(self, mock_us, mock_ues, mock_es):
        mock_es.get_event_by_id = fakes.get_fake_event
        mock_us.get_user_by_id = fakes.get_fake_user_by_id
        response = events.add_user_to_event(9, 14)
        self.assertEqual(response["user_id"], 9)
        self.assertEqual(response["event_id"], 14)
        mock_ues.add_userevent.assert_called_once()

    @patch.object(events, "event_store")
    @patch.object(events, "userevent_store")
    @patch.object(events, "user_store")
    def test_add_user_to_event_fail(self, mock_us, mock_ues, mock_es):
        mock_es.get_event_by_id = fakes.get_fake_event
        mock_us.get_user_by_id = lambda _: None
        with self.assertRaises(exceptions.NotFoundError):
            events.add_user_to_event(9, 14)
        mock_us.get_user_by_id = fakes.get_fake_user_by_id
        mock_es.get_event_by_id = lambda _: None
        with self.assertRaises(exceptions.NotFoundError):
            events.add_user_to_event(9, 14)
        mock_ues.add_userevent.assert_not_called()


class TestLeaveEvent(unittest.TestCase):

    @patch.object(events, "event_store")
    @patch.object(events, "userevent_store")
    @patch.object(events, "user_store")
    def test_leave_event_success(self, mock_us, mock_ues, mock_es):
        mock_es.get_owner_id = lambda _: 5
        mock_ues.get_userevent = fakes.get_fake_userevent
        response = events.leave_event(3, 17)
        self.assertEqual(response, None)
        mock_ues.delete_userevent.assert_called_once()

    @patch.object(events, "event_store")
    @patch.object(events, "userevent_store")
    @patch.object(events, "user_store")
    def test_leave_event_fail(self, mock_us, mock_ues, mock_es):
        mock_es.get_owner_id = lambda _: 3
        mock_ues.get_userevent = fakes.get_fake_userevent
        with self.assertRaises(exceptions.InvalidRequestError):
            events.leave_event(3, 17)
        mock_ues.get_userevent = lambda *args: None
        with self.assertRaises(exceptions.NotFoundError):
            events.leave_event(3, 17)
        mock_ues.delete_userevent.assert_not_called()


class TestRemoveUserFromEvent(unittest.TestCase):

    @patch.object(events, "userevent_store")
    @patch.object(events, "event_store")
    def test_remove_user_from_event_success(self, mock_es, mock_ues):
        mock_es.get_owner_id = lambda _: 3
        mock_ues.get_userevent = fakes.get_fake_userevent
        self.assertEqual(events.remove_user_from_event(3, 4, 9), None)
        mock_ues.delete_userevent.assert_called_once()

    @patch.object(events, "userevent_store")
    @patch.object(events, "event_store")
    def test_remove_user_from_event_fail(self, mock_es, mock_ues):
        mock_es.get_owner_id = lambda _: 3
        mock_ues.get_userevent = fakes.get_fake_userevent
        with self.assertRaises(exceptions.NotFoundError):
            events.remove_user_from_event(4, 5, 9)
        with self.assertRaises(exceptions.InvalidRequestError):
            events.remove_user_from_event(3, 3, 9)
        mock_ues.get_userevent = lambda *args: None
        with self.assertRaises(exceptions.NotFoundError):
            events.remove_user_from_event(3, 4, 9)
        mock_ues.delete_userevent.assert_not_called()


class TestGetMembers(unittest.TestCase):

    @patch.object(events, "userevent_store")
    def test_get_members_success(self, mock_ues):
        mock_ues.get_userevent = fakes.get_fake_userevent
        mock_ues.get_users_by_event = fakes.get_fake_users_by_event
        response = events.get_members(3, 7)
        self.assertEqual(len(response), 2)
        self.assertEqual(response[0]["user_id"], 1)
        self.assertEqual(response[1]["screen_name"], "Fake User")

        mock_ues.get_users_by_event = lambda *args: []
        response = events.get_members(3, 7)
        self.assertEqual(response, [])

    @patch.object(events, "userevent_store")
    def test_get_members_fail(self, mock_ues):
        mock_ues.get_userevent = lambda *args: None
        with self.assertRaises(exceptions.NotFoundError):
            events.get_members(3, 7)


class TestGetOwnedEvents(unittest.TestCase):

    @patch.object(events, "event_store")
    def test_get_owned_events(self, mock_es):
        mock_es.get_events_by_owner = fakes.get_fake_events_by_owner
        response = events.get_owned_events(3)
        self.assertEqual(len(response), 2)
        self.assertEqual(response[0]["event_name"], "Fake Event")
        self.assertEqual(response[1]["event_name"], "Fake Event Two")

        mock_es.get_events_by_owner = lambda _: None
        self.assertEqual(events.get_owned_events(3), [])


class TestGetEvents(unittest.TestCase):

    @patch.object(events, "userevent_store")
    def test_get_events(self, mock_ues):
        mock_ues.get_events_by_user = fakes.get_fake_events_by_user
        response = events.get_events(3)
        self.assertEqual(len(response), 2)
        self.assertEqual(response[0]["event_name"], "Fake Event")
        self.assertEqual(response[0]["id"], 1)
        self.assertEqual(response[0]["owner_name"], "Fake User")
        self.assertEqual(response[0]["event_owner_id"], 3)
        self.assertEqual(response[1]["event_name"], "Fake Event")
        self.assertEqual(response[1]["id"], 2)
        self.assertEqual(response[1]["owner_name"], "Fake User")

        mock_ues.get_events_by_user = lambda _: None
        self.assertEqual(events.get_events(3), [])


if __name__ == "__main__":
    unittest.main()
