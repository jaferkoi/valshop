from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from catalog.models import WeaponModel, SkinModel
from applications.models import SkinRequestModel


User = get_user_model()


class WeaponTests(TestCase):
    def setUp(self):
        self.weapon = WeaponModel.objects.create(name="vandal", slug="vandal")
        self.skin = SkinModel.objects.create(
            name="oni", slug="oni", weapon=self.weapon
        )

    def test_weapon_is_published_by_default(self):
        self.assertTrue(self.weapon.is_published)

    def test_skin_weapon_relation(self):
        self.assertEqual(self.skin.weapon.name, "vandal")

    def test_weapon_str(self):
        self.assertEqual(str(self.weapon), "vandal")

    def test_skin_str(self):
        self.assertEqual(str(self.skin), "Скин: oni -> vandal")


class PublicationFilterTests(TestCase):
    """Черновики и скины скрытых родителей не видны на сайте."""

    @classmethod
    def setUpTestData(cls):
        cls.weapon = WeaponModel.objects.create(
            name="vandal", slug="vandal", is_published=True
        )
        cls.hidden_weapon = WeaponModel.objects.create(
            name="phantom", slug="phantom", is_published=False
        )
        cls.published_skin = SkinModel.objects.create(
            name="oni", slug="oni", weapon=cls.weapon, is_published=True
        )
        cls.draft_skin = SkinModel.objects.create(
            name="sneaky", slug="sneaky", weapon=cls.weapon, is_published=False
        )
        cls.orphan_skin = SkinModel.objects.create(
            name="ion", slug="ion", weapon=cls.hidden_weapon, is_published=True
        )
        cls.user = User.objects.create_user(username="viewer", password="pass12345")

    def test_home_shows_only_published(self):
        response = self.client.get(reverse("homepage:home"))
        skins = list(response.context["skins"])
        self.assertIn(self.published_skin, skins)
        self.assertNotIn(self.draft_skin, skins)
        self.assertNotIn(self.orphan_skin, skins)

    def test_skin_list_hides_drafts_and_orphans(self):
        response = self.client.get(reverse("catalog:skin_list"))
        skins = list(response.context["skins"])
        self.assertIn(self.published_skin, skins)
        self.assertNotIn(self.draft_skin, skins)
        self.assertNotIn(self.orphan_skin, skins)

    def test_skin_list_filter_by_weapon(self):
        response = self.client.get(
            reverse("catalog:skin_list"), {"weapon": "vandal"}
        )
        skins = list(response.context["skins"])
        self.assertIn(self.published_skin, skins)
        self.assertNotIn(self.orphan_skin, skins)

    def test_skin_detail_shows_published(self):
        self.client.force_login(self.user)
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("catalog:skin_detail", kwargs={"slug": self.published_skin.slug})
        )
        self.assertEqual(response.status_code, 200)

    def test_skin_detail_draft_returns_404(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("catalog:skin_detail", kwargs={"slug": self.draft_skin.slug})
        )
        self.assertEqual(response.status_code, 404)

    def test_skin_detail_of_hidden_weapon_returns_404(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("catalog:skin_detail", kwargs={"slug": self.orphan_skin.slug})
        )
        self.assertEqual(response.status_code, 404)

    def test_weapon_detail_shows_only_published_skins(self):
        response = self.client.get(
            reverse("catalog:weapon_detail", kwargs={"slug": self.weapon.slug})
        )
        self.assertEqual(response.status_code, 200)
        skins = list(response.context["skins"])
        self.assertIn(self.published_skin, skins)
        self.assertNotIn(self.draft_skin, skins)

    def test_hidden_weapon_returns_404(self):
        response = self.client.get(
            reverse("catalog:weapon_detail", kwargs={"slug": self.hidden_weapon.slug})
        )
        self.assertEqual(response.status_code, 404)


class SkinRequestFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.weapon = WeaponModel.objects.create(
            name="вандал", slug="vandal", is_published=True
        )
        cls.skin = SkinModel.objects.create(
            name="прайм", slug="prime", weapon=cls.weapon, is_published=True
        )
        cls.url = reverse("catalog:skin_detail", kwargs={"slug": cls.skin.slug})
        cls.data = {"nickname": "jaferkoi", "message": "Хочу скин!"}

    def test_anonymous_cannot_create_request(self):
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(SkinRequestModel.objects.count(), 0)

    def test_create_skin_request_logged_in(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.create_user(username="jaferkoi", password="pass12345")
        self.client.force_login(user)

        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 302)

        request_obj = SkinRequestModel.objects.first()
        self.assertEqual(request_obj.user, user)
        self.assertEqual(request_obj.nickname, "jaferkoi")
