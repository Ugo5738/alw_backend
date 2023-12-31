import random

import factory

from accounts.factories import UserFactory
from projects.models import Project

# Example realistic options for project status
PROJECT_STATUS_CHOICES = ['Planning', 'In Progress', 'Completed', 'On Hold']

# Example realistic project names
PROJECT_NAMES = [
    "Alpha Development", "Beta Integration", "Gamma Testing", "Delta Launch",
    "Epsilon Upgrade", "Zeta Migration", "Eta Analysis", "Theta Research",
    "Iota Implementation", "Kappa Optimization"
]

MILESTONES = [
    "Project Kick-off",
    "Requirements Gathering Completed",
    "First Prototype Developed",
    "User Testing Phase 1",
    "Mid-Project Review",
    "Feature Completion",
    "Beta Release",
    "Final Testing",
    "Client Approval",
    "Project Closure"
]

DELIVERABLES = [
    "Detailed Project Plan",
    "Completed Requirement Specification Document",
    "Alpha Version of the Software",
    "User Testing Report",
    "Mid-Term Project Report",
    "Fully Functional Software",
    "Beta Version for Public Testing",
    "Final Test Results",
    "Client Training Material",
    "Final Project Documentation"
]

MILESTONE_TEMPLATE = """
Milestone: {}
- Objective: {}
- Expected Completion Date: {}
- Key Deliverables: {}
"""

DELIVERABLE_TEMPLATE = """
Deliverable: {}
- Description: {}
- Due Date: {}
- Responsible Team: {}
"""

# Function to generate random budgets
def generate_random_budget():
    return round(random.uniform(1000, 100000), 2)

def generate_milestone_content():
    milestone_title = random.choice(MILESTONES)
    objective = factory.Faker('sentence', nb_words=6)
    completion_date = factory.Faker('future_date', end_date="+30d")
    key_deliverables = factory.Faker('sentence', nb_words=4)
    
    return MILESTONE_TEMPLATE.format(milestone_title, objective, completion_date, key_deliverables)

def generate_deliverable_content():
    deliverable_title = random.choice(DELIVERABLES)
    description = factory.Faker('sentence', nb_words=8)
    due_date = factory.Faker('future_date', end_date="+60d")
    responsible_team = factory.Faker('word')

    return DELIVERABLE_TEMPLATE.format(deliverable_title, description, due_date, responsible_team)

def create_milestones():
    return '\n'.join([generate_milestone_content() for _ in range(random.randint(2, 5))])

def create_deliverables():
    return '\n'.join([generate_deliverable_content() for _ in range(random.randint(2, 5))])


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    name = factory.Iterator(PROJECT_NAMES)  # Use predefined project names
    description = factory.Faker('text')
    status = factory.Iterator(PROJECT_STATUS_CHOICES)  # Use predefined status choices
    owner = factory.SubFactory(UserFactory)
    start_date = factory.Faker('past_date')  # Generates a date in the past
    end_date = factory.Faker('future_date')  # Generates a date in the future
    budget = factory.LazyFunction(generate_random_budget)  # Use your custom function for budget
    milestones = factory.LazyFunction(create_milestones)  # Generate milestones using your custom function
    deliverables = factory.LazyFunction(create_deliverables)  # Generate deliverables using your custom function

