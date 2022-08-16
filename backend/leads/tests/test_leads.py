import datetime
from time import strftime

import pytest
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from freezegun import freeze_time
from rest_framework import status

from leads.models import Agent, OrganizerUser

User = get_user_model()


# test the endpoints of our api not the implementation like Leads.objects.create()
@pytest.mark.django_db()
class TestCreateLeads:
    def test_if_user_not_authorized_return_403(self, api_client):
        response = api_client.post("/api/leads/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_agent_cant_create_leads_return_401(self, api_client):
        api_client.force_authenticate(user=User(is_agent=True))
        response = api_client.post("/api/leads/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_organizer_can_create_leads_return_201(
        self, api_client, create_lead, user_factory
    ):
        user = user_factory.create(is_organizer=True)
        api_client.force_authenticate(user=user)
        # lead = leads_factory.create()
        # print(leads_factory.__dict__)
        response = api_client.post(
            "/api/leads/",
            {
                "first_name": "a",
                "last_name": "b",
                "age": 20,
                "organizer": create_lead.organizer.pk,
                "agent": create_lead.agent.pk,
                "category": create_lead.category.pk,
                "description": "abc",
                "phone_number": 123,
                "email": "email@email.com",
            },
        )
        print(response.data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0

    def test_admin_can_create_leads_return_201(self, api_client, create_lead):
        api_client.force_authenticate(user=User(is_staff=True))
        # lead = create_lead
        print(create_lead.__dict__)

        # print(leads_factory.__dict__)
        response = api_client.post(
            "/api/leads/",
            {
                "first_name": "a",
                "last_name": "b",
                "age": 20,
                "organizer": create_lead.organizer.pk,
                "agent": create_lead.agent.pk,
                "category": create_lead.category.pk,
                "description": "abc",
                "phone_number": 123,
                "email": "email@email.com",
            },
        )
        print(response.data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0


@pytest.mark.django_db()
class TestRetrieveLeads:
    def test_anonymous_user_cant_see_leads_return_401(self, api_client):
        response = api_client.get("/api/leads/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_normal_user_cant_see_leads_return_400(self, api_client):
        api_client.force_authenticate(user=User())

        response = api_client.get("/api/leads/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_agent_can_see_leads_return_200(
        self, api_client, create_lead, user_factory
    ):
        user = user_factory.create(is_agent=True)
        api_client.force_authenticate(user=user)

        response = api_client.get("/api/leads/")

        assert response.status_code == status.HTTP_200_OK

    def test_organizer_can_see_leads_return_200(
        self, api_client, create_lead, user_factory
    ):
        user = user_factory.create(is_organizer=True)
        api_client.force_authenticate(user=user)

        response = api_client.get("/api/leads/")

        assert response.status_code == status.HTTP_200_OK

    def test_if_lead_exist_return_200(
        self,
        api_client,
        admin_user,
        leads_factory,
    ):
        lead = leads_factory.create()
        # api_client.force_authenticate(user=User(is_superuser=True))
        response = api_client.get(
            f"/api/leads/{lead.id}/",
        )

        assert response.status_code == status.HTTP_200_OK

        # assert response.data == serializer.data
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
        #

    def test_agent_can_see_one_lead_return_200(
        self, api_client, leads_factory, user_factory
    ):
        user = user_factory.create(is_agent=True)
        user2 = user_factory.create(is_agent=True)
        agent = Agent.objects.get(user=user)
        # agent2 = Agent.objects.get(user=user2)
        lead = leads_factory.create(agent=agent)
        print(lead.agent)
        api_client.force_authenticate(user=user)
        # print(agent)

        print(user.__dict__)
        # agent = agent_factory.create(agent=user)
        # print(agent.__dict__)
        # lead = leads_factory.create()
        # lead.agent = agent2

        print(lead.__dict__)
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

    def test_agent_cant_see_others_lead_return_403(
        self, api_client, leads_factory, user_factory
    ):
        user = user_factory.create(is_agent=True)
        user2 = user_factory.create(is_agent=True)
        agent = Agent.objects.get(user=user)
        # agent2 = Agent.objects.get(user=user2)
        lead = leads_factory.create(agent=agent)

        api_client.force_authenticate(user=user2)

        response = api_client.get(
            f"/api/leads/{lead.id}/",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_organizer_cant_see_others_lead_return_403(
        self, api_client, leads_factory, user_factory
    ):
        user = user_factory.create(is_organizer=True)
        user2 = user_factory.create(is_organizer=True)
        organizer = OrganizerUser.objects.get(user=user)
        # agent2 = Agent.objects.get(user=user2)
        lead = leads_factory.create(organizer=organizer)

        api_client.force_authenticate(user=user2)

        response = api_client.get(
            f"/api/leads/{lead.id}/",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_see_all_leads_return_200(
        self, api_client, admin_user, leads_factory, user_factory
    ):
        user = user_factory.create(is_organizer=True)
        organizer = OrganizerUser.objects.get(user=user)
        # agent2 = Agent.objects.get(user=user2)
        lead = leads_factory.create(organizer=organizer)

        # api_client.force_authenticate(user=User(is_superuser=True))

        response = api_client.get(
            f"/api/leads/{lead.id}/",
        )

        assert response.status_code == status.HTTP_200_OK


# def test_admin_can_update_leads_return_200(self, api_client, leads_factory, user_factory):
#     # user = user_factory.create(is_organizer=True)
#     # organizer = OrganizerUser.objects.get(user=user)
#     # # agent2 = Agent.objects.get(user=user2)
#     lead = leads_factory.create()
#     lead2 = lead.objects.all().first()
#
#     api_client.force_authenticate(user=User(is_staff=True))
#
#     response = api_client.put(f'/api/leads/{lead.id}/', lead)
#     print(lead.__dict__)
#     assert response.status_code == status.HTTP_200_OK
#     assert lead.first_name == 'a'


@pytest.mark.django_db()
class TestUpdateLeads:
    def test_anonymous_user_cant_update_leads_return_401(self, api_client, create_lead):
        response = api_client.put(f"/api/leads/{create_lead.id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_normal_user_cant_update_leads_return_403(
        self, api_client, normal_user, create_lead
    ):
        """Normal user is a user that is not admin, agent or organizer"""
        response = api_client.put(f"/api/leads/{create_lead.id}/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_agent_cant_update_leads_return_403(
        self, api_client, agent_user, create_lead
    ):
        """
        Agent can see the leads that assigned to him/her by the organizer. Agent can't update or delete leads.
        """
        response = api_client.put(f"/api/leads/{create_lead.id}/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_organizer_can_update_leads_return_200(
        self, api_client, user_factory, leads_factory, payload
    ):
        """Organizer can see, update and delete the leads. Organizer assign leads to Agents"""
        user1 = user_factory.create(is_organizer=True)
        organizer = OrganizerUser.objects.get(user=user1)
        lead = leads_factory.create(organizer=organizer)
        api_client.force_authenticate(user1)
        response = api_client.put(f"/api/leads/{lead.id}/", payload)

        assert response.status_code == status.HTTP_200_OK

    def test_organizer_cant_update_other_organizer_leads_return_403(
        self, api_client, user_factory, leads_factory, payload
    ):
        user1 = user_factory.create(is_organizer=True)
        user2 = user_factory.create(is_organizer=True)
        organizer = OrganizerUser.objects.get(user=user1)
        lead = leads_factory.create(organizer=organizer)
        api_client.force_authenticate(user2)

        response = api_client.put(f"/api/leads/{lead.id}/", payload)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_update_leads_return_200(
        self, api_client, admin_user, create_lead, payload
    ):
        """Admin can access to everything"""
        # api_client.force_authenticate(user=User(is_superuser=True))
        response = api_client.put(f"/api/leads/{create_lead.id}/", payload)
        print(response.data)
        create_lead.refresh_from_db()
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


@pytest.mark.django_db()
class TestDeleteLeads:
    def test_normal_user_cant_delete_leads_return_403(
        self, api_client, normal_user, create_lead
    ):
        """Normal user is a user that is not admin, agent or organizer"""
        response = api_client.delete(f"/api/leads/{create_lead.id}/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_agent_cant_delete_leads_return_403(
        self, api_client, agent_user, create_lead
    ):
        """
        Agent can see the leads that assigned to him/her by the organizer. Agent can't update or delete leads.
        """
        response = api_client.delete(f"/api/leads/{create_lead.id}/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_organizer_can_update_leads_return_200(
        self, api_client, user_factory, leads_factory, payload
    ):
        """Organizer can see, update and delete the leads. Organizer assign leads to Agents"""

        user = user_factory.create(is_organizer=True)
        organizer = OrganizerUser.objects.get(user=user)
        lead = leads_factory.create(organizer=organizer)
        api_client.force_authenticate(user)
        response = api_client.delete(f"/api/leads/{lead.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_admin_can_delete_leads_return_200(
        self, api_client, admin_user, create_lead, payload
    ):
        """Admin can access to everything"""
        # api_client.force_authenticate(user=User(is_superuser=True))
        response = api_client.delete(f"/api/leads/{create_lead.id}/")
        print(response.data)
        assert response.status_code == status.HTTP_204_NO_CONTENT
