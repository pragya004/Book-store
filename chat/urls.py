from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("direct/", views.chat_index_direct, name="chat_index_direct_url"),
    path("group/", views.chat_index_group, name="chat_index_group_url"),
    path("group/create/", views.chat_create_group, name="chat_create_group"),
    path("api/direct/conversation/", views.get_direct_conversation, name="direct_conversation_url"),
    path("api/group/adduser/", views.adduser_to_group, name="adduser_to_group_url"),
    path("api/messages/", views.messages, name="messages_url"),
    path("api/fetch/users/", views.get_users, name="users_url"),
    path("api/fetch/groups/", views.get_groups, name="groups_url"),
]

