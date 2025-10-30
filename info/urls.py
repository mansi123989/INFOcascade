from django.urls import path
from info import views
app_name = 'info' 
urlpatterns = [

    path('', views.home, name='home'),   
    path('home', views.home, name='home'),
    path('login', views.login, name='login'),
    path('form', views.form ,name='form'),
    path('INFOadmin', views.admin_panel, name='admin_panel'),
    path('notice', views.notice_list, name='notice_list'),
    path('logout', views.logout_view, name='logout'),
    path('search', views.notice_search, name='notice_search'),
    path('chat/messages/', views.chat_messages, name='chat_messages'),
    path('chat/send/', views.send_message, name='send_message'),
    path('chat/delete/<int:msg_id>/', views.delete_message, name='delete_message'),
]