# Generated by Django 3.2.5 on 2021-08-16 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_comment_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.CharField(help_text='Post a comment', max_length=500),
        ),
    ]
