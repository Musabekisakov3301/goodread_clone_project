# Generated by Django 4.2.3 on 2023-07-07 12:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(default='default_profile_picture.jpg', upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg', 'heic', 'heif'])]),
        ),
    ]
