from django.db import models

class Achievement(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
