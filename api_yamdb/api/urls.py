from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet, SignUpViewSet, GenreViewSet, TitleViewSet,
    CommentViewSet, ReviewViewSet, get_jwt_token, UserViewSet
)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment'
)
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('users', UserViewSet, basename='users')
router_v1.register(
    'auth/signup', SignUpViewSet, basename='token'
)
# router_v1.register(
#     'auth/token', get_jwt_token, basename='jwt_token'
# )


v1_auth_patterns = [
    # path('signup/', signup_view),
    # path('token/', user_token_view),
]

urlpatterns = [
    path('v1/auth/token/', get_jwt_token, name='token'),
    path('v1/', include(router_v1.urls)),
]
