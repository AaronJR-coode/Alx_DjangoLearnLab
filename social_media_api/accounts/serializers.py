from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import User

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()


    class Meta:
        model = User
        fields = [
            'id', 'username', 'bio', 'email', 'profile_picture', 'following', 'followers'
        ]

    def get_following(self, obj):
        return obj.following.count()
    

    def get_followers(self, obj):
        return User.objects.filter(followers=obj).count()
    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'password'
        ]

    def create(self, validate_data):
        user = get_user_model().objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        Token.objects.create(user=user)
        return user
        
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid username or password")
        data["user"] = user

        return data



