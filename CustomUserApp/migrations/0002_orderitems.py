# Generated by Django 4.2.13 on 2024-07-22 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CustomUserApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CustomUserApp.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CustomUserApp.product')),
            ],
        ),
    ]
