import unittest
from unittest.mock import patch

from convergence import friends
from convergence import exceptions
from test import fakes


class TestGetFriendships(unittest.TestCase):

    @patch.object(friends, "friend_store")
    def test_get_friendships(self, mock_fs):
        mock_fs.get_friendships_by_user = fakes.get_fake_friendships_by_user
        friendships = friends.get_friendships(3)

        self.assertEqual(friendships[0]["friend_a_id"], 3)
        self.assertEqual(friendships[0]["friend_b_id"], 9)
        self.assertEqual(friendships[0]["friend_name"], "Test Friend")

        mock_fs.get_friendships_by_user = lambda _: None
        self.assertEqual(friends.get_friendships(3), [])


class TestProposeFriendship(unittest.TestCase):

    @patch.object(friends, "friend_store")
    @patch.object(friends, "user_store")
    def test_propose_friendship_success(self, mock_us, mock_fs):
        mock_us.get_user_by_id = fakes.get_fake_user_by_id
        mock_fs.get_invite_by_details = lambda *args: None
        friendinvite = friends.propose_friendship(3, 9)
        self.assertEqual(friendinvite["requesting_id"], 3)
        self.assertEqual(friendinvite["requested_id"], 9)
        mock_fs.add_friendinvite.assert_called_once()

    @patch.object(friends, "friend_store")
    @patch.object(friends, "user_store")
    def test_propose_friendship_fail(self, mock_us, mock_fs):
        mock_us.get_user_by_id = lambda *args: None
        mock_fs.get_invite_by_details = fakes.get_fake_friendinvite

        with self.assertRaises(exceptions.InvalidRequestError):
            friends.propose_friendship(3, 3)

        with self.assertRaises(exceptions.NotFoundError):
            friends.propose_friendship(3, 6)

        mock_us.get_user_by_id = fakes.get_fake_user_by_id
        with self.assertRaises(exceptions.InvalidRequestError):
            friends.propose_friendship(3, 7)

        mock_fs.add_friendship.assert_not_called()


class TestProposeFriendships(unittest.TestCase):

    @patch.object(friends, "friend_store")
    @patch.object(friends, "user_store")
    def test_propose_friendships_success(self, mock_us, mock_fs):
        mock_fs.get_pending_invites_sent = lambda *args: None
        mock_fs.get_friendships_by_user = lambda *args: None
        mock_us.get_users_by_emails = fakes.get_fake_users_by_emails

        emails = [
            "testuser1@gmail.com",
            "testuser2@gmail.com",
            "testuser3@gmail.com"
        ]
        response = friends.propose_friendships(3, emails)
        self.assertEqual(response, set())
        mock_fs.add_friendinvites.assert_called_once()

        mock_fs.get_pending_invites_sent = fakes.get_fake_friendinvites_by_user
        response = friends.propose_friendships(3, emails)
        self.assertEqual(len(response), 3)

    @patch.object(friends, "friend_store")
    @patch.object(friends, "user_store")
    def test_propose_friendships_fail(self, mock_us, mock_fs):
        mock_fs.get_pending_invites_sent = lambda *args: None
        mock_fs.get_friendships_by_user = lambda *args: None
        mock_us.get_users_by_emails = fakes.get_fake_users_by_emails

        emails = ["testuser@gmail.com"] * (friends.MAX_INVITES_PER_REQUEST + 1)
        with self.assertRaises(exceptions.InvalidRequestError):
            friends.propose_friendships(3, emails)


class TestGetInvites(unittest.TestCase):

    @patch.object(friends, "friend_store")
    def test_get_invites(self, mock_fs):
        mock_fs.get_pending_invites_received = fakes.get_fake_pending_invites_by_user
        response = friends.get_invites(3)
        self.assertEquals(len(response), 1)
        self.assertEquals(response[0]["screen_name"], "Fake User")
        self.assertEquals(response[0]["requested_id"], 3)
        self.assertEquals(response[0]["requesting_id"], 5)

        mock_fs.get_pending_invites_received = lambda *args: None
        response = friends.get_invites(3)
        self.assertEquals(response, [])


class TestRespondToInvite(unittest.TestCase):

    @patch.object(friends, "friend_store")
    def test_respond_to_invite_accept(self, mock_fs):
        mock_fs.get_invite_by_id = fakes.get_fake_friendinvite_by_id
        mock_fs.add_friendship_from_invite = fakes.get_fake_friendships_by_friendinvite
        response = friends.respond_to_invite(8, 9, True)
        self.assertEqual(len(response), 2)

    @patch.object(friends, "friend_store")
    def test_respond_to_invite_reject(self, mock_fs):
        mock_fs.get_invite_by_id = fakes.get_fake_friendinvite_by_id
        mock_fs.add_friendship_from_invite = fakes.get_fake_friendships_by_friendinvite
        response = friends.respond_to_invite(8, 9, False)
        self.assertEqual(response, [])
        mock_fs.delete_friendinvite.assert_called_once()

    @patch.object(friends, "friend_store")
    def test_respond_to_invite_fail(self, mock_fs):
        mock_fs.get_invite_by_id = fakes.get_fake_friendinvite_by_id
        mock_fs.add_friendship_from_invite = fakes.get_fake_friendships_by_friendinvite

        with self.assertRaises(exceptions.NotFoundError):
            friends.respond_to_invite(3, 9, True)

        mock_fs.get_invite_by_id = lambda *args: None
        with self.assertRaises(exceptions.NotFoundError):
            friends.respond_to_invite(8, 9, True)


if __name__ == "__main__":
    unittest.main()
