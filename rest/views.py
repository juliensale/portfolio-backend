import os
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import action
from rest_framework.response import Response
from rest.serializers import LightProjectSerializer, ProjectImageSerializer,\
    ProjectSerializer, ReviewSerializer, TechnologySerializer,  SkillSerializer
from core.models import Project, Review, Skill, Technology
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
        project = self.get_object()
        serializer = self.get_serializer(
            project,
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

    @action(
        methods=['get'],
        detail=True,
        permission_classes=[IsAdminOrIsGet, ],
        url_path="review"
    )
    def review(self, request, pk=None):
        """Retrieves the associated review"""
        project = self.get_object()
        associated_review = Review.objects.all().filter(project=project.id)[0]
        serializer = ReviewSerializer(associated_review, data=request.data)
        if serializer.is_valid():
            return Response(
                status=status.HTTP_200_OK,
                data=serializer.data
            )
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data=serializer.errors
        )


class ReviewPermission(BasePermission):
    """Permission that authorizes all GET methods and
    requires the Admin Token for all other kind of method"""
    keyword = 'Token'

    def has_permission(self, request, view):
        if request.method == "GET" or view.action == "with_code":
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


class ReviewItemViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin):

    permission_classes = (ReviewPermission,)
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return self.queryset.order_by('author')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(modified=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=['get', 'patch', 'put'],
        detail=False,
        url_path='with-code'
    )
    def with_code(self, request, *args, **kwargs):
        if request.method == 'GET':
            try:
                update_code = request.query_params.get('update_code')
                instance = Review.objects.all().get(
                    update_code=update_code
                )
                serializer = self.get_serializer(instance)
                return Response(
                    status=status.HTTP_200_OK,
                    data=serializer.data
                )

            except KeyError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        elif request.method == 'PATCH' or request.method == 'PUT':
            try:
                update_code = request.data['update_code']
                if update_code is not None:
                    try:
                        instance = Review.objects.all().get(
                            update_code=update_code)
                        partial = kwargs.pop('partial', False)
                        serializer = self.get_serializer(
                            instance, data=request.data, partial=partial)
                        if serializer.is_valid():
                            serializer.save()
                            return Response(serializer.data)
                        else:
                            return Response(status=status.HTTP_400_BAD_REQUEST)
                    except ObjectDoesNotExist:
                        return Response(status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response(status=status.HTTP_403_FORBIDDEN)
            except KeyError:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(
        methods=['get'],
        detail=False,
        url_path="get-all"
    )
    def get_all(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
