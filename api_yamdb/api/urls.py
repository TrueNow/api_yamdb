from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import signup_view, user_token_view, CategoryViewSet, GenreViewSet, TitleViewSet

app_name = 'api'

router_v1 = SimpleRouter()
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('categories', CategoryViewSet, basename='categories')

v1_auth_patterns = [
    path('signup/', signup_view),
    path('token/', user_token_view),
]

urlpatterns = [
    path('v1/auth/', include(v1_auth_patterns)),
    path('v1/', include(router_v1.urls)),
]
