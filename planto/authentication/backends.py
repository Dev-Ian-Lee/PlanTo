import jwt

from django.conf import settings
from rest_framework import authentication, exceptions

from .models import User

class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'

    """
        모든 요청에서 호출되는 인증 메서드
        
        특정 요청의 헤더에 "token"이라는 문자열이 포함되지 않은 경우, None 반환(인증 실패)
        인증에 성공한 경우 _authenticate_credentials() 메서드 호출
    
    """

    def authenticate(self, request):
        
        # auth_header는 "token {사용자의 JWT token값}"의 형식
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        # auth_header의 "token", {사용자의 JWT token값}을 decode
        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        # auth_header가 위의 형식에서 벗어나는 경우, None 반환
        if not auth_header:
            return None

        if len(auth_header) != 2:
            return None

        if prefix.lower() != auth_header_prefix:
            return None

        return self._authenticate_credentials(request, token)

    """
        authenticate() 과정을 통과한 사용자에 대해 추가적인 인증 과정을 거친 후, 접근을 허가하는 메서드
        
        인증에 성공한 경우 (user, token) 반환
        에러 발생 시 AuthenticationFailed Exception 반환
    
    """

    def _authenticate_credentials(self, request, token):
        
        # JWT token decode 가능 여부 확인
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms = ['HS256'])
            
        except:
            msg = 'Invalid authentication. Could not decode token.'
            raise exceptions.AuthenticationFailed(msg)

        # 사용자 존재 여부 확인
        try:
            user = User.objects.get(pk = payload['id'])
            
        except User.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)

        # 사용자 비활성화 여부 확인
        if not user.is_active:
            msg = 'This user has been deactivated.'
            raise exceptions.AuthenticationFailed(msg)

        return (user, token)