import unittest
from unittest.mock import patch

from convergence import invite
from convergence import exceptions
from test import fakes


class TestInviteUser(unittest.TestCase):

    @patch.object(invite, "userevent_store")
    @patch.object(invite, "userinvite_store")
    @patch.object(invite, "user_store")
    @patch.object(invite, "event_store")
    def test_invite_user_to_event_success(self, mock_es, mock_us, mock_uis,
                                          mock_ues):
        mock_es.get_event_by_id = fakes.get_fake_event
        mock_us.get_user_by_id = fakes.get_fake_user_by_id
        mock_ues.get_userevent = lambda *args: None
        mock_uis.get_invitation_by_details = lambda *args: None

        userinvite = invite.invite_user_to_event(3, 5, 1)
        self.assertEqual(userinvite["inviter_id"], 3)
        self.assertEqual(userinvite["invitee_id"], 5)
        self.assertEqual(userinvite["event_id"], 1)

        userinvite = invite.invite_user_to_event(3, 9, 4)
        self.assertEqual(userinvite["inviter_id"], 3)
        self.assertEqual(userinvite["invitee_id"], 9)
        self.assertEqual(userinvite["event_id"], 4)

    @patch.object(invite, "userevent_store")
    @patch.object(invite, "userinvite_store")
    @patch.object(invite, "user_store")
    @patch.object(invite, "event_store")
    def test_invite_user_to_event_fail(self, mock_es, mock_us, mock_uis,
                                       mock_ues):
        mock_es.get_event_by_id = fakes.get_fake_event
        mock_us.get_user_by_id = fakes.get_fake_user_by_id

        with self.assertRaises(exceptions.InvalidRequestError):
            invite.invite_user_to_event(1, 1, 5)  # cannot invite self
        with self.assertRaises(exceptions.NotFoundError):
            invite.invite_user_to_event(1, 7, 1)  # not event owner

        mock_es.get_event_by_id = lambda _: None
        with self.assertRaises(exceptions.NotFoundError):
            invite.invite_user_to_event(1, 3, 5)  # event not found

        mock_es.get_event_by_id = fakes.get_fake_event
        mock_us.get_user_by_id = lambda _: None
        with self.assertRaises(exceptions.NotFoundError):
            invite.invite_user_to_event(1, 7, 3)  # user not found

        mock_us.get_user_by_id = fakes.get_fake_user_by_id
        mock_es.get_event_by_id = fakes.get_fake_event
        mock_ues.get_userevent = lambda *args: True
        mock_uis.get_invitation_by_id = lambda *args: None

        with self.assertRaises(exceptions.InvalidRequestError):
            invite.invite_user_to_event(3, 9, 4)  # User already event member

        mock_ues.get_userevent = lambda *args: None
        mock_uis.get_invitation_by_id = lambda *args: True
        with self.assertRaises(exceptions.InvalidRequestError):
            invite.invite_user_to_event(3, 9, 4)  # Invite already pending


class TestGetInvitations(unittest.TestCase):

    @patch.object(invite, "userinvite_store")
    def test_get_invitations(self, mock_uis):
        mock_uis.get_invitations_by_user = fakes.get_fake_userinvites
        invitations = invite.get_invitations(3)
        self.assertEqual(invitations[0]["id"], 19)
        self.assertEqual(invitations[0]["event_name"], "Fake Event")
        self.assertEqual(invitations[0]["event_owner_id"], 3)
        self.assertEqual(invitations[0]["owner_name"], "Fake Owner")
        self.assertEqual(invitations[0]["invitation_id"], 1)
        self.assertEqual(invitations[0]["inviter_name"], "Fake Owner")
        self.assertEqual(invitations[1]["id"], 21)
        self.assertEqual(invitations[1]["event_name"], "Another Fake Event")
        self.assertEqual(invitations[1]["event_owner_id"], 6)
        self.assertEqual(invitations[1]["owner_name"], "Another Fake")
        self.assertEqual(invitations[1]["invitation_id"], 2)
        self.assertEqual(invitations[1]["inviter_name"], "Not The Owner")

        mock_uis.get_invitations_by_user = lambda _: None
        self.assertEqual(invite.get_invitations(3), [])


class TestRespondToInvitation(unittest.TestCase):

    @patch.object(invite, "event_store")
    @patch.object(invite, "events")
    @patch.object(invite, "userinvite_store")
    def test_respond_accept(self, mock_uis, mock_events, mock_es):
        mock_uis.get_invitation_by_id = fakes.get_fake_userinvite
        mock_es.get_event_by_id = fakes.get_fake_event
        event_response = invite.respond_to_invitation(7, 2, True)
        self.assertEqual(event_response["id"], 6)
        self.assertEqual(event_response["event_name"], "Fake Event")
        self.assertEqual(event_response["event_owner_id"], 3)

    @patch.object(invite, "event_store")
    @patch.object(invite, "events")
    @patch.object(invite, "userinvite_store")
    def test_respond_reject(self, mock_uis, mock_events, mock_es):
        mock_uis.get_invitation_by_id = fakes.get_fake_userinvite
        mock_es.get_event_by_id = fakes.get_fake_event
        response = invite.respond_to_invitation(7, 2, False)
        self.assertEqual(response, None)

    @patch.object(invite, "event_store")
    @patch.object(invite, "events")
    @patch.object(invite, "userinvite_store")
    def test_respond_fail(self, mock_uis, mock_events, mock_es):
        mock_uis.get_invitation_by_id = fakes.get_fake_userinvite
        mock_es.get_event_by_id = fakes.get_fake_event

        with self.assertRaises(exceptions.NotFoundError):
            invite.respond_to_invitation(1, 2, False)  # not this user's invite

        mock_uis.get_invitation_by_id = lambda _: None
        with self.assertRaises(exceptions.NotFoundError):
            invite.respond_to_invitation(3, 7, False)  # invite not found


if __name__ == "__main__":
    unittest.main()
