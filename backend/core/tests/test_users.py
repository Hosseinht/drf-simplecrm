import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


@pytest.mark.django_db()
def test_user_cant_be_organizer_and_agent_at_the_same_time():
    with pytest.raises(ValidationError):
        user = User(
            username="a",
            email="a@gmail.com",
            password="a.123456",
            is_agent=True,
            is_organizer=True,
        )
        user.clean()
