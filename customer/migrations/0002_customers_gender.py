# Generated by Django 4.2.2 on 2023-06-20 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customers',
            name='gender',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
