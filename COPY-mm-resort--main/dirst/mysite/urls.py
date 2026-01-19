from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('hotel/', views.home2, name='hotel-main'),     # головна сторінка готелю
    path('booking/', views.create_booking, name='create_booking'),
    # опціонально — бронювання конкретного номера
    path('booking/<int:room_id>/', views.create_booking, name='book_specific_room'),
]