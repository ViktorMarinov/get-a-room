from __future__ import unicode_literals

from accounts.models import User

from django.db import migrations
from django.contrib.auth.models import Group


def add_groups(apps, schema_editor):

    teachers, created_teachers = Group.objects.get_or_create(name='teachers')
    students, created_students = Group.objects.get_or_create(name='students')
    user = User.objects.create_user(
        username='admin',
        password='admin',
        email='admin@fakemail.com'
    )
    user.is_superuser = True
    user.is_staff = True
    user.save()

    teachers.user_set.add(user)
    teachers.save()
    students.save()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial')
    ]

    operations = [
        migrations.RunPython(add_groups)
    ]
