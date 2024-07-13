from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("user_create", views.user_create, name="user_create"),
    path("server_create", views.server_create, name="server_create"),
    # path("<int:pk>/update/", views.todo_update, name="todo_update"),
    # path("<int:pk>/delete/", views.todo_delete, name="todo_delete"),
]
