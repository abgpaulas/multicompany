from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from apps.job_orders.models import Product
from apps.accounts.models import User


class Command(BaseCommand):
    help = 'Assign job order approval permissions to users and groups'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user-email',
            type=str,
            help='Email of user to assign permission to',
        )
        parser.add_argument(
            '--group-name',
            type=str,
            help='Name of group to assign permission to',
        )
        parser.add_argument(
            '--all-staff',
            action='store_true',
            help='Assign permission to all staff users',
        )
        parser.add_argument(
            '--create-approver-group',
            action='store_true',
            help='Create a Job Order Approvers group with approval permissions',
        )

    def handle(self, *args, **options):
        # Get the permission
        try:
            permission = Permission.objects.get(
                codename='can_approve_jobs',
                content_type=ContentType.objects.get_for_model(Product)
            )
            self.stdout.write(f'Found permission: {permission}')
        except Permission.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Permission "can_approve_jobs" not found')
            )
            return

        # Create approver group if requested
        if options['create_approver_group']:
            group, created = Group.objects.get_or_create(
                name='Job Order Approvers',
                defaults={'name': 'Job Order Approvers'}
            )
            group.permissions.add(permission)
            if created:
                self.stdout.write(
                    self.style.SUCCESS('Created "Job Order Approvers" group')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS('Updated "Job Order Approvers" group')
                )

        # Assign to specific user
        if options['user_email']:
            try:
                user = User.objects.get(email=options['user_email'])
                user.user_permissions.add(permission)
                self.stdout.write(
                    self.style.SUCCESS(f'Assigned permission to user: {user.email}')
                )
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'User with email {options["user_email"]} not found')
                )

        # Assign to specific group
        if options['group_name']:
            try:
                group = Group.objects.get(name=options['group_name'])
                group.permissions.add(permission)
                self.stdout.write(
                    self.style.SUCCESS(f'Assigned permission to group: {group.name}')
                )
            except Group.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Group "{options["group_name"]}" not found')
                )

        # Assign to all staff users
        if options['all_staff']:
            staff_users = User.objects.filter(is_staff=True)
            count = 0
            for user in staff_users:
                user.user_permissions.add(permission)
                count += 1
            self.stdout.write(
                self.style.SUCCESS(f'Assigned permission to {count} staff users')
            )

        # Show current users with permission
        users_with_permission = User.objects.filter(
            user_permissions=permission
        ).values_list('email', flat=True)
        
        groups_with_permission = Group.objects.filter(
            permissions=permission
        ).values_list('name', flat=True)

        self.stdout.write('\nCurrent users with approval permission:')
        for email in users_with_permission:
            self.stdout.write(f'  - {email}')

        self.stdout.write('\nCurrent groups with approval permission:')
        for name in groups_with_permission:
            self.stdout.write(f'  - {name}')
