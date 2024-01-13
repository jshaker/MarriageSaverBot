from django.contrib import admin
from .models import Items, Queries, ItemQueries

class ItemsAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'name', 'price') 
    list_filter = ['name', 'price']
    search_fields = ['name', 'price']

class QueriesAdmin(admin.ModelAdmin):
    list_display = ('query_id', 'query_type', 'query_text', 'query_date') 
    list_filter = ['query_type']
    search_fields = ['query_text', 'query_date']

class ItemQueriesAdmin(admin.ModelAdmin):
    list_display = ('item_query_id', 'item_id', 'query_id') 
    list_filter = ['item_id', 'query_id']
    search_fields = ['item_id', 'query_id']

admin.site.register(Items, ItemsAdmin)
admin.site.register(Queries, QueriesAdmin)
admin.site.register(ItemQueries, ItemQueriesAdmin)
