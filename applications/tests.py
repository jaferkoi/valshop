from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from applications.models import SkinRequestModel
from applications.admin import SkinRequestAdmin
from catalog.models import WeaponModel, SkinModel


class SkinRequestTest(TestCase):
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
            message=""
        )
        self.assertEqual(str(request), "Ник: NoobMaster -> Скин: Prime -> Vandal")

    def test_default_status(self):
        request = SkinRequestModel.objects.create(
            skin=self.skin,
            nickname="TestUser",
            message="",
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

    def test_approve_action(self):
        req1 = SkinRequestModel.objects.create(skin=self.skin, nickname="User1", message="", status=SkinRequestModel.STATUS_NEW)
        req2 = SkinRequestModel.objects.create(skin=self.skin, nickname="User2", message="", status=SkinRequestModel.STATUS_NEW)
        queryset = SkinRequestModel.objects.filter(id__in=[req1.id, req2.id])
        self.admin.approve(request=None, queryset=queryset)
        req1.refresh_from_db()
        req2.refresh_from_db()
        self.assertEqual(req1.status, SkinRequestModel.STATUS_APPROVED)
        self.assertEqual(req2.status, SkinRequestModel.STATUS_APPROVED)
