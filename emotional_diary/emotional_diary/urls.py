from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.urls import path, include
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/",include("accounts.urls")),
    path("api-auth", include("rest_framework.urls")),
    path("",include("diaryapp.urls")),

    path('token/', TokenObtainPairView.as_view(),name="token_obtain_pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('token/verify/', TokenVerifyView.as_view(), name="token_verify"),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)