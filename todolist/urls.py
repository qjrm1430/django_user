from django.urls import path

from .views import delete_todo, get_todolist, update_todo

urlpatterns = [
    path("", get_todolist, name="todolist-index"),
    path("delete-todo/<str:title>", delete_todo, name="delete-todo"),
    path("update-todo/<str:title>", update_todo, name="update-todo"),
]
