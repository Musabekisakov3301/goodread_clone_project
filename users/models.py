from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(
                      default='default_profile_picture.jpg',
                      validators=[FileExtensionValidator(allowed_extensions=['jpg','png','jpeg','heic','heif','jfif'])]
                     )