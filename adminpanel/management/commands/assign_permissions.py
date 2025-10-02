# app/management/commands/assign_permissions.py
from django.core.management.base import BaseCommand
from adminpanel.models.role import Role
from adminpanel.models.permission import Permission

class Command(BaseCommand):
    help = "Assign permissions to roles"

    def handle(self, *args, **kwargs):
        # Admin gets all permissions
        admin_role = Role.objects.get(name="Admin")
        all_permissions = Permission.objects.all()
        admin_role.permissions.set(all_permissions)


        self.stdout.write(self.style.SUCCESS("Permissions assigned to roles"))
