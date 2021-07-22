from budget_app.settings import MEDIA_ROOT
from django import urls
from django import contrib
from django.contrib import admin
from django.urls import path, include
from.views import home_page
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home_page, name="homepage"),
    path("", include('accounts.urls')),
    path("", include('budget.urls'))
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
