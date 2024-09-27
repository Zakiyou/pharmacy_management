from pharmacy_management.views.IndexView import index
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index_du_projet"),
    path("domaine/", include("domaine.urls")),
    path("categorie/", include("categories.urls")),
    path("medicaments/", include("products.urls")),
     path('stocks/', include('stocks.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
