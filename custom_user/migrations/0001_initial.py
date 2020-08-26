# Generated by Django 3.1 on 2020-08-25 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="EmailRecord",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("subject", models.CharField(max_length=220)),
                ("message", models.TextField()),
                (
                    "no_of_user",
                    models.PositiveSmallIntegerField(
                        help_text="The number of users as at the time this mail was sent"
                    ),
                ),
                ("updateted_date", models.DateTimeField(auto_now=True)),
                ("created_date", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["-created_date"],
            },
        ),
    ]
