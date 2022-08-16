import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from pytest_factoryboy import register

from leads.tests.factories import LeadsFactory, UserFactory, OrganizerUserFactory, AgentFactory

register(LeadsFactory)
register(UserFactory)
register(OrganizerUserFactory)
register(AgentFactory)

User = get_user_model()


@pytest.fixture()
def api_client():
    return APIClient()


@pytest.fixture()
def admin_user(api_client):
    return api_client.force_authenticate(user=User(is_superuser=True))


@pytest.fixture()
def agent_user(api_client):
    return api_client.force_authenticate(user=User(is_agent=True))


@pytest.fixture()
def organizer_user(api_client):

    return api_client.force_authenticate(user=User(is_organizer=True))


@pytest.fixture()
def normal_user(api_client):
    return api_client.force_authenticate(user=User())


@pytest.fixture()
def create_lead(db, leads_factory):
    create_lead = leads_factory.create()
    return create_lead


@pytest.fixture()
def create_leads(db, leads_factory):
    create_lead = leads_factory.create_batch(size=2)
    return create_lead


@pytest.fixture()
def create_organizer_user(db, organizer_user_factory):
    create_organizer = organizer_user_factory.create_batch(size=2)
    return create_organizer


@pytest.fixture()
def create_agent_user(db, agent_factory):
    create_agent = agent_factory.create()
    return create_agent


@pytest.fixture()
def payload(create_lead):
    return {
        'first_name': 'a',
        'last_name': 'b',
        'age': 20,
        'organizer': create_lead.organizer.pk,
        'agent': create_lead.agent.pk,
        'category': create_lead.category.pk,
        'description': 'abc',
        'phone_number': '032-647-2000x02836',
        'email': 'email@email.com'
    }


@pytest.fixture()
def lead1(db, leads_factory):
    lead = leads_factory.create()
    lead1 = {
        'id': lead.id,
        'first_name': lead.first_name,
        'last_name': lead.last_name,
        'age': lead.age,
        'organizer': lead.organizer.id,
        'agent': lead.agent.id,
        'category': lead.category.id,
        'description': lead.description,
        'date_added': lead.date_added,
        'phone_number': lead.phone_number,
        'email': lead.email,
        'converted_date': lead.converted_date,
    }

    return lead1
