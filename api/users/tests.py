from django.test import TestCase
from django.contrib.auth import get_user_model

class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username = "standard",
            email = "standard@user.com",
            password= "standardStrongPass1!"
        )
        self.assertEqual(user.email, "standard@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username = "admin",
            email = "admin@manager.com",
            password = "adminStrongPass1!"
        )
        self.assertEqual(admin_user.email, "admin@manager.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
