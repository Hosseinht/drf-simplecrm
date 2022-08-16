
import factory.fuzzy

from faker import Faker


from core.models import User
from leads.models import Agent, Category, Lead, OrganizerUser

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: "john%s" % n)
    email = factory.LazyAttribute(lambda o: "%s@example.org" % o.username)


class OrganizerUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrganizerUser

    user = factory.SubFactory(UserFactory)


class AgentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Agent

    organizer = factory.SubFactory(OrganizerUserFactory)
    user = factory.SubFactory(UserFactory)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    title = factory.fuzzy.FuzzyText(length=10)


class LeadsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Lead

    first_name = fake.first_name()
    last_name = fake.last_name()
    age = fake.random_int(min=2, max=2)
    organizer = factory.SubFactory(OrganizerUserFactory)
    agent = factory.SubFactory(AgentFactory)
    category = factory.SubFactory(CategoryFactory)
    description = fake.sentence(nb_words=5)
    phone_number = fake.phone_number()
    email = fake.email()
    date_added = "2021-09-04T22:14:18Z"
