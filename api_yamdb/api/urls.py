from django.urls import path, include

from .views import signup_view, user_token_view

v1_auth_patterns = [
    path('signup/', signup_view),
    path('token/', user_token_view),
]

urlpatterns = [
    path('v1/auth/', include(v1_auth_patterns)),
]
