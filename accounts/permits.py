from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


def create_groups_with_permissions():
    # Create or get the groups
    mentors_group, _ = Group.objects.get_or_create(name="Mentors")
    founders_group, _ = Group.objects.get_or_create(name="Founders")

    # Get the permissions
    create_permission = Permission.objects.get(codename="create_project")
    edit_permission = Permission.objects.get(codename="edit_project")
    add_member_permission = Permission.objects.get(codename="add_member")

    # Assign permissions to groups
    mentors_group.permissions.set(
        [create_permission, edit_permission]
    )  # Mentors can create and edit
    founders_group.permissions.set(
        [create_permission, add_member_permission]
    )  # Founders can create and add members

    mentors_group.save()
    founders_group.save()


# # Call this function to set up your groups and permissions
# create_groups_with_permissions()


# user = User.objects.get(username='new_member')
# group = Group.objects.get(name='Mentors')  # Or 'Founders', depending on the role
# user.groups.add(group)

# from django.contrib.auth.decorators import permission_required

# For creating and editing projects:
# @permission_required('app.create_project')
# def create_project(request):
#     # Implementation

# @permission_required('app.edit_project')
# def edit_project(request, project_id):
#     # Implementation

# For adding new members (only for Founders):
# @permission_required('app.add_member')
# def add_member(request):
#     # Implementation
