from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet

app_name = 'api'

router_v1 = SimpleRouter()
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('categories', CategoryViewSet, basename='categories')


urlpatterns = [
    path('', include(router_v1.urls)),
]
