from rest_framework import serializers

class tweetAnalysisSerializer(serializers.Serializer):
    analyzeTweet = serializers.CharField()
