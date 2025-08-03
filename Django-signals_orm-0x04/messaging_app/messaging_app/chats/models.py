# chats/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass  # Extend this later if needed (e.g., add profile picture, bio, etc.)
