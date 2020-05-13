from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from chat.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='index'),
    path('chat', views.chat_view, name='chats'),
    path('chat/<int:sender>/<int:receiver>', views.message_view, name='chat'),
    path('api/messages/<int:sender>/<int:receiver>', views.message_list, name='message-detail'),
    path('api/messages', views.message_list, name='message-list'),
    path('api/users/<int:pk>', views.user_list, name='user-detail'),
    path('api/users', views.user_list, name='user-list'),
    path('logout', LogoutView.as_view(next_page='index'), name='logout'),
    path('register', views.register_view, name='register'),
    path('update_profile/<str:u>/',update_profile),
    path('ForgotPasswordUser/', ForgotPasswordUser),
    path('findotp/', findotp),
    path('Registration/', Registration),
    path('Login/', Login),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
