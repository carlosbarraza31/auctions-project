# Generated by Django 3.2.5 on 2021-08-17 22:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_alter_bid_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='status',
            field=models.CharField(choices=[('AC', 'Active'), ('CL', 'Closed')], default='Active', max_length=64),
        ),
        migrations.AddField(
            model_name='listing',
            name='winner',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='listing_winner', to='auctions.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, choices=[('FS', 'Fashion'), ('TO', 'Toys'), ('ET', 'Electronics'), ('HM', 'Home'), ('AR', 'Art'), ('JW', 'Jewelry'), ('PT', 'Properties'), ('CT', 'Contracts'), ('MS', 'Miscellaneous')], max_length=64),
        ),
        migrations.AlterField(
            model_name='listing',
            name='current_bid',
            field=models.FloatField(default=0.0),
        ),
    ]