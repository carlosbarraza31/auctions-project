# Generated by Django 3.2.5 on 2021-08-17 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0019_alter_listing_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, choices=[('Fashion', 'FS'), ('Toys', 'TO'), ('Electronics', 'ET'), ('Home', 'HM'), ('Art', 'AR'), ('Jewelry', 'JW'), ('Properties', 'PT'), ('Contracts', 'CT'), ('Miscellaneous', 'MS')], max_length=64),
        ),
        migrations.AlterField(
            model_name='listing',
            name='status',
            field=models.CharField(blank=True, choices=[('Active', 'AC'), ('Closed', 'CL')], default='Active', max_length=64),
        ),
    ]
