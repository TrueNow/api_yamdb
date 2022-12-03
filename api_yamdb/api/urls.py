from django.urls import include, path
from rest_framework.routers import SimpleRouter

# from api.views import

app_name = 'api'

router_v1 = SimpleRouter()

urlpatterns = [
    path('', include(router_v1.urls)),
]
