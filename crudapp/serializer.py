from rest_framework import serializers
from .models import User, U2

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'phone', 'createdDate']


class U2Serializer(serializers.HyperlinkedModelSerializer):
    user  = UserSerializer()
    class Meta:
        model = U2
        fields = ['id', 'name', 'user']