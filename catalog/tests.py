from django.urls import reverse
from django.test import TestCase
from catalog.models import WeaponModel, SkinModel


class WeaponTests(TestCase):
    def setUp(self):
        self.weapon = WeaponModel.objects.create(
            name="vandal",
            slug="vandal"
        )
        self.skin = SkinModel.objects.create(
            name="oni",
            slug="oni",
            weapon=self.weapon
        )

    def test_weapon_is_published_by_default(self):
        self.assertTrue(self.weapon.is_published)
 
    def test_skin_weapon_relation(self):
        self.assertEqual(self.skin.weapon.name, "vandal")

    def test_weapon_str(self):
        self.assertEqual(str(self.weapon), "vandal")


class PublishedManagerTest(TestCase):
    def setUp(self):
        self.weapon = WeaponModel.objects.create(name="Vandal", slug="vandal")

        self.skin_pub = SkinModel.objects.create(
            name="Prime",
            slug="prime",
            weapon=self.weapon,
            is_published=True
        )

        self.skin_unpub = SkinModel.objects.create(
            name="Sneaky",
            slug="sneaky",
            weapon=self.weapon,
            is_published=False,
        )

    def test_published_manager(self):
        self.assertEqual(SkinModel._base_manager.count(), 2)
        self.assertTrue(SkinModel._base_manager.filter(name="Sneaky").exists())
