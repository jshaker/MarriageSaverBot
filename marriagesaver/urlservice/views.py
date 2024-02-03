from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from urlservice.models import ItemQueries, Items, Queries

class ItemQueryView(View):
    def get(self, request, *args, **kwargs):
        """Get all URL's from the database"""
        queries = Queries.objects.all()
        item_queries = ItemQueries.objects.all()
        # for item in item_queries:
            
        return JsonResponse({'queries': list(queries.values())}, status=200)

    def post(self, request, *args, **kwargs):
        """Add a URL to the database"""
        item_query = ItemQueries.objects.create(
            item_id = Items.objects.create(name="test", price=10.00),
            query_id = Queries.objects.create(
                query_type = "URL",
                query_text = "https://www.westelm.com"
            )
        )
        
        return JsonResponse({'success': f'item_query'}, status=201)
