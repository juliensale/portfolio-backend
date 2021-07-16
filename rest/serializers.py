from core.models import Technology
from rest_framework import serializers


class TechnologySerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = Technology
        fields = ('id', 'name', 'image')
