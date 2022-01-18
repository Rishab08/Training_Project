from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
import io


class UserTests(APITestCase):

    def __init__(self):
        self.client = APIClient()
        self.create_account_url = reverse("register")

    def test_create_users(self, users_data):
        users_data["status"] = ""
        users_data["error"] = ""
        for idx in users_data.index:
            user_data = {
                "username": users_data["username"][idx],
                "email": users_data["email"][idx],
                "password": users_data["password"][idx],
                "phone": users_data["phone"][idx],
                "date_of_birth": users_data["date_of_birth"][idx],
            }
            status, error_msg = self._test_create_user(user_data)
            users_data["status"][idx] = status
            users_data["error"][idx] = error_msg

        b_buf = io.BytesIO()
        users_data.to_excel(b_buf)
        return users_data

    def _test_create_user(self, user_data):
        response = self.client.post(self.create_account_url, user_data, format="json")
        if response.status_code == status.HTTP_201_CREATED:
            return "pass", ""
        error_msg = []
        for _, val in response.data.items():
            error_msg.append(val[0])
            break
        error_msg_str = "".join([str(msg) for msg in error_msg])
        return "Fail", error_msg_str
