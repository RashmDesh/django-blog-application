from rest_framework.serializers import ModelSerializer
from .models import blogpost

class BlogSerializer(ModelSerializer):

    class Meta:
        model = blogpost
        fields = ["title", "content", "category"]