from django.contrib.auth.models import User
from rest_framework import serializers

from chat.models import Message


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    online = serializers.ReadOnlyField(source='userprofile.online')

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'online','email',]


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'timestamp']

class UseresSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
           
            'password',

        )
        def save(self):

            useres = User(
                username=self.validated_data['username'],
                email=self.validated_data['email'],
               
                password=self.validated_data['password'],
                )
            useres.save()
            data['response']="Successful"
            return Response(data)


class userLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields= ('username', 'password',)