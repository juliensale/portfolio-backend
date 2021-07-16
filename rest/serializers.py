from core.models import Skill, Technology
from rest_framework import serializers


class TechnologySerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = Technology
        fields = ('id', 'name', 'image')


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'date',  'name', 'description', 'technology')
