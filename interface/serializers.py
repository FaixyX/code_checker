from rest_framework import serializers
from .models import MyUser, ProgrammingLanguage, ExpertiseLevel


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        exclude = ('email' , 'password')


class UserProfileRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        exclude = ('password', )


class ProgrammingLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammingLanguage
        fields = '__all__'


class ExpertiseLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpertiseLevel
        fields = '__all__'
