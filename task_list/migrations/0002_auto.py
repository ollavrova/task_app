from django.core.management import call_command
from django.db import migrations


def loadfixture(apps, schema_editor):
    call_command('loaddata', 'initial.json')


class Migration(migrations.Migration):

    dependencies = [
        ('task_list', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(loadfixture),
    ]
