from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import HttpResponseRedirect


# def redirect_to_frontend(request):
#     return HttpResponseRedirect("http://localhost:5173")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
   # path('', redirect_to_frontend, name='home'),
   
]