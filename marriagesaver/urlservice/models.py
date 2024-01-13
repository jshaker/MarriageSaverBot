from django.db import models


class Items(models.Model):
    item_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Queries(models.Model):
    query_id = models.AutoField(primary_key=True)
    query_type = models.CharField(max_length=50, choices=[('URL', 'URL'), ('QUERY', 'QUERY')])
    query_text = models.CharField(max_length=1000, help_text="Full URL or search query")
    query_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.query_text

class ItemQueries(models.Model):
    item_query_id = models.AutoField(primary_key=True)
    item_id = models.ForeignKey(Items, on_delete=models.CASCADE)
    query_id = models.ForeignKey(Queries, on_delete=models.CASCADE)

    def __str__(self):
        return self.item_id.name + " - " + self.query_id.query_text