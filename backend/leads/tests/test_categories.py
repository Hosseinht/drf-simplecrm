import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse

User = get_user_model()


@pytest.mark.django_db()
class TestCreateCategories:
    url = reverse("categories-list")

    def test_if_user_is_anonymous_return_401(self, api_client):
        response = api_client.post(self.url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_normal_user_can_not_create_category_return_403(
        self, api_client, normal_user
    ):
        response = api_client.post(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_agent_can_not_create_category_return_403(self, api_client, agent_user):
        response = api_client.post(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_organizer_can_create_category_return_200(self, api_client, organizer_user):
        response = api_client.post(self.url, {"title": "a"})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0

    def test_admin_can_create_category_return_200(self, api_client, admin_user):
        response = api_client.post(self.url, {"title": "a"})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0


@pytest.mark.django_db()
class TestRetrieveCategories:
    url = reverse("categories-list")

    def test_if_user_is_anonymous_return_401(self, api_client):
        response = api_client.get(self.url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_normal_user_can_not_create_category_return_400(
        self, api_client, normal_user
    ):
        response = api_client.get(self.url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_agent_can_see_categories_return_200(self, api_client, agent_user):
        response = api_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK

    def test_organizer_can_see_categories_return_200(self, api_client, organizer_user):
        response = api_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_see_categories_return_200(self, api_client, admin_user):
        response = api_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db()
class TestUpdateCategories:
    def test_anonymous_user_can_not_update_categories_return_401(
        self, api_client, create_category
    ):
        response = api_client.put(f"/api/categories/{create_category.id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_normal_user_can_not_update_categories_return_403(
        self, api_client, normal_user, create_category
    ):
        response = api_client.put(f"/api/categories/{create_category.id}/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_agent_can_not_update_categories_return_403(
        self, api_client, normal_user, create_category
    ):
        response = api_client.put(f"/api/categories/{create_category.id}/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_organizer_can_update_categories_return_200(
        self, api_client, organizer_user, create_category
    ):
        response = api_client.put(
            f"/api/categories/{create_category.id}/", {"title": "b"}
        )

        create_category.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert create_category.title == "b"

    def test_can_can_update_categories_return_200(
        self, api_client, admin_user, create_category
    ):
        response = api_client.put(
            f"/api/categories/{create_category.id}/", {"title": "b"}
        )

        create_category.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert create_category.title == "b"


@pytest.mark.django_db()
class TestDeleteCategories:
    def test_anonymous_user_can_not_delete_categories_return_401(
        self, api_client, create_category
    ):
        response = api_client.delete(f"/api/categories/{create_category.id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_normal_user_can_not_delete_categories_return_403(
        self, api_client, normal_user, create_category
    ):
        response = api_client.delete(f"/api/categories/{create_category.id}/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_agent_can_not_delete_categories_return_403(
        self, api_client, normal_user, create_category
    ):
        response = api_client.delete(f"/api/categories/{create_category.id}/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_organizer_can_delete_categories_return_200(
        self, api_client, organizer_user, create_category
    ):
        response = api_client.delete(f"/api/categories/{create_category.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_admin_can_delete_categories_return_200(
        self, api_client, admin_user, create_category
    ):
        response = api_client.delete(f"/api/categories/{create_category.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
