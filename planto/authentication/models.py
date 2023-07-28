from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.fields import BooleanField
from .managers import UserManager

import jwt
from datetime import datetime, timedelta
from django.conf import settings

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length = 255, unique = True)
    email = models.EmailField(db_index = True, unique = True)
    is_active = BooleanField(default = True)
    is_staff = BooleanField(default = False)

    # username 대신 email을 로그인 ID로 사용
    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["username"]

    # 커스텀 UserManager 등록
    objects = UserManager()

    def __str__(self):
        return self.email
    
    # 사용자의 jwt token을 쉽게 확인하기 위한 함수
    @property
    def token(self):
        return self.generate_jwt_token()

    def generate_jwt_token(self):
        # token의 기간 설정
        exp_date = datetime.now() + timedelta(days = 60)

        # token 생성
        token = jwt.encode(
            {"id": self.pk, "exp": exp_date.utcfromtimestamp(exp_date.timestamp())},
            settings.SECRET_KEY, algorithm = "HS256"
        )

        return token
    
    class Meta:
        db_table = "user"
