from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from authentication.models import User

class UserSerializer(serializers.ModelSerializer):
    # User의 Task 객체를 PrimaryKeyRelatedField로 연결
    tasks = serializers.PrimaryKeyRelatedField(many = True, queryset = Task.objects.all())

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "tasks"]
        
class RegistrationSerializer(serializers.ModelSerializer):
    # django의 password validation 사용해 비밀번호 검증
    password = serializers.CharField(write_only = True, required = True, validators = [validate_password])
    password2 = serializers.CharField(write_only = True, required = True)
    
    token = serializers.CharField(max_length = 128, read_only = True)
    
    # 확인용 비밀번호 일치 여부 검증
    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "두 비밀번호가 일치하지 않습니다."})
        
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password", "password2", "token"]