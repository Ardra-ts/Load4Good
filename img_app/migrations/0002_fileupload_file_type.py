# Generated by Django 5.1.3 on 2024-11-20 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('img_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileupload',
            name='file_type',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
    ]
