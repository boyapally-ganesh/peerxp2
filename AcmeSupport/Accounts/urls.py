from django.urls import path
from Accounts.views import login_view, home, logout_view, create_user, create_ticket,create_department, edit_department,view_all_users,view_departments,delete_department,retrieve_all_tickets, delete_ticket
from django.contrib.auth import views as auth_views
from .views import create_ticket

from . import views
app_name = 'Accounts'
urlpatterns = [
    path('login/', login_view, name='login'),
    path('home/', home, name='home'),
    path('logout/', logout_view, name='logout'),
    path('create-user/', create_user, name='create_user'), 
    path('create-ticket/', create_ticket, name='create_ticket'),
    path('create-department/', create_department, name='create-department'),
    path('edit-department/<int:department_id>/', edit_department, name='edit-department'),
    path('view_all_users/', view_all_users, name='view_all_users'),
    path('view_departments/', views.view_departments, name='view_departments'),
    path('delete_department/<int:department_id>/',delete_department, name='delete_department'),
    path('retrieve_all_tickets/', retrieve_all_tickets, name='retrieve_all_tickets'),
    path('delete-ticket/<int:ticket_id>', delete_ticket, name='delete_ticket'),
    
    # path('ticket_page/', ticket, name='ticket_page'),
]