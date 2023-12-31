import factory
from django.utils import timezone

from accounts.factories import UserFactory
from documents.models import Document


class DocumentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Document

    title = factory.Faker('sentence', nb_words=5)
    content = factory.Faker('text')
    document_type = factory.Iterator(['Contract', 'Report', 'Plan'])  # Add more types as needed
    created_by = factory.SubFactory(UserFactory)
    creation_date = factory.Faker('date')
    # last_modified = factory.Faker('date_time')
    last_modified = factory.LazyFunction(timezone.now)
    status = factory.Iterator(['Draft', 'Final', 'Archived'])  # Add more statuses as needed
    is_template = factory.Faker('boolean')
    access_level = factory.Iterator(['read', 'write', 'edit'])
