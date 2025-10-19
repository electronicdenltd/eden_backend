from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password

User = get_user_model()

pin_validator = RegexValidator(regex=r'^\d{4}$', message='Pin must be a 4-digit number.')

# Create your models here.
class Building(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
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
    
    
class BuildingDoors(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    door_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    locked = models.BooleanField(default=False)
    pin = models.CharField(max_length=128, null=True, blank=True)
    has_pin = models.BooleanField(default=False)

    def __str__(self):
        return self.door_name
    
    def set_pin(self, raw_pin):
        self.pin = make_password(raw_pin)
        self.has_pin = True
        self.save()
        
    def _check_pin(self, pin):
        return check_password(pin, self.pin)
    
    
    def unlock(self, pin):
        if self.has_pin:
            if self._check_pin(pin):
                self.locked = False
                self.save()
                return True
            else:
                return False
        elif not self.has_pin:
            self.locked = False
            self.save()
            return True
            
        
    def lock(self):
        self.locked = True
        self.save()
        
