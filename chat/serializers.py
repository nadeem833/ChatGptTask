from rest_framework import serializers
from .models import Conversation
from django.contrib.auth.models import User

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'  # You can specify fields explicitly if needed


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # To ensure password is write-only

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
