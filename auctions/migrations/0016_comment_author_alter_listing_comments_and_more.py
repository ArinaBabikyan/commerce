# Generated by Django 4.2.14 on 2024-07-26 19:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_comment_listing_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='comm_author', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='listing',
            name='comments',
            field=models.ManyToManyField(blank=True, null=True, related_name='Comment', to='auctions.comment'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='last_bid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='last_bid_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
