from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from models.views import StudentViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
