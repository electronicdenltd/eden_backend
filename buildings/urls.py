from django.urls import path

from .views import BuildingAddView, BuildingListView, BuildingRetrieveUpdateView, BuildingDeleteView, BuildingDoorsListView, BuildingDoorsRetrieveUpdateView, BuildingDoorsDeleteView, BuildingDoorsAddView, BuildingDoorActionView

urlpatterns = [
    path('door-action/', BuildingDoorActionView.as_view(), name='door-action'),
    
    path('add-building/', BuildingAddView.as_view(), name='add-building'),
    path('list-buildings/', BuildingListView.as_view(), name='list-buildings'),
    path('update-building/<int:id>/', BuildingRetrieveUpdateView.as_view(), name='update-building'),
    path('delete-building/<int:id>/', BuildingDeleteView.as_view(), name='delete-building'),
    
    path('list-doors/<int:building>/', BuildingDoorsListView.as_view(), name='list-doors'),
    path('update-door/<int:id>/', BuildingDoorsRetrieveUpdateView.as_view(), name='update-door'),
    path('add-door/<int:building>/', BuildingDoorsAddView.as_view(), name='add-door'),
    path('delete-door/<int:id>/', BuildingDoorsDeleteView.as_view(), name='delete-door'),
    
]