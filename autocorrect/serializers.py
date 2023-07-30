from rest_framework import serializers
from autocorrect.models import *
class autoCorrectSerializer(serializers.Serializer):
        str=serializers.CharField()