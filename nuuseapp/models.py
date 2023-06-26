from django.db import models

class QA(models.Model):
    question = models.TextField()
    answer = models.TextField()

class QA_en(models.Model):
    question = models.TextField()
    answer = models.TextField()