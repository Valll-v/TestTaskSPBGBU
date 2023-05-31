from django.db import models


# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=400, null=True, blank=True)
    organizations = models.ManyToManyField('organizations.Organization')
    image = models.FileField(upload_to='images/', null=True, blank=True)
    date = models.DateField()
