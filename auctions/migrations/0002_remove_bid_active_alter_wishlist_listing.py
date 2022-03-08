# Generated by Django 4.0.3 on 2022-03-08 03:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='Active',
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='Listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.listing', unique=True),
        ),
    ]