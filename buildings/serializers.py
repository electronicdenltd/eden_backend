from rest_framework import serializers

from .models import Building, BuildingDoors

class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ['id', 'owner', 'name', 'address', 'description', 'locked']
        
class BuildingDoorsSerializer(serializers.ModelSerializer):
    pin = serializers.CharField(write_only=True, required = False)
    has_pin = serializers.ReadOnlyField()
    locked = serializers.ReadOnlyField()
    class Meta:
        model = BuildingDoors
        fields = ['id', 'building', 'door_name', 'description', 'locked', 'pin', 'has_pin']
        
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
        fields = ['pin', 'door_id', 'action']