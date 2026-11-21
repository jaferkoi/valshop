from django.test import TestCase

from users.models import User


class UsersTests(TestCase):
    def test_user_create_works(self):
        user = User.objects.create(
            username="abc",
            password="123",
        )
        self.assertEqual(user.username, "abc", msg="Имя не совпадает",)
