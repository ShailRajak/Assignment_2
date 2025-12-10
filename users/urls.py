from django.urls import path
from .views import get_users, create_user, update_user_partial, delete_users

urlpatterns = [
    path('users/', get_users),
    path('create-user/', create_user),
    path('users/<int:id>/patch/', update_user_partial),
    path('users/delete/', delete_users),
]