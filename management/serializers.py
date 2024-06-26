from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project, ProjectMember, Task, Comment
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password






class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined','password']
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password field is write-only
            'id': {'read_only': True},  # Prevent id from being modified manually
            'date_joined': {'read_only': True}  # Prevent date_joined from being modified manually
        }

    def create(self, validated_data):
        """
        Create and return a new User instance, given the validated data.
        """
        password = validated_data.pop('password', None)  # Extract password from validated data
        user = User(**validated_data)  # Create a new User instance with remaining data

        if password:
            user.set_password(password)  # Set password using set_password method
        else:
            raise serializers.ValidationError({'password': 'Password field is required.'})

        user.save()  # Save the user instance
        return user

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'created_at']

class ProjectMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMember
        fields = ['id', 'project', 'user', 'role']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'assigned_to', 'project', 'created_at', 'due_date']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'task', 'created_at']
