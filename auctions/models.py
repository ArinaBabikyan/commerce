from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    listings = models.ManyToManyField('Listing', related_name='user_listings')
    watchlist = models.ManyToManyField('Listing', related_name='user_watchlist')
    

class Listing(models.Model):
    title = models.CharField(max_length=64, primary_key=True)
    description = models.CharField(max_length=300)
    starting_bid = models.IntegerField()
    image_url = models.URLField(blank=True, null=True)  # URLField to store the image URL
    category = models.CharField(max_length=50, null=True, blank=True)
    new_bid = models.IntegerField(null=True, blank=True)
    closed = models.BooleanField(null=True, blank=True)
    last_bid = models.ForeignKey('User', related_name='last_bid_user', null=True, blank=True, on_delete=models.CASCADE,)
    you_won =  models.BooleanField(null=True, blank=True)
    comments = models.ManyToManyField('Comment', related_name='Comment', null=True, blank=True)
    def __str__(self):
        return self.title
    

class Comment(models.Model):
    author = models.ForeignKey('User', related_name='comm_author', on_delete=models.CASCADE)
    comm = models.TextField(null=True, blank=True)

