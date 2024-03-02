import datetime
import random

import factory
from django.utils import timezone

from accounts.factories import UserFactory
from meetings.models import Meeting
from projects.factories import ProjectFactory


class MeetingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Meeting

    project = factory.SubFactory(ProjectFactory)
    title = factory.Faker("sentence", nb_words=4)
    scheduled_time = factory.Faker("future_datetime", tzinfo=datetime.timezone.utc)
    duration = factory.LazyFunction(
        lambda: random.randint(30, 180)
    )  # Duration in minutes
    agenda = factory.Faker("text")
    notes = factory.Faker("text")
    outcomes = factory.Faker("text")
    location = factory.Faker("address")
    created_by = factory.SubFactory(UserFactory)
    created_at = factory.LazyFunction(timezone.now)
    access_level = factory.Iterator(["read", "write", "edit"])

    @factory.post_generation
    def participants(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for participant in extracted:
                self.participants.add(participant)

    @factory.post_generation
    def shared_with(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for user in extracted:
                self.shared_with.add(user)
