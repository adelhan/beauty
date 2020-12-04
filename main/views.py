from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework import permissions, viewsets, filters, pagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Category, Place, Application, Master, Comment
from .permisssions import IsCommentAuthor, ApplicationPermission, IsApplicationAuthor
from .serializers import CategoryListSerializers, CategoryCreateSerializers, PlaceListSerializers, \
    PlaceCreateSerializers, ApplicationCreateSerializers, ApplicationListSerializers, MasterListSerializers, \
    MasterCreateSerializers, CommentSerializer


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })

class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title']

class CategoryCreateView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializers


class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializers
    lookup_field = 'slug'

class PlaceListView(ListAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceListSerializers

class PlaceCreateView(CreateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceCreateSerializers

class PlaceDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceListSerializers
    lookup_field = 'slug'

class MasterListView(ListAPIView):
    queryset = Master.objects.all()
    serializer_class = MasterListSerializers

class MasterCreateView(CreateAPIView):
    queryset = Master.objects.all()
    serializer_class = MasterCreateSerializers

class ApplicationListView(ListAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationListSerializers
    pagination_class = CustomPagination

class ApplicationCreateView(CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationCreateSerializers
    permission_classes = [IsApplicationAuthor, ]

class ApplicationDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationListSerializers
    lookup_field = 'slug'


    def get_permissions(self):
        if self.action in ['update', 'retrieve', 'delete']:
            permissions = []
        else:
            permissions = [ApplicationPermission, ]
        return [permission() for permission in permissions]

# class CategoryDestroyView(DestroyAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategoryListSerializers
#
# class CategoryUpdateView(UpdateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategoryCreateSerializers

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [ApplicationPermission, ]
    queryset = Comment.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permissions = []
        else:
            permissions = [IsAuthenticated, IsCommentAuthor, ]
        return [permission() for permission in permissions]


class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])