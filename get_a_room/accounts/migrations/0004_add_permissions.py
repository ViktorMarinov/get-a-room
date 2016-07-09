from __future__ import unicode_literals

from django.db import migrations
from django.contrib.auth.models import Permission, Group


def add_permissions(apps, schema_editor, with_create_permissions=True):

    teachers = Group.objects.get(name='teachers')
    students = Group.objects.get(name='students')
    try:
        can_add_booking = Permission.objects.get(name='Can add booking')
        can_delete_booking = Permission.objects.get(name='Can delete booking')
        can_change_booking = Permission.objects.get(name='Can change booking')

        teachers.permissions.add(
            can_add_booking,
            can_delete_booking,
            can_change_booking,
        )
    except Permission.DoesNotExist:
        if with_create_permissions:
            # Manually run create_permissions
            from django.contrib.auth.management import create_permissions
            assert not getattr(apps, 'models_module', None)
            apps.models_module = True
            create_permissions(apps, verbosity=0)
            apps.models_module = None
            return add_permissions(
                apps, schema_editor, with_create_permissions=False)
        else:
            raise

    teachers.save()
    students.save()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20160704_1230'),
        ('rooms', '0003_booking')
    ]

    operations = [
        migrations.RunPython(add_permissions)
    ]
