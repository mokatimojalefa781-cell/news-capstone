from django.test import TestCase
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class CustomUserModelTest(TestCase):
    def setUp(self):
        # Create a reader
        self.reader = CustomUser.objects.create_user(
            username="reader_test",
            password="Mojalefa1999",
            role="reader"
        )
        # Create a journalist
        self.journalist = CustomUser.objects.create_user(
            username="journalist_test",
            password="Mojalefa1999",
            role="journalist"
        )
        # Create an editor
        self.editor = CustomUser.objects.create_user(
            username="editor_test",
            password="Mojalefa1999",
            role="editor"
        )

    def test_user_roles(self):
        self.assertEqual(self.reader.role, "reader")
        self.assertFalse(self.reader.is_staff)

        self.assertEqual(self.journalist.role, "journalist")
        self.assertFalse(self.journalist.is_staff)

        self.assertEqual(self.editor.role, "editor")
        self.assertTrue(self.editor.is_staff)

