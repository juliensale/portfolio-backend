from core.models import Project, Review, Skill, Technology
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


class LightProjectSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'image', 'technologies')
        read_only_fields = ('id', 'image')


class ProjectSerializer(serializers.ModelSerializer):

    image = serializers.ImageField()

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('id', 'image')
        extra_kwargs = {
            'github': {'required': False},
            'client': {'required': False},
            'link': {'required': False},
            'duration': {'required': False},
            'technologies': {'required': False}
        }


class ProjectImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = Project
        fields = ('id', 'image')
        read_only_fields = ('id',)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'author', 'message', 'project', 'modified')
        read_only_fields = ('id', 'project', 'update_code', 'modified')
