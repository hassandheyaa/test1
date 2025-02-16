import json
from ntpath import join
import os
from random import Random, randbytes, randint
import random
import string
import uuid
from django.core import serializers
from django.http import HttpResponse,JsonResponse

from core import settings
from .models import Page1Serializer, page1
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from sql_query import *
# Create your views here.
# هذا الصفحة التي يمكن منها ارسال
#  البيانات التي تظهر للمستخدم
# هذا الدالة يعيد على الرابط التي نهايته فارغ
def main(request):
    return HttpResponse("main")
# هذه الدوال يعيد على الرباط التي له نهاية محدد مسبقا
def section1(request):
    return HttpResponse("section 1")
def section2(request):
    return HttpResponse("section 2")
# هذا الدالة يعيد على الرباط التي نهايته متغير كاسماء الافلام او المعرفات
def costumSection(request, endPoint):
    return HttpResponse(f'cosutom Section "end point name : {endPoint}"')
# جلب البينات من قاعدة البيانات وعرضها 
def dbview(request):
    # هنا ننشئ متغير يمثل كلاس لمودل الجدول
    pag1var = page1.objects.all()
    # هنا نسطيع تفكيك مصفوفة البيانات القادمة من قاعدة البيانات
    for pag1va in pag1var:
        print("for loop "+pag1va.name)
    # هنا نستطيع طباعة قسم معين داخل صف معين
    print(pag1var[0].name+"\n"+str(pag1var[1].id)+"\n"+str(pag1var[0].createdDate))
    # هذه الدالة"str" يقوم بتحويل البيانات الى النص
    # هنا نقوم بتغير البيانات القادمة من المودل الى صيغة جيسون
    return JsonResponse(list(pag1var.values()),safe = False, content_type='application/json; charset=UTF-8') 
    # هنا نقوم بتغير صف واحد من المصفوف القادمة من المودل
    # return JsonResponse(list(pag1var.values()[0]),safe = False, content_type='application/json; charset=UTF-8') 
    # values() هذا الدالة يرد لنا البيانات بصيغة مصفوفة بدلا من صيفة المودل
# في هذا الداالة يمكننا استدعاء صفوف معينا حسب المطلبات 
def showOne(request):
    # هنا نستدعي الصفوف التي تساوي معرفها 1
    # pag1var = page1.objects.filter(id=1)
    # هنا نستدعي الصفوف التي تساوي اسمائها hassan
    pag1var = page1.objects.filter(name="anwar")
    return JsonResponse(list(pag1var.values())[0],safe = False, content_type='application/json; charset=UTF-8') 
# Delete table form database
def deleteOne(request):
    # هنا نستدعي الصف المطلوب
    pag1var = page1.objects.filter(name="ghalib")
    # هنا نتحقق اذا كان هناك صف يحمل نفس البيانات 
    if pag1var.count() != 0:
      pag1var.delete()
      return HttpResponse("deleted")
    else :return HttpResponse("not deleted or not found row to this data"),
@csrf_exempt
def addTable(request):
    method = request.method
    if method == "POST" and request.POST.get("name",'') != '':
        # هنا نضيف صف جديد في الجدول داخل قاعدة البيانات
        page1.objects.create(name = request.POST.get("name",''),createdDate = "2015-02-11 14:43:20.770507")
        print(f"post {method} .. {request.POST.get("name",'')}")
    else:
        print(f"get {method} .. {request.GET.get("name",'')}")
    return HttpResponse("hassan")
def updataTable(request):
    pag1var = page1.objects.filter(id=1)
    print(pag1var[0].name)
    pag1var.update(name= "hasna")
    print(pag1var[0].name)
    return HttpResponse(pag1var[0].name)
# لانشاء استدعاء البيانات في خطاب مخصص من قاعدة البيانات دون المرور الى ملف الموديل
def costumSelect(request):
    # هذا دالة استدعاء خاص من قاعدة البيانات ونمرر له البيانات اللازمة
    data = sql_query(
        # هنا نمرر له اسم المودل
        page1,
        # هنا نمرر له كلاس تسلسل البيانات
        Page1Serializer,
        # هنا نمرر له اسماء الاعمدة المطلوب استردادهم ونمرر له * اذا كان جميع الاعمدة مطلوب استرداده
        "*",
        # هنا نمرر له اسم الصف المطلوب استرداده من قاعدة البيانات
        "page1_page1",
        # هنا نمرر له شروط استدعاء البيانات من قاعدة البيانات
        "name LIKE %s OR id LIKE %s",
        # هنا نمرر له قيم الشروط في البرميتر السابق
        ["%hassan%","%26%"]
        )
    return JsonResponse(data , safe=False, content_type='application/json; charset=UTF-8')
@csrf_exempt
def uploadFiles(request):
    # هنا نفحص اذا كان الطلب يحمل بيانات بوست واذا كان هناك برميتر بوست باسم image
    uploaded_file = request.FILES.get('image')
    if request.method == 'POST' and uploaded_file:
        original_name, file_extension = os.path.splitext(uploaded_file.name)
        unique_name = f"{random.randint(10, 5000)}_{id_generator(7)}_{random.randint(10, 5000)}{file_extension}"  # إنشاء اسم فريد باستخدام UUID
        # الحصول على معلومات الملف
        file_name = unique_name  # اسم الملف
        file_size = uploaded_file.size  # حجم الملف بالبايت
        file_type = uploaded_file.content_type  # نوع الملف (MIME type)
        # هنا نحفظ الملف في المسار المطلوب. ونجلب اسم الملف من داخل ملف الاعدادات في المتغير
        save_path = os.path.join(settings.IMAGE_ROOT, file_name)  # المسار الذي تريد حفظ الملف فيه
        with open(save_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        # إرجاع معلومات الملف
        response_message = [
            f"تم رفع الملف بنجاح!",
            f"اسم الملف: {file_name}",
            f"حجم الملف: {file_size} بايت",
            f"نوع الملف: {file_type}",
            f"تم الحفظ في: {save_path}",
            settings.IMAGE_URL+file_name,
        ]
        # randint(0, 255)
        return JsonResponse(response_message , safe=False, content_type='application/json; charset=UTF-8')
    else:
        return HttpResponse("الطلب غير مدعوم. يرجى استخدام POST.", status=405)
# hashlib.md5("hass".encode('UTF-8')).hexdigest()
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))