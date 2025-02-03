from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.validators import UniqueValidator
from .models import Students, Classes, Book
import re
from django.utils import timezone


class ClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classes
        fields = '__all__'

class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_full_name(self, value):
        if not re.match(r"^[\p{L} ]+$", value):
            raise serializers.ValidationError("Tên chỉ được chứa chữ cái và khoảng trắng")
        return value.strip().title()

    def validate_username(self, value):
        if len(value) < 8 or len(value) > 16:
            raise serializers.ValidationError("Username phải có độ dài từ 8 đến 16 ký tự")
        if ' ' in value:
            raise serializers.ValidationError("Username không được có khoảng trống")
        if not re.match("^[A-Za-z0-9_]+$", value):
            raise serializers.ValidationError("Username không được chứa ký tự đặc biệt")
        return value

    def validate_phone_number(self, value):
        if not re.match(r"^\d{10}$", value):
            raise serializers.ValidationError("Số điện thoại phải có đúng 10 chữ số.")
        return value

    def validate_date_of_birth(self, value):
        today = timezone.now().date()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 6:
            raise serializers.ValidationError("Học sinh phải từ 6 tuổi trở lên")
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def validate_isbn(self, value):
        if not re.match(r"^[0-9]{13}$", value):
            raise serializers.ValidationError("ISBN phải có đúng 13 chữ số")
        return value