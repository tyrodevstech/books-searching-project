# Generated by Django 4.1.7 on 2023-05-16 16:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app_book", "0003_blogmodel_alter_authormodel_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="reviewmodel",
            options={
                "ordering": ["-id"],
                "verbose_name": "Review",
                "verbose_name_plural": "Reviews",
            },
        ),
        migrations.AddField(
            model_name="blogmodel",
            name="banner",
            field=models.ImageField(
                blank=True, null=True, upload_to="banner-image/%Y/%d/%b"
            ),
        ),
    ]