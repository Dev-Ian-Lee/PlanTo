from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User
from todo.models import Task
from job_announcement.models import Job

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 128, write_only = True, required = True, validators = [validate_password])
    
    # User가 소유한 Task 모델(일정)과 Job 모델(채용공고)을 PrimaryKeyRelatedField로 연결
    tasks = serializers.PrimaryKeyRelatedField(many = True, queryset = Task.objects.all())
    jobs = serializers.PrimaryKeyRelatedField(many = True, queryset = Job.objects.all())

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        
        if password is not None:
            instance.set_password(password)
        
        for key, value in validated_data.items():
            setattr(instance, key, value)
            
        instance.save()
        
        return instance

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password", "token", "tasks"]
        
class RegistrationSerializer(serializers.ModelSerializer):
    # django의 password validation 사용해 비밀번호 검증
    password = serializers.CharField(max_length = 128, write_only = True, required = True, validators = [validate_password])
    password2 = serializers.CharField(max_length = 128, write_only = True, required = True)
    
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
        
class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length = 255, read_only = True)
    email = serializers.EmailField()
    password = serializers.CharField(max_length = 128, write_only = True)
    
    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        
        # 검증 과정에서 에러 발생 시 ValidationError 반환
        if email is None:
            raise serializers.ValidationError("이메일 주소를 입력해주십시오.")
        
        if password is None:
            raise serializers.ValidationError("비밀번호를 입력해주십시오.")
        
        user = authenticate(username = email, password = password)
        
        # 인증 과정에서 에러 발생 시 AuthenticationFailed 반환
        if user is None:
            raise AuthenticationFailed("이메일 주소 혹은 비밀번호가 잘못 입력되었습니다.")
        
        if not user.is_active:
            raise AuthenticationFailed("유효하지 않은 계정입니다.")

        return {"email": user.email, "username": user.username}
    
    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password"]