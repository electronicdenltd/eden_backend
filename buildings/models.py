from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import get_user_model

User = get_user_model()

pin_validator = RegexValidator(regex=r'^\d{4}$', message='Pin must be a 4-digit number.')
# Create your models here.
class Building(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    locked = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def unlock(self):
        self.locked = False
        self.save()
        
    def lock(self):
        self.locked = True
        self.save()
    
    
class Doors(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    door_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    locked = models.BooleanField(default=False)
    pin = models.Charfield(max_length=4, null=True, blank=True, validators=[pin_validator])

    def __str__(self):
        return self.door_name
    
    def has_pin(self):
        return self.pin is not None
    
    def unlock(self):
        self.locked = False
        self.save()
        
    def lock(self):
        self.locked = True
        self.save()
        
