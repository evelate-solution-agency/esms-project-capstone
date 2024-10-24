from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from web_project.views import SystemView

urlpatterns = [
    path("admin/", admin.site.urls),
    # starter urls
    path("", include("apps.core.urls")),
    # auth urls
    path("auth/", include("apps.authentication.urls")),
    path("", include("apps.pages.urls")),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)

handler404 = SystemView.as_view(template_name="pages_misc_error.html", status=404)
handler403 = SystemView.as_view(template_name="pages_misc_not_authorized.html", status=403)
handler400 = SystemView.as_view(template_name="pages_misc_error.html", status=400)
handler500 = SystemView.as_view(template_name="pages_misc_error.html", status=500)
