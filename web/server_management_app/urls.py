from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("user_create", views.user_create, name="user_create"),
    path("server_create", views.server_create, name="server_create"),
    path("image_create", views.image_create, name="image_create"),
    path("user_delete/<int:user_id>", views.user_delete, name="user_delete"),
    path("image_delete/<int:image_id>", views.image_delete, name="image_delete"),
    path("image_update_list", views.image_update_list, name="image_update_list"),
    # path("<int:pk>/update/", views.todo_update, name="todo_update"),
    # path("<int:pk>/delete/", views.todo_delete, name="todo_delete"),
]
