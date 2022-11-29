from rest_framework import viewsets
from rest_framework.response import Response
from accounts.models import User, UserProfile
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from vendor.models import Vendor
from .serializers import UserSerializer, UserProfileSerializer


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    # permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        return User.objects.get(user=request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        userprofile = UserProfile.objects.get(user=instance)
        userializer = UserProfileSerializer(instance=userprofile)
        serializer = self.get_serializer(instance)
        return Response({'user': serializer.data,
                        'userprofile': userializer.data})


class UserProfileViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = None
    serializer_class = UserProfileSerializer

    # def list(self, request, *args, **kwargs):
    #     return Response(UserProfileSerializer(
    #         instance=self.get_queryset().get(user=request.user)).data)

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
