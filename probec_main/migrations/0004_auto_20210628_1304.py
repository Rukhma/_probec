# Generated by Django 3.1.4 on 2021-06-28 08:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('probec_main', '0003_auto_20210627_1104'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['sales']},
        ),
    ]
