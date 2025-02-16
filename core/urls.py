# هنا نسطيع توجيه المستخدم على ملف "urls" بناءا على المسار. بعد رابط الخادم"دومين"
from django.contrib import admin
from django.urls import path,include

from core import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # مثلا هذا يقوم بتوجيه المستخدم على الصحفة page1
    path("page1/", include('page1.urls'))
]
if settings.DEBUG:
    urlpatterns += static(settings.IMAGE_URL, document_root=settings.IMAGE_ROOT)