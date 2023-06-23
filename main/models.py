from django.db import models


class Word(models.Model):
    word = models.CharField(max_length=127, verbose_name='word')
    frequency = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.word} : {self.frequency}'
