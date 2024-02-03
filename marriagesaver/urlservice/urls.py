from django.urls import path
# from .views import ItemQueryView
from urlservice.views import ItemQueryView

app_name = 'urlservice'

urlpatterns = [
    path('itemquery/', ItemQueryView.as_view(), name='itemquery'),
]