import os
from rest_framework.decorators import action
from rest_framework.response import Response
from rest.serializers import LightProjectSerializer, ProjectImageSerializer,\
    ProjectSerializer, TechnologySerializer,  SkillSerializer
from core.models import Project, Skill, Technology
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import BasePermission
from rest_framework.authentication import get_authorization_header


class IsAdminOrIsGet(BasePermission):
    """Permission that authorizes all GET methods and
    requires the Admin Token for all other kind of method"""
    keyword = 'Token'

    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return False

        if len(auth) == 1:
            return False
        elif len(auth) > 2:
            return False
        try:
            token = auth[1].decode()
            return token == os.environ['ADMIN_TOKEN']
        except UnicodeError:
            return False


class TechnologyItemViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin):
    permission_classes = (IsAdminOrIsGet,)
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer

    def get_queryset(self):
        return self.queryset.order_by('name')


class SkillItemViewSet(viewsets.GenericViewSet,
                       mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin):
    permission_classes = (IsAdminOrIsGet,)
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

    def get_queryset(self):
        return self.queryset.order_by('name')

    def create(self, request, *args, **kwargs):
        try:
            returnValue = super(SkillItemViewSet, self).create(
                request, *args, **kwargs)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return returnValue

    def update(self, request, *args, **kwargs):
        try:
            returnValue = super(SkillItemViewSet, self).update(
                request, *args, **kwargs)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return returnValue


class ProjectItemViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.CreateModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin):
    permission_classes = (IsAdminOrIsGet,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return self.queryset.order_by('name')

    def create(self, request, *args, **kwargs):
        try:
            returnValue = super(ProjectItemViewSet, self).create(
                request, *args, **kwargs)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return returnValue

    def update(self, request, *args, **kwargs):
        try:
            returnValue = super(ProjectItemViewSet, self).update(
                request, *args, **kwargs)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return returnValue

    def get_serializer_class(self):
        """Returns the appropriate serializer class"""
        if self.action == 'upload_image':
            return ProjectImageSerializer
        elif self.action == 'list':
            return LightProjectSerializer
        return self.serializer_class

    @action(
        methods=['post'],
        detail=True,
        permission_classes=[IsAdminOrIsGet, ],
        url_path='upload_image'
    )
    def upload_image(self, request, pk=None):
        """Uploads an image to a project"""
        drawing = self.get_object()
        serializer = self.get_serializer(
            drawing,
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                status=status.HTTP_200_OK,
                data=serializer.data
            )
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data=serializer.errors
        )
