from django.contrib.auth.models import User
from django.db import models


class Player(User):
    tokens = models.IntegerField(default=1000)
