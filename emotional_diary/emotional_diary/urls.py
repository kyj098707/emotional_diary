from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth", include("rest_framework.urls")),
    
    #========================================================
    #========================================================
    #========================================================
    
    path("aivlary/", include("accounts.urls")),
    path("aivlary/",include("diaryapp.urls")),
    
    
    
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)