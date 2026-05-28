# campuscart/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from push.views import service_worker
from products.views import product_redirect_view  # 🆕 import

urlpatterns = [
    path("admin/", admin.site.urls),
    path("products/<int:pk>/", product_redirect_view, name="product-view"),
    path("api/v1/", include(("campuscart.api_urls", "api"), namespace="v1")),
    path("sw.js", service_worker, name="service-worker"),
    path("api/v1/payments/", include("payments.urls")),  # ✅ keep this
]

# serve media in dev
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve frontend static files in production (Render)
from django.views.static import serve
from django.urls import re_path
import os

FRONTEND_DIR = os.path.join(settings.BASE_DIR, 'frontend')

urlpatterns += [
    re_path(r'^(?!api/|admin/|static/|media/|sw.js).*$',
        serve,
        {
            'document_root': FRONTEND_DIR,
            'show_indexes': False,
        }
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
