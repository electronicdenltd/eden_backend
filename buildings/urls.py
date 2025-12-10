from django.urls import path

from .views import BuildingAddView, BuildingListView, BuildingRetrieveUpdateView, BuildingDeleteView, BuildingDoorsListView, BuildingDoorsRetrieveUpdateView, BuildingDoorsDeleteView, BuildingDoorsRegisterView, BuildingDoorActionView, BuildingDoorActionListView, BuildingDoorsAssignView, BuildingDoorVerifyView

urlpatterns = [
    path('door-action/', BuildingDoorActionView.as_view(), name='door-action'),
    
    path('add-building/', BuildingAddView.as_view(), name='add-building'),
    path('list-buildings/', BuildingListView.as_view(), name='list-buildings'),
    path('update-building/<int:id>/', BuildingRetrieveUpdateView.as_view(), name='update-building'),
    path('delete-building/<int:id>/', BuildingDeleteView.as_view(), name='delete-building'),
    
    path('list-doors/<int:building>/', BuildingDoorsListView.as_view(), name='list-doors'),
    path('update-door/<int:id>/', BuildingDoorsRetrieveUpdateView.as_view(), name='update-door'),
    path('register-door/', BuildingDoorsRegisterView.as_view(), name='add-door'),
    path('delete-door/<int:id>/', BuildingDoorsDeleteView.as_view(), name='delete-door'),
    path('assign-door/', BuildingDoorsAssignView.as_view(), name='assign-door'),
    path('verify-door/<str:uid>/', BuildingDoorVerifyView.as_view(), name='verify-door'),
    
    path('list-actions/<int:building>/',BuildingDoorActionListView.as_view(), name='list-actions')
]