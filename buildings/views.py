from django.shortcuts import render, get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

#import requests

from eden_backend.permissions import IsOwner
from .models import Building, BuildingDoors, BuildingDoorAction
from .serializers import BuildingSerializer, BuildingDoorsSerializer, BuildingDoorUnlockSerializer, BuildingDoorActionSerializer

class BuildingAddView(generics.CreateAPIView):
    serializer_class = BuildingSerializer
    queryset = Building.objects.all()
    
    def perform_create(self, serializer):
        building = serializer.save()
        building.owner = self.request.user
        building.save()

class BuildingListView(generics.ListAPIView):
    serializer_class = BuildingSerializer
    queryset = Building.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        return Building.objects.filter(owner=self.request.user)

class BuildingRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = BuildingSerializer
    queryset = Building.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = "id"
    
    def get_object(self):
        building = Building.objects.get(id=self.kwargs["id"])
        self.check_object_permissions(self.request, building)
        return building
    

class BuildingDeleteView(generics.DestroyAPIView):
    serializer_class = BuildingSerializer
    queryset = Building.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = "id"
    
class BuildingDoorVerifyView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, uid):
        #data = request.data
        response = BuildingDoors.objects.filter(uid=uid).exists()
        if response:
            return Response({"success": True, "message": "Door exists"}, status=status.HTTP_200_OK)
        else:
            return Response({"success": False, "message": "Door does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            
        #return Response({"success": True}, status=status.HTTP_200_OK)
        #return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)
    

class BuildingDoorsRegisterView(generics.CreateAPIView):
    serializer_class = BuildingDoorsSerializer
    queryset = BuildingDoors.objects.all()
    permission_classes = [AllowAny]
    
    def perform_create(self, serializer):
        #if ~self.request.user.is_superuser:
        #    raise Exception("You are not permitted to register doors")
        serializer.save(building=None,is_assigned=False)
    
    # def perform_create(self, serializer):
    #     building = serializer.validated_data['building']
    #     if building.owner != self.request.user:
    #         raise Exception("You are not the owner of this building")
    #     serializer.save()
        
        
class BuildingDoorsAssignView(generics.UpdateAPIView):
    serializer_class = BuildingDoorsSerializer
    queryset = BuildingDoors.objects.all()
    
    def get_object(self):
        door = BuildingDoors.objects.get(id=self.request.data["uid"])
        if door.check_pin(self.request.data['pin']):
            door.building = self.request.data["building"]
            door.door_name = self.request.data["door_name"]
            door.description = self.request.data["description"]
            door.is_assigned = True
            door.save()
            return door
        else:
            raise Exception("Invalid pin or uid")
    
class BuildingDoorsListView(generics.ListAPIView):
    serializer_class = BuildingDoorsSerializer
    queryset = BuildingDoors.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        return BuildingDoors.objects.filter(building = self.kwargs['building'])
    
class BuildingDoorsRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = BuildingDoorsSerializer
    queryset = BuildingDoors.objects.all()
    
    
    def get_object(self):
        door = BuildingDoors.objects.get(id=self.kwargs["uid"])
        self.check_object_permissions(self.request, door)
        return door
    
class BuildingDoorsDeleteView(generics.DestroyAPIView):
    serializer_class = BuildingDoorsSerializer
    queryset = BuildingDoors.objects.all()
    lookup_field = "id"
    
    
class BuildingDoorActionView(generics.GenericAPIView):
    serializer_class = BuildingDoorUnlockSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        door_id = serializer.validated_data['door_id']
        pin = serializer.validated_data['pin']
        action = serializer.validated_data['action']
        
        # door = get_object_or_404(BuildingDoors, id=door_id)
        # if door.building.owner != request.user:
        #     raise PermissionDenied("You are not the owner of this door")
        
        # if action not in ['lock', 'unlock']:
        #     raise PermissionDenied("Invalid action")
        
        # if action == 'unlock':
        #     success = door.unlock(pin)
        # else:
        #     door.lock()
        #     success = True
        
        # if not success:
        #     return Response({"error": "Invalid pin"}, status=status.HTTP_403_FORBIDDEN)
        
### Implement communication with esp32
        #requests.post(f"http://192.168.4.1/{action}", json={"action": action})
        # try:
        #     requests.post(ESP32_API_URL, json={"door_id": door.id, "action": action})
        # except Exception:
        #     return Response({"warning": "Door state updated but ESP not reached."})

        # return Response(
        #     {"status": f"Door {action}ed successfully"},
        #     status=status.HTTP_200_OK
        # )

        return Response({"success": "Door action successful."}, status=status.HTTP_200_OK)
        
        
class BuildingDoorActionListView(generics.ListAPIView):
    serializer_class = BuildingDoorActionSerializer
    queryset = BuildingDoorAction.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        return BuildingDoorAction.objects.filter(building = self.kwargs['building'])