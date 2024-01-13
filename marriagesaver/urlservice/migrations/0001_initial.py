# Generated by Django 5.0.1 on 2024-01-13 05:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Items',
            fields=[
                ('item_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Queries',
            fields=[
                ('query_id', models.AutoField(primary_key=True, serialize=False)),
                ('query_type', models.CharField(choices=[('URL', 'URL'), ('QUERY', 'QUERY')], max_length=50)),
                ('query_text', models.CharField(help_text='Full URL or search query', max_length=1000)),
                ('query_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ItemQueries',
            fields=[
                ('item_query_id', models.AutoField(primary_key=True, serialize=False)),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='urlservice.items')),
                ('query_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='urlservice.queries')),
            ],
        ),
    ]
