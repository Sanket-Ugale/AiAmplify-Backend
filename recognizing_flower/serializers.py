from rest_framework import serializers

class flowerPredictSerializer(serializers.Serializer):
    flowerImage = serializers.ImageField()
