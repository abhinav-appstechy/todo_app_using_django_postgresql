from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name="homepage"),
    path('about-us/', views.about_us, name="about_us"),
    path('contact-us/', views.contact_us, name="contact_us"),
    path('add-todo/', views.add_todo, name="add_new_todo"),
    path('add-new-todo/', views.add_new_todo_logic, name="add_new_todo_logic"),
    path('update-todo/<int:id>/', views.update_todo_page, name="update_todo_page"),
    path('update-todo-logic/', views.update_todo_logic, name="update_todo_logic"),
    path('todo-change-status', views.change_status, name="todo_change_status"),
    path('delete-todo', views.delete_todo , name="delete_todo"),
    path('logout', views.logout_view , name="logout")

    
]
