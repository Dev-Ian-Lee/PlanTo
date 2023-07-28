from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import User
from .serializers import *
from .renderers import UserJsonRenderer

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class UserDetail(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer
    renderer_classes = (UserJsonRenderer, )
    
class Registration(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJsonRenderer, )
    
class Login(APIView):
    permission_classes = (AllowAny, )
    serializer_class = LoginSerializer
    renderer_classes = (UserJsonRenderer, )
    
    def post(self, request):
        user = request.data
        
        serializer = self.serializer_class(data = user)
        serializer.is_valid(raise_exception = True)
        
        return Response(serializer.data, status = status.HTTP_200_OK)