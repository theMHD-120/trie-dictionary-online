from django.db import models


class Word(models.Model):
    word = models.CharField(max_length=127, verbose_name='word')
    frequency = models.PositiveIntegerField(default=0)

