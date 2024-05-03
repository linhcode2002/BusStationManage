from rest_framework.serializers import ModelSerializer
from .models import *

class BusCompanySerializer(ModelSerializer):
    class Meta:
        model = BusCompany
        fields = ['id', 'name', 'description', 'avatar']

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'avatar']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }
    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(data['password'])
        user.save()
        return user