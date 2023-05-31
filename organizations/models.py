from django.db import models


# Create your models here.
class Organization(models.Model):
    owner = models.ForeignKey('users.CustomUser', null=True, blank=True, on_delete=models.CASCADE,
                              related_name='organizations')
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=400, null=True, blank=True)
    address = models.CharField(max_length=400)
    postcode = models.CharField(max_length=6)

    def __str__(self):
        return self.title
