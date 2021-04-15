from rest_framework import serializers
from AllModels.models import Post,Comment


class PostSerializer(serializers.ModelSerializer):
    # author = serializers.CharField(required = False)
    class Meta:
        model =Post
        fields = ("id","title","content","excerpt","campus","Published","category", "images","subAuthor")

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("post","name","body")