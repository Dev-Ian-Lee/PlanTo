from rest_framework import generics
from .models import *
from .serializers import *
from authentication.models import User
from authentication.renderers import UserJsonRenderer

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class Registration(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJsonRenderer, )