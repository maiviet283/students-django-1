from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from students import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('students/', include('students.urls')),
    path('', views.index, name='students.index')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
