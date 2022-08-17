import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse

from leads.models import Agent, OrganizerUser

User = get_user_model()


@pytest.mark.django_db()
class TestCreateLeads:
    url = reverse('leads')

    def test_if_user_not_authorized_return_401(self, api_client):
        response = api_client.post(self.url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_agent_can_not_create_leads_return_403(self, api_client, agent_user):
        # api_client.force_authenticate(user=User(is_agent=True))
        response = api_client.post(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_organizer_can_create_leads_return_201(
            self, api_client, leads_factory, create_organizer_user
    ):
        user = create_organizer_user[0]
        organizer = OrganizerUser.objects.get(user=user)
        lead = leads_factory.create(organizer=organizer)
        api_client.force_authenticate(user=user)

        response = api_client.post(
            "/api/leads/",
            {
                "first_name": "a",
                "last_name": "b",
                "age": 20,
                "organizer": lead.organizer.pk,
                "agent": lead.agent.pk,
                "category": lead.category.pk,
                "description": "abc",
                "phone_number": 123,
                "email": "email@email.com",
            },
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0

    def test_admin_can_create_leads_return_201(self, api_client, create_lead, admin_user, payload):
        response = api_client.post("/api/leads/", payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0


@pytest.mark.django_db()
class TestRetrieveLeads():
    url = reverse('leads')

    def test_anonymous_user_can_not_see_leads_return_401(self, api_client):
        response = api_client.get(self.url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_normal_user_can_not_see_leads_return_400(self, api_client, normal_user):
        response = api_client.get(self.url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_agent_can_see_leads_return_200(
            self, api_client, create_lead, agent_user,
    ):
        response = api_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK

    def test_organizer_can_see_leads_return_200(
            self, api_client, create_lead, user_factory
    ):
        user = user_factory.create(is_organizer=True)
        api_client.force_authenticate(user=user)

        response = api_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK

    def test_if_lead_exist_return_200(
            self,
            api_client,
            admin_user,
            create_lead
    ):

        response = api_client.get(
            f"/api/leads/{create_lead.id}/",
        )

        assert response.status_code == status.HTTP_200_OK

        # assert response.data == serializer.data
        assert response.data == {
            "id": create_lead.id,
            "first_name": create_lead.first_name,
            "last_name": create_lead.last_name,
            "age": create_lead.age,
            "organizer": create_lead.organizer.id,
            "agent": create_lead.agent.id,
            "category": create_lead.category.id,
            "description": create_lead.description,
            "date_added": create_lead.date_added,
            "phone_number": create_lead.phone_number,
            "email": create_lead.email,
            "converted_date": create_lead.converted_date,
        }
        #

    def test_agent_can_see_one_lead_return_200(
            self, api_client, leads_factory, user_factory
    ):
        user = user_factory.create(is_agent=True)
        agent = Agent.objects.get(user=user)
        lead = leads_factory.create(agent=agent)
        api_client.force_authenticate(user=user)

        response = api_client.get(
            f"/api/leads/{lead.id}/",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": lead.id,
            "first_name": lead.first_name,
            "last_name": lead.last_name,
            "age": lead.age,
            "organizer": lead.organizer.id,
            "agent": lead.agent.id,
            "category": lead.category.id,
            "description": lead.description,
            "date_added": lead.date_added,
            "phone_number": lead.phone_number,
            "email": lead.email,
            "converted_date": lead.converted_date,
        }

    def test_agent_can_not_see_others_lead_return_403(
            self, api_client, leads_factory, create_agent_user
    ):
        user = create_agent_user[0]
        user2 = create_agent_user[1]
        agent = Agent.objects.get(user=user)

        lead = leads_factory.create(agent=agent)

        api_client.force_authenticate(user=user2)

        response = api_client.get(
            f"/api/leads/{lead.id}/",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_organizer_can_not_see_others_lead_return_403(
            self, api_client, leads_factory, create_organizer_user
    ):
        user = create_organizer_user[0]
        user2 = create_organizer_user[1]
        organizer = OrganizerUser.objects.get(user=user)
        # agent2 = Agent.objects.get(user=user2)
        lead = leads_factory.create(organizer=organizer)

        api_client.force_authenticate(user=user2)

        response = api_client.get(
            f"/api/leads/{lead.id}/",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_see_all_leads_return_200(
            self, api_client, admin_user, leads_factory,
    ):
        lead = leads_factory.create()

        response = api_client.get(
            f"/api/leads/{lead.id}/",
        )

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db()
class TestUpdateLeads:
    def test_anonymous_user_can_not_update_leads_return_401(self, api_client, create_lead):
        response = api_client.put(f"/api/leads/{create_lead.id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_normal_user_can_not_update_leads_return_403(
            self, api_client, normal_user, create_lead
    ):
        """Normal user is a user that is not admin, agent or organizer"""
        response = api_client.put(f"/api/leads/{create_lead.id}/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_agent_can_not_update_leads_return_403(
            self, api_client, agent_user, create_lead
    ):
        """
        Agent can see the leads that assigned to him/her by the organizer. Agent can't update or delete leads.
        """
        response = api_client.put(f"/api/leads/{create_lead.id}/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_organizer_can_not_update_other_organizer_leads_return_403(
            self, api_client, create_organizer_user, leads_factory, payload
    ):
        user1 = create_organizer_user[0]
        user2 = create_organizer_user[1]
        organizer = OrganizerUser.objects.get(user=user1)
        lead = leads_factory.create(organizer=organizer)
        api_client.force_authenticate(user2)

        response = api_client.put(f"/api/leads/{lead.id}/", payload)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_update_leads_return_200(
            self, api_client, admin_user, create_lead, payload
    ):
        """Admin can access to everything"""

        response = api_client.put(f"/api/leads/{create_lead.id}/", payload)
        # now the lead that created by create_lead should be equal to the payload

        create_lead.refresh_from_db()
        # without refreshing the database the content of the create_lead stay the same

        assert response.status_code == status.HTTP_200_OK
        assert create_lead.first_name == "a"
        assert create_lead.last_name == "b"
        assert create_lead.age == 20
        assert create_lead.organizer == create_lead.organizer
        assert create_lead.agent == create_lead.agent
        assert create_lead.category == create_lead.category
        assert create_lead.description == "abc"
        assert create_lead.phone_number == "032-647-2000x02836"
        assert create_lead.email == "email@email.com"

    def test_organizer_can_update_leads_return_200(
            self, api_client, create_organizer_user, leads_factory, payload
    ):
        """Organizer can see, update and delete the leads. Organizer assign leads to Agents"""

        user = create_organizer_user[0]
        organizer = OrganizerUser.objects.get(user=user)
        lead = leads_factory.create(organizer=organizer)
        api_client.force_authenticate(user)

        response = api_client.put(f"/api/leads/{lead.id}/", payload)

        lead.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert lead.first_name == "a"
        assert lead.last_name == "b"
        assert lead.age == 20
        assert lead.organizer == lead.organizer
        assert lead.agent == lead.agent
        assert lead.category == lead.category
        assert lead.description == "abc"
        assert lead.phone_number == "032-647-2000x02836"
        assert lead.email == "email@email.com"


@pytest.mark.django_db()
class TestDeleteLeads:
    def test_normal_user_can_not_delete_leads_return_403(
            self, api_client, normal_user, create_lead
    ):
        """Normal user is a user that is not admin, agent or organizer"""
        response = api_client.delete(f"/api/leads/{create_lead.id}/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_agent_can_not_delete_leads_return_403(
            self, api_client, agent_user, create_lead
    ):
        """
        Agent can see the leads that assigned to him/her by the organizer. Agent can't update or delete leads.
        """
        response = api_client.delete(f"/api/leads/{create_lead.id}/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_organizer_can_delete_leads_return_204(
            self, api_client, create_organizer_user, leads_factory, payload
    ):
        """Organizer can see, update and delete the leads. Organizer assign leads to Agents"""

        user = create_organizer_user[0]
        organizer = OrganizerUser.objects.get(user=user)
        lead = leads_factory.create(organizer=organizer)
        api_client.force_authenticate(user)
        response = api_client.delete(f"/api/leads/{lead.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_organizer_can_not_delete_other_organizers_leads_return_403(
            self, api_client, create_organizer_user, leads_factory, payload
    ):
        user = create_organizer_user[0]
        user2 = create_organizer_user[1]
        organizer = OrganizerUser.objects.get(user=user)
        lead = leads_factory.create(organizer=organizer)
        api_client.force_authenticate(user2)
        response = api_client.delete(f"/api/leads/{lead.id}/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_delete_leads_return_204(
            self, api_client, admin_user, create_lead, payload
    ):
        """Admin can access to everything"""

        response = api_client.delete(f"/api/leads/{create_lead.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
