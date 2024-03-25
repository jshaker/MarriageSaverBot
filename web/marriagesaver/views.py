import datetime
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import *
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import action

from .models import *
from .serializers import *

class PricesViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    serializer_class = PriceSerializer
    model = Price
    queryset = Price.objects.all()

    def perform_create(self, serializer):
        # Set date to today
        serializer.save(date=datetime.date.today())

    def create(self, request, *args, **kwargs):
        # Set default values for missing fields
        if 'date' not in request.data:
            request.data._mutable = True
            request.data['date'] = datetime.date.today()
            request.data._mutable = False

        return super().create(request, *args, **kwargs)
    
    @action(methods=['delete'], detail=False)
    def delete(self, request):
        if 'watcher_id' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # delete specific price
        if 'date' in request.data:
            price = Price.objects.get(date=request.data['date'], watcher_id=request.data['watcher_id'])
            price.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # delete all prices for watcher
        else:
            prices = Price.objects.filter(watcher_id=request.data['watcher_id'])
            prices.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

class WatchersViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    serializer_class = WatcherSerializer
    model = Watcher
    queryset = Watcher.objects.all()

    def delete(self, request):
        if 'id' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # delete specific price
        watcher = Watcher.objects.get(id=request.data['id'])
        watcher.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    