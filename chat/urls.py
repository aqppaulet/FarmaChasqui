from django.urls import path
from .views import chat_response

urlpatterns = [path("message/", chat_response, name="chat_message")]
