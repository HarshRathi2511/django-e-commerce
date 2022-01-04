from django.db import models
from django.contrib.auth.models import User

#Create the address model here 
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    apartment = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pin = models.PositiveIntegerField()
    # default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name_plural = 'Addresses'


# Create the profile model here 


