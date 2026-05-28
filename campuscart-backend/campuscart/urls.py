# campuscart/urls.py
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from push.views import service_worker
from products.views import product_redirect_view
import os

FRONTEND_DIR = os.path.join(settings.BASE_DIR, 'frontend')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("products/<int:pk>/", product_redirect_view, name="product-view"),
    path("api/v1/", include(("campuscart.api_urls", "api"), namespace="v1")),
    path("api/v1/payments/", include("payments.urls")),
    path("sw.js", service_worker, name="service-worker"),
]

# Serve media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve frontend HTML/JS/CSS (must be last)
urlpatterns += [
    re_path(r"^(?P<path>.*)$", serve, {"document_root": FRONTEND_DIR, "show_indexes": False}),
]
