# Generated by Django 4.1.2 on 2022-11-07 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vendor", "0002_vendor_vendor_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vendor",
            name="vendor_slug",
            field=models.SlugField(max_length=100),
        ),
    ]
