from rest_framework import serializers
from .models import *


class PriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Price
        fields = '__all__'

class WatcherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Watcher
        fields = '__all__'

