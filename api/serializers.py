from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Client, Project

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.username
        }

class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'project_name']
        
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.project_name
        }

class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'created_by']

class ClientDetailSerializer(serializers.ModelSerializer):
    projects = ProjectListSerializer(many=True, read_only=True)
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Client
        fields = ['id', 'client_name', 'projects', 'created_at', 'created_by', 'updated_at']

class ProjectCreateSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)
    
    class Meta:
        model = Project
        fields = ['project_name', 'users']
    
    def create(self, validated_data):
        users_data = validated_data.pop('users')
        client_id = self.context['client_id']
        client = Client.objects.get(id=client_id)
        
        project = Project.objects.create(
            project_name=validated_data['project_name'],
            client=client,
            created_by=self.context['request'].user
        )
        
        user_ids = [user_data['id'] for user_data in users_data]
        users = User.objects.filter(id__in=user_ids)
        project.users.set(users)
        
        return project

class ProjectResponseSerializer(serializers.ModelSerializer):
    client = serializers.CharField(source='client.client_name', read_only=True)
    users = UserSerializer(many=True, read_only=True)
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client', 'users', 'created_at', 'created_by']

class UserProjectSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Project
        fields = ['id', 'project_name', 'created_at', 'created_by']