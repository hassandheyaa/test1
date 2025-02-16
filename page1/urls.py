# بعد انشاء هذا الملف. يمكن من خلاله تنظيم استرداد الدول بناءا على نهاية الرباظ كالذي يحمل نهاية معرفة مسبقا كاسماء الصفحات او نهاية متغيرة كاسماء الافلام او المعرفات
from django.urls import path
from .views import *
urlpatterns = [
    # 
    path("db",dbview),
    path("showone",showOne),
    path("deleteone",deleteOne),
    path("addtable",addTable),
    path("updataTable",updataTable),
    path("costumSelect",costumSelect),
    path("uploadFiles",uploadFiles),
    # هذا الذي يكون فراغ او الذي لا يحمل ايندبوينت
    path("",main),
    # هذه التي يحتوي على نهايات المسار المعينة مسبقا
    path('section1',section1),
    path('section2',section2),
    # هذا التي يحتوي على ايندبوينت متغير ويمكن تمريره عبر متغير على الدالة 
    path("<str:endPoint>",costumSection),
]
