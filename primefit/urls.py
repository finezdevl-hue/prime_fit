from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from primefit.admin_site import PrimeFitAdminSite
from store import views as store_views

# Use custom admin site
admin.site = PrimeFitAdminSite()

admin.site.site_header = "⚡ PRIME FIT Apparels Admin"
admin.site.site_title = "PRIME FIT Admin"
admin.site.index_title = "Welcome to PRIME FIT Control Panel"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-panel/', store_views.admin_panel, name='admin_panel'),
    path('', include('store.urls')),
]

# Serve media files only in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

