from django.db import models


class Words(models.Model):
    lang = ['eng', 'rus', 'jap']

    word = models.CharField()
