from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        style={'input_type': 'password'},
        min_length=8,
        help_text="Password must be at least 8 characters long"
    )

    password2 = serializers.CharField(
        write_only=True, 
        style={'input_type': 'password'},
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'password2',
            'first_name',
            'last_name',
            'role',
            'department',
            'phone',
            'bio'
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        """Check that the two password entries match"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        # Remove password2 before creating user
        validated_data.pop('password2')
        
        password = validated_data.pop('password')

        # Create user with hashed password
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=password,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', 'TeamMember'),
            department=validated_data.get('department', 'Other'),
            phone=validated_data.get('phone', ''),
            bio=validated_data.get('bio', '')
        )
        return user


# Serializer for viewing user details
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'department',
            'phone',
            'bio',
            'date_joined'
        ]
        read_only_fields = ['date_joined']