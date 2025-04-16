from rest_framework import serializers
from .models import MyUser


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        exclude = ('email' , 'password')


class UserProfileRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        exclude = ('password', )
