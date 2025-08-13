from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/swagger/', SpectacularSwaggerView.as_view(), name='swagger-ui'),
    path('docs/redoc/', SpectacularRedocView.as_view(), name='redoc'),
    path('users/', include('account.api.urls')),
    path('regions/', include('regions.api.urls')),
]
