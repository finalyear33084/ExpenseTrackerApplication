# Generated by Django 5.1.5 on 2025-02-22 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_incomeexpensetable_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incomeexpensetable',
            name='updated_at',
        ),
    ]
