from rest_framework import serializers
from accounts.models import User, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id",
                  "first_name",
                  "last_name",
                  "username",
                  "email",
                  "phone_number",
                  #   "password",
                  #   "confirm_password",
                  )


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("id", "profile_picture",
                  "cover_photo",
                  "address",
                  "country",
                  "state",
                  "city",
                  "pincode",
                  "latitude",
                  "longitude",)
