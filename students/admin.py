from django.contrib import admin
from .models import *
from django.utils.html import mark_safe
# Register your models here.

class AdminStudents(admin.ModelAdmin):
    search_fields = ['id', 'full_name', 'date_of_birth', 'address', 'username', 'email', 'student_class__name', 'phone_number', 'gender']
    list_display = ['id', 'full_name', 'date_of_birth', 'username', 'get_class_name', 'image']
    list_filter = ['student_class__name']  # Đổi 'classes__name' -> 'student_class__name'
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
    list_display = ['id', 'name', 'current_students']  # Đổi 'quantity' -> 'current_students'
    search_fields = ['id','name']


class AdminBook(admin.ModelAdmin):
    search_fields = ['id', 'title', 'price', 'quantity', 'author']  # Đổi 'name' -> 'title'
    list_display = ['id', 'title', 'author', 'quantity', 'price', 'image']  # Đổi 'name' -> 'title'
    list_per_page = 5
    readonly_fields = ["image_static"]

    def image_static(self, book):
        if book.avata:
            return mark_safe(f"<img src='{book.avata.url}' width='120px' style='border-radius: 5px;' />")
        return "No Image"

    def image(self, book):
        if book.avata:
            return mark_safe(f"<img src='{book.avata.url}' width='120px' style='border-radius: 5px;' />")
        return "No Image"



admin.site.register(Students,AdminStudents)
admin.site.register(Classes, AdminClasses)
admin.site.register(Book, AdminBook)