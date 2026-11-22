from django.contrib.auth import get_user_model
from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from applications.models import SkinRequestModel
from applications.admin import SkinRequestAdmin
from catalog.models import WeaponModel, SkinModel

User = get_user_model()


class SkinRequestTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="pass12345")

    def setUp(self):
        self.weapon = WeaponModel.objects.create(name="Vandal", slug="vandal")
        self.skin = SkinModel.objects.create(
            name="Prime",
            slug="prime",
            weapon=self.weapon
            )

    def test_skin_request_str(self):
        request = SkinRequestModel.objects.create(
            skin=self.skin,
            nickname="NoobMaster",
            status=SkinRequestModel.STATUS_NEW,
            message="",
            user=self.user,
        )
        self.assertEqual(str(request), "Ник: NoobMaster -> Скин: Prime -> Vandal")

    def test_default_status(self):
        request = SkinRequestModel.objects.create(
            skin=self.skin,
            nickname="TestUser",
            message="",
            user=self.user,
            )
        self.assertEqual(request.status, SkinRequestModel.STATUS_NEW)


class AdminActionTest(TestCase):
    def setUp(self):
        self.weapon = WeaponModel.objects.create(name="Phantom", slug="phantom")
        self.skin = SkinModel.objects.create(
            name="Oni",
            slug="oni",
            weapon=self.weapon
            )
        self.admin_site = AdminSite()
        self.admin = SkinRequestAdmin(SkinRequestModel, self.admin_site)
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="pass12345")

    def test_approve_action(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        requester = User.objects.create_user(username="requester", password="pass")
        req1 = SkinRequestModel.objects.create(
            skin=self.skin,
            nickname="User1",
            message="Хочу скин!",
            status=SkinRequestModel.STATUS_NEW,
            user=requester,
        )
        req2 = SkinRequestModel.objects.create(skin=self.skin, nickname="User2", message="", status=SkinRequestModel.STATUS_NEW, user=requester)
        queryset = SkinRequestModel.objects.filter(id__in=[req1.id, req2.id])
        self.admin.approve(request=None, queryset=queryset)
        req1.refresh_from_db()
        req2.refresh_from_db()
        self.assertEqual(req1.status, SkinRequestModel.STATUS_APPROVED)
        self.assertEqual(req2.status, SkinRequestModel.STATUS_APPROVED)
