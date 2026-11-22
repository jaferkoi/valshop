from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from applications.models import SkinRequestModel
from catalog.models import SkinModel, WeaponModel
from users.forms import SignUpForm
from users.models import Profile

User = get_user_model()


class UserAndProfileModelTests(TestCase):
    def test_user_create_works(self):
        user = User.objects.create(username="abc")
        self.assertEqual(user.username, "abc")

    def test_profile_created_by_signal(self):
        user = User.objects.create(username="abc")
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_resaving_user_does_not_duplicate_profile(self):
        user = User.objects.create(username="abc")
        user.save()
        self.assertEqual(Profile.objects.filter(user=user).count(), 1)


class SignUpTests(TestCase):
    def test_signup_page_returns_200(self):
        response = self.client.get(reverse("users:signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/signup.html")

    def test_form_has_username_and_password_fields(self):
        form = SignUpForm()
        self.assertIn("username", form.fields)
        self.assertIn("password1", form.fields)
        self.assertIn("password2", form.fields)

    def test_signup_creates_user_and_profile(self):
        response = self.client.post(
            reverse("users:signup"),
            {
                "username": "newuser",
                "password1": "StrongPass!42",
                "password2": "StrongPass!42",
            },
        )
        self.assertRedirects(response, reverse("users:login"))
        user = User.objects.get(username="newuser")
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_signup_with_mismatched_passwords_fails(self):
        response = self.client.post(
            reverse("users:signup"),
            {
                "username": "newuser",
                "password1": "StrongPass!42",
                "password2": "OtherPass!42",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="newuser").exists())

    def test_signup_with_existing_username_fails(self):
        User.objects.create(username="taken")
        response = self.client.post(
            reverse("users:signup"),
            {
                "username": "taken",
                "password1": "StrongPass!42",
                "password2": "StrongPass!42",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(username="taken").count(), 1)


class LoginLogoutTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = "StrongPass!42"
        cls.user = User.objects.create_user(
            username="abc", password=cls.password
        )

    def test_login_page_returns_200(self):
        response = self.client.get(reverse("users:login"))
        self.assertEqual(response.status_code, 200)

    def test_login_with_valid_credentials(self):
        response = self.client.post(
            reverse("users:login"),
            {"username": "abc", "password": self.password},
        )
        self.assertRedirects(response, reverse("users:profile"))

    def test_login_with_wrong_password(self):
        response = self.client.post(
            reverse("users:login"),
            {"username": "abc", "password": "wrong"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)

    def test_logout_requires_confirmation(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("users:logout"))
        self.assertEqual(response.status_code, 405)

    def test_logout_deauthenticates_user(self):
        self.client.force_login(self.user)
        self.client.post(reverse("users:logout"))
        response = self.client.get(reverse("users:profile"))
        self.assertRedirects(
            response, f"{reverse('users:login')}?next={reverse('users:profile')}"
        )


class ProfileTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="abc", password="StrongPass!42"
        )

    def test_profile_requires_authentication(self):
        response = self.client.get(reverse("users:profile"))
        self.assertEqual(response.status_code, 302)

    def test_profile_page_returns_200_for_owner(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("users:profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile.html")

    def test_profile_shows_current_name(self):
        self.client.force_login(self.user)
        self.user.name = "Вася"
        self.user.save()
        response = self.client.get(reverse("users:profile"))
        self.assertContains(response, "Вася")

    def test_profile_form_updates_name(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("users:profile"), {"name": "Петя"}
        )
        self.assertRedirects(response, reverse("users:profile"))
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, "Петя")

    def test_success_message_shown_after_save(self):
        self.client.force_login(self.user)
        self.client.post(reverse("users:profile"), {"name": "Петя"})
        response = self.client.get(reverse("users:profile"))
        self.assertContains(response, "Профиль успешно изменён")


class ProfileApplicationsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="jaferkoi", password="StrongPass!42"
        )
        cls.other = User.objects.create_user(
            username="someone", password="StrongPass!42"
        )
        cls.weapon = WeaponModel.objects.create(
            name="вандал", slug="vandal", is_published=True
        )
        cls.skin = SkinModel.objects.create(
            name="прайм", slug="prime", weapon=cls.weapon, is_published=True
        )

    def _make_request(self, user=None):
        return SkinRequestModel.objects.create(
            skin=self.skin,
            nickname="jaferkoi",
            message="Хочу скин!",
            user=user,
        )

    def test_detail_requires_authentication(self):
        response = self.client.get(
            reverse("users:profile_application_detail", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 302)

    def test_profile_shows_own_applications(self):
        self.client.force_login(self.user)
        own = self._make_request(user=self.user)
        response = self.client.get(reverse("users:profile"))
        self.assertIn(own, list(response.context["applications"]))

    def test_profile_hides_foreign_applications(self):
        self.client.force_login(self.user)
        foreign = self._make_request(user=self.other)
        response = self.client.get(reverse("users:profile"))
        self.assertNotIn(foreign, list(response.context["applications"]))

    def test_foreign_detail_returns_404(self):
        self.client.force_login(self.user)
        foreign = self._make_request(user=self.other)
        response = self.client.get(
            reverse("users:profile_application_detail", kwargs={"pk": foreign.pk})
        )
        self.assertEqual(response.status_code, 404)

    def test_own_detail_returns_200(self):
        self.client.force_login(self.user)
        own = self._make_request(user=self.user)
        response = self.client.get(
            reverse("users:profile_application_detail", kwargs={"pk": own.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, own.skin.name)
        self.assertContains(response, own.nickname)
