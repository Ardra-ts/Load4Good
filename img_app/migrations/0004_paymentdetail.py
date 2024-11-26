# Generated by Django 5.1.3 on 2024-11-24 14:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('img_app', '0003_remove_fileupload_file_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payer_id', models.CharField(max_length=255)),
                ('payment_status', models.CharField(default='Success', max_length=50)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('pic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='img_app.fileupload')),
            ],
        ),
    ]