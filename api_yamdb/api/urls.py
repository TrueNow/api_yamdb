from django.urls import include, path 
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from .views import CommentViewSet, ReviewViewSet

from .views import signup_view, user_token_view

app_name = 'api'

router_v1 = DefaultRouter()
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
