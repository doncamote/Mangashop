from rest_framework import serializers
from MangaShop.models import Manga

class MangaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Manga
        fields = '__all__'