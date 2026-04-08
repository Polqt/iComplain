import json

from django.contrib.auth import get_user_model
from django.test import TestCase


User = get_user_model()


class UserAuthApiTests(TestCase):
    def setUp(self) -> None:
        self.password = "StrongPassword123!"
        self.user = User.objects.create_user(
            email="student@usls.edu.ph",
            password=self.password,
        )

    def test_csrf_endpoint_returns_token(self) -> None:
        response = self.client.get("/api/user/csrf")

        self.assertEqual(response.status_code, 200)
        self.assertIn("csrfToken", response.json())

    def test_login_returns_authenticated_user(self) -> None:
        response = self.client.post(
            "/api/user/login",
            data=json.dumps(
                {
                    "email": self.user.email,
                    "password": self.password,
                }
            ),
            content_type="application/json",
        )

        payload = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(payload["success"])
        self.assertEqual(payload["user"]["email"], self.user.email)
        self.assertIn("sessionid", response.cookies)

    def test_profile_requires_authentication(self) -> None:
        response = self.client.get("/api/user/profile")
        payload = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertFalse(payload["success"])
        self.assertIsNone(payload["user"])

    def test_profile_returns_authenticated_user(self) -> None:
        self.client.force_login(self.user)

        response = self.client.get("/api/user/profile")
        payload = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(payload["success"])
        self.assertEqual(payload["user"]["email"], self.user.email)

    def test_logout_contract(self) -> None:
        self.client.force_login(self.user)

        response = self.client.post("/api/user/logout")
        payload = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(payload["success"])
        self.assertIsNone(payload["user"])

    def test_google_login_rejects_missing_or_invalid_token(self) -> None:
        response = self.client.post(
            "/api/user/google-login",
            data=json.dumps({"id_token": "invalid-token"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertFalse(payload["success"])
        self.assertIsNone(payload["user"])
