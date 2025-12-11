from rest_framework import serializers

from .models import Building, BuildingDoors, BuildingDoorAction

class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ['id', 'owner', 'name', 'address', 'description', 'locked']
        
class BuildingDoorsSerializer(serializers.ModelSerializer):
    #Take the building id from the request and use it to find the building object
    building_id = serializers.IntegerField(write_only=True, required = True)
    pin = serializers.CharField(write_only=True, required = True)
    #has_pin = serializers.ReadOnlyField() #was initially added but removed as
    #it was a requirement to set pin
    locked = serializers.ReadOnlyField()
    class Meta:
        model = BuildingDoors
        fields = ['uid', 'building_id', 'door_name', 'description', 'locked', 'pin']
        
    def create(self, validated_data):
        pin = validated_data.pop('pin', None)
        door = BuildingDoors.objects.create(**validated_data)
        if pin:
            door.set_pin(pin)
        return door
    

class BuildingDoorUnlockSerializer(serializers.Serializer):
    pin = serializers.CharField()
    door_id = serializers.IntegerField()
    action = serializers.CharField(max_length=10)
    
    class Meta:
        fields = ['pin', 'door_uid', 'action']


class BuildingDoorActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingDoorAction
        fields = ['id', 'house', 'door', 'user', 'action', 'timestamp']       
        
