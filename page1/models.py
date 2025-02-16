from django.db import models
from django.core import serializers
from rest_framework import serializers
# يمكن هنا انشاء كلاس الذي يكون على اسمه جدول في قاعدة البيانات والمتغيرات الذي بداخها يكون اعمدة في نفس الجدول في قاعدة البيانات
# Create your models here.
class page1(models.Model):
    name = models.TextField()
    createdDate = models.DateTimeField(auto_now_add=True)
    updataDate = models.DateTimeField(auto_now=True)
    # def __str__(self):
    #     return self.name
class Page1Serializer(serializers.ModelSerializer):
    hassan = None
    class Meta:
        model = page1
        fields = '__all__'