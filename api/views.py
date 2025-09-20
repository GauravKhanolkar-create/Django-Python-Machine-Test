from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Client, Project
from .serializers import (
    ClientSerializer, ClientDetailSerializer, 
    ProjectCreateSerializer, ProjectResponseSerializer,
    UserProjectSerializer
)

class ClientListCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        return ClientSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        return ClientDetailSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProjectCreateView(generics.CreateAPIView):
    serializer_class = ProjectCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['client_id'] = self.kwargs['client_id']
        return context
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = serializer.save()
        
        response_serializer = ProjectResponseSerializer(project)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class UserProjectsView(generics.ListAPIView):
    serializer_class = UserProjectSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Project.objects.filter(users=self.request.user)