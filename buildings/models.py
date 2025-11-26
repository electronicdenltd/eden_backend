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
    uid = models.CharField(max_length=255, unique=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, null=True)
    door_name = models.CharField(max_length=255, default='Door')
    description = models.TextField(null=True, blank=True)
    locked = models.BooleanField(default=False)
    pin = models.CharField(max_length=128)
    has_pin = models.BooleanField(default=True)
    is_assigned = models.BooleanField(default=False)

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
        
class BuildingDoorAction(models.Model):
    class ActionChoices(models.TextChoices):
        LOCK = 'lock'
        UNLOCK = 'unlock'
    
    house = models.ForeignKey(Building, on_delete=models.CASCADE)
    door = models.ForeignKey(BuildingDoors, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=ActionChoices.choices)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} {self.action}ed {self.door.door_name} at {self.timestamp}"
    
    