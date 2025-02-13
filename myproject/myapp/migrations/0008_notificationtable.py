# Generated by Django 5.1.2 on 2025-01-18 05:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_incomeexpensetable_category_incomeexpensetable_price_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification', models.CharField(blank=True, max_length=100, null=True)),
                ('notification_date', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.usertable')),
            ],
        ),
    ]
