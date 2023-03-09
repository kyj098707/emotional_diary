from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.urls import path, include
from django.shortcuts import render
from django.views.generic import TemplateView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/",include("accounts.urls")),
    path("",include("diaryapp.urls")),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)