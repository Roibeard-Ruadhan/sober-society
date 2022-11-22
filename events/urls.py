from . import views
from django.urls import path


urlpatterns = [
    path('', views.EventList.as_view(), name='events'),
    path('add_event/', views.add_event, name='add-event'),
    path('post_event/<str:location>/', views.PostEvents, name='post_event'),
    path('edit_event/<int:pk>/', views.edit_event, name="edit_event"),
    path('delete_event/<int:pk>/', views.delete_event, name='delete_event'),
]
