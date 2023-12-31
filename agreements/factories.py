import factory
from django.utils import timezone

from accounts.factories import UserFactory
from agreements.models import Agreement, Amendment, DigitalSignature
from projects.factories import ProjectFactory


class AgreementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Agreement

    title = factory.Faker('sentence', nb_words=4)
    content = factory.Faker('text')
    status = factory.Iterator(['Draft', 'Pending', 'Signed'])  # Add more statuses as needed
    created_by = factory.SubFactory(UserFactory)
    project = factory.SubFactory(ProjectFactory)  # Assuming you have a ProjectFactory
    effective_date = factory.Faker('date')
    expiration_date = factory.Faker('date')
    agreement_type = factory.Iterator(['NDA', 'Service Contract'])  # Add more types as needed
    # last_amended_date = factory.Faker('date_time')
    last_amended_date = factory.LazyFunction(timezone.now)


class AmendmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Amendment

    agreement = factory.SubFactory(AgreementFactory)
    description = factory.Faker('text')
    updated_by = factory.SubFactory(UserFactory)
    # updated_at = factory.Faker('date_time')
    updated_at = factory.LazyFunction(timezone.now)
    version = factory.Sequence(lambda n: n)


class DigitalSignatureFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DigitalSignature

    amendment = factory.SubFactory(AmendmentFactory)
    signee = factory.SubFactory(UserFactory)
    # signed_at = factory.Faker('date_time')
    signed_at = factory.LazyFunction(timezone.now)
    signature = factory.django.ImageField(color='blue')  # Adjust as needed
