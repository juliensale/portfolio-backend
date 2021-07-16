import os
from rest.serializers import TechnologySerializer
from core.models import Technology
from rest_framework import viewsets, mixins
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
