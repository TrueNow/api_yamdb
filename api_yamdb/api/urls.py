from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    signup_view, user_token_view, CategoryViewSet,
    GenreViewSet, TitleViewSet, CommentViewSet, ReviewViewSet
)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register(
    r'title/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='review'
)
router_v1.register(
    r'title/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment'
)


v1_auth_patterns = [
    path('signup/', signup_view),
    path('token/', user_token_view),
]

urlpatterns = [
    path('v1/auth/', include(v1_auth_patterns)),
    path('v1/', include(router_v1.urls)),
]
