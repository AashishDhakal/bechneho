# Generated by Django 3.0.4 on 2020-03-30 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_message_attachment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.TextField(blank=True),
        ),
    ]
