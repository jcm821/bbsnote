# Generated by Django 4.1.7 on 2023-03-22 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bbsnote", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="board",
            name="update_date",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="board",
            name="create_date",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
