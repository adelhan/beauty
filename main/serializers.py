from rest_framework import serializers
from .models import Category, Place, Application, Master, Comment
from rest_framework.permissions import IsAuthenticated

class RecursiveSerializer(serializers.Serializer):

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CategoryListSerializers(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)

    class Meta:
        model = Category
        fields = ('title', 'slug', 'children', 'parent')

class CategoryCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title', 'slug', 'parent')



class PlaceListSerializers(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)

    class Meta:
        model = Place
        fields = ('title', 'slug', 'price', 'parent', 'children')


class PlaceCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ('title', 'slug', 'price', 'parent', 'categories')


class MasterListSerializers(serializers.ModelSerializer):

    class Meta:
        model = Master
        fields = ('name', 'surname', 'places')

    def _get_image_url(self, obj):
        request = self.context.get('request')
        image_obj = obj.images.first()
        if image_obj is not None and image_obj.image:
            url = image_obj.image.url
            if request is not None:
                url = request.build_absolute_uri(url)
            return url
        return "No Image"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if "comment" not in self.fields:
            representation['comments'] = CommentSerializer(instance.comment_set.all(), many=True).data
        return representation

class MasterCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = ('name', 'surname', 'places')

class ApplicationListSerializers(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = ('master', 'time', 'user')


class ApplicationCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('master','time', 'user')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('master', 'text')

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author_id'] = request.user
        comment = Comment.objects.create(**validated_data)
        return comment

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # representation['author'] = CommentSerializer(instance.author_id).data
        # representation['text'] = CommentSerializer(instance.text).data
        return representation