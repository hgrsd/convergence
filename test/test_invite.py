import unittest
from unittest.mock import patch

from convergence.core import invites
from convergence.utils import exceptions
from test import fakes


class TestInviteUser(unittest.TestCase):

    @patch.object(invites, "userevent_store")
    @patch.object(invites, "userinvite_store")
    @patch.object(invites, "user_store")
    @patch.object(invites, "event_store")
    def test_invite_user_to_event_success(self, mock_es, mock_us, mock_uis,
                                          mock_ues):
        mock_es.get_event_by_id = fakes.get_fake_event
        mock_us.get_user_by_id = fakes.get_fake_user_by_id
        mock_ues.get_userevent = lambda *args: None
        mock_uis.get_invite_by_details = lambda *args: None

        userinvite = invites.invite_user_to_event(3, 5, 1)
        self.assertEqual(userinvite["inviter_id"], 3)
        self.assertEqual(userinvite["invitee_id"], 5)
        self.assertEqual(userinvite["event_id"], 1)

        userinvite = invites.invite_user_to_event(3, 9, 4)
        self.assertEqual(userinvite["inviter_id"], 3)
        self.assertEqual(userinvite["invitee_id"], 9)
        self.assertEqual(userinvite["event_id"], 4)

    @patch.object(invites, "userevent_store")
    @patch.object(invites, "userinvite_store")
    @patch.object(invites, "user_store")
    @patch.object(invites, "event_store")
    def test_invite_user_to_event_fail(self, mock_es, mock_us, mock_uis,
                                       mock_ues):
        mock_es.get_event_by_id = fakes.get_fake_event
        mock_us.get_user_by_id = fakes.get_fake_user_by_id

        with self.assertRaises(exceptions.InvalidRequestError):
            invites.invite_user_to_event(1, 1, 5)  # cannot invite self
        with self.assertRaises(exceptions.NotFoundError):
            invites.invite_user_to_event(1, 7, 1)  # not event owner

        mock_es.get_event_by_id = lambda _: None
        with self.assertRaises(exceptions.NotFoundError):
            invites.invite_user_to_event(1, 3, 5)  # event not found

        mock_es.get_event_by_id = fakes.get_fake_event
        mock_us.get_user_by_id = lambda _: None
        with self.assertRaises(exceptions.NotFoundError):
            invites.invite_user_to_event(1, 7, 3)  # user not found

        mock_us.get_user_by_id = fakes.get_fake_user_by_id
        mock_es.get_event_by_id = fakes.get_fake_event
        mock_ues.get_userevent = lambda *args: True
        mock_uis.get_invite_by_id = lambda *args: None

        with self.assertRaises(exceptions.InvalidRequestError):
            invites.invite_user_to_event(3, 9, 4)  # User already event member

        mock_ues.get_userevent = lambda *args: None
        mock_uis.get_invite_by_id = lambda *args: True
        with self.assertRaises(exceptions.InvalidRequestError):
            invites.invite_user_to_event(3, 9, 4)  # invite already pending


class TestInviteUsers(unittest.TestCase):

    @patch.object(invites, "userevent_store")
    @patch.object(invites, "userinvite_store")
    @patch.object(invites, "user_store")
    @patch.object(invites, "event_store")
    def test_invite_users_to_event_success(self, mock_es, mock_us, mock_uis,
                                           mock_ues):
        mock_es.get_event_by_id = fakes.get_fake_event
        mock_us.get_users_by_emails = fakes.get_fake_users_by_emails
        mock_ues.get_users_by_event = lambda *args: None
        mock_uis.get_users_by_event = lambda *args: None

        emails = [
            "testuser1@gmail.com",
            "testuser2@gmail.com",
            "testuser3@gmail.com"
        ]
        response = invites.invite_users_to_event(3, emails, 1)
        self.assertEqual(response, set())
        mock_uis.add_userinvites.assert_called_once()

    @patch.object(invites, "userevent_store")
    @patch.object(invites, "userinvite_store")
    @patch.object(invites, "user_store")
    @patch.object(invites, "event_store")
    def test_invite_users_to_event_fail(self, mock_es, mock_us, mock_uis,
                                        mock_ues):
        mock_es.get_event_by_id = fakes.get_fake_event
        mock_us.get_users_by_emails = fakes.get_fake_users_by_emails
        mock_ues.get_users_by_event = lambda *args: None
        mock_uis.get_users_by_event = lambda *args: None

        emails = [
            "testuser1@gmail.com",
            "testuser2@gmail.com",
            "testuser3@gmail.com"
        ]
        with self.assertRaises(exceptions.NotFoundError):
            invites.invite_users_to_event(2, emails, 1)
        mock_uis.add_userinvites.assert_not_called()

        emails = ["testuser@gmail.com"] * (invites.MAX_INVITES_PER_REQUEST + 1)
        with self.assertRaises(exceptions.InvalidRequestError):
            invites.invite_users_to_event(3, emails, 1)


class TestGetInvitations(unittest.TestCase):

    @patch.object(invites, "userinvite_store")
    def test_get_invites(self, mock_uis):
        mock_uis.get_invites_by_user = fakes.get_fake_userinvites
        ret_invites = invites.get_invites(3)
        self.assertEqual(ret_invites[0]["id"], 19)
        self.assertEqual(ret_invites[0]["event_name"], "Fake Event")
        self.assertEqual(ret_invites[0]["event_owner_id"], 3)
        self.assertEqual(ret_invites[0]["owner_name"], "Fake Owner")
        self.assertEqual(ret_invites[0]["invite_id"], 1)
        self.assertEqual(ret_invites[0]["inviter_name"], "Fake Owner")
        self.assertEqual(ret_invites[1]["id"], 21)
        self.assertEqual(ret_invites[1]["event_name"], "Another Fake Event")
        self.assertEqual(ret_invites[1]["event_owner_id"], 6)
        self.assertEqual(ret_invites[1]["owner_name"], "Another Fake")
        self.assertEqual(ret_invites[1]["invite_id"], 2)
        self.assertEqual(ret_invites[1]["inviter_name"], "Not The Owner")

        mock_uis.get_invites_by_user = lambda _: None
        self.assertEqual(invites.get_invites(3), [])


class TestRespondToInvitation(unittest.TestCase):

    @patch.object(invites, "userevent_store")
    @patch.object(invites, "event_store")
    @patch.object(invites, "events")
    @patch.object(invites, "userinvite_store")
    def test_respond_accept(self, mock_uis, mock_e, mock_es, mock_ues):
        mock_uis.get_invite_by_id = fakes.get_fake_userinvite
        mock_es.get_event_by_id = fakes.get_fake_event
        mock_e.add_user_to_event_from_invite = fakes.get_fake_userevent_from_invite
        event_response = invites.respond_to_invite(7, 2, True)

        self.assertEqual(event_response.user_id, 7)
        self.assertEqual(event_response.event_id, 6)

    @patch.object(invites, "event_store")
    @patch.object(invites, "events")
    @patch.object(invites, "userinvite_store")
    def test_respond_reject(self, mock_uis, mock_events, mock_es):
        mock_uis.get_invite_by_id = fakes.get_fake_userinvite
        mock_es.get_event_by_id = fakes.get_fake_event
        response = invites.respond_to_invite(7, 2, False)
        self.assertEqual(response, None)

    @patch.object(invites, "event_store")
    @patch.object(invites, "events")
    @patch.object(invites, "userinvite_store")
    def test_respond_fail(self, mock_uis, mock_events, mock_es):
        mock_uis.get_invite_by_id = fakes.get_fake_userinvite
        mock_es.get_event_by_id = fakes.get_fake_event

        with self.assertRaises(exceptions.NotFoundError):
            invites.respond_to_invite(1, 2, False)  # not this user's

        mock_uis.get_invite_by_id = lambda _: None
        with self.assertRaises(exceptions.NotFoundError):
            invites.respond_to_invite(3, 7, False)  # invites not found


if __name__ == "__main__":
    unittest.main()
