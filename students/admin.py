from django.contrib import admin
from .models import *
from django.utils.html import mark_safe
# Register your models here.

class AdminStudents(admin.ModelAdmin):
    search_fields = ['id','name','age','address','username','email','classes__name','phone_number','sex']
    list_display = ['id','name','age','username','get_class_name','image']
    list_filter = ['classes__name']
    list_per_page = 5
    readonly_fields = ["image_static"]

    def image_static(self, avata):
        if avata.avata:
            return mark_safe(f"<img src='{avata.avata.url}' width='120px' style='border-radius: 5px;' />")
        return "No Image"
    
    def get_class_name(self, obj):
        return obj.classes.name if obj.classes else "No Class"
    get_class_name.short_description = 'Class Name'

    def image(self, avata):
        if avata.avata:
            return mark_safe(f"<img src='{avata.avata.url}' width='120px' style='border-radius: 5px;' />")
        return "No Image"


class AdminClasses(admin.ModelAdmin):
    list_display = ['id','name','quantity']
    search_fields = ['id','name']

admin.site.register(Students,AdminStudents)
admin.site.register(Classes, AdminClasses)