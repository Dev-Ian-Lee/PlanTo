from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, email, password = None, **extra_fields):
        if username is None:
            raise TypeError("이름을 입력해주십시오.")
        
        if email is None:
            raise TypeError("이메일 주소를 입력해주십시오.")
        
        if password is None:
            raise TypeError("비밀번호를 입력해주십시오.")
        
        user = self.model(username = username, email = self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, username, email, password, **extra_fields):
        
        # 사용자 생성 후 관리자로 지정
        user = self.create_user(username, email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user