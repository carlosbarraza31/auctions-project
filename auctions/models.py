from django.contrib.auth.models import AbstractUser
from django.db import models


class Comment(models.Model):
    content = models.CharField(max_length = 500)
    date = models.DateTimeField(auto_now_add = True)
    user = models.ForeignKey('User', on_delete = models.CASCADE, related_name = 'user_comments')
    listing = models.ForeignKey('Listing', on_delete = models.CASCADE, related_name = 'comments')

    def __str__(self):
        return f"Comment created on {self.date}"


class Listing(models.Model):
    title = models.CharField(max_length=64, help_text = "Title")
    description = models.CharField(max_length = 500, help_text = "Description")
    starting_bid = models.FloatField(help_text = "Starting Bid Amount in US$")
    current_bid = models.FloatField(default = 0.00)
    url = models.ImageField(blank = True)
    timestamp = models.DateTimeField(auto_now_add=True)

    FASHION = 'Fashion'
    TOYS = 'Toys'
    ELECTRONICS = 'Electronics'
    HOME = 'Home'
    ART = 'Art'
    JEWELRY = 'Jewelry'
    PROPERTIES = 'Properties'
    CONTRACTS = 'Contracts'
    MISCELLANEOUS = 'Miscellaneous'

    ACTIVE = 'Active'
    CLOSED = 'Closed'

    CATEGORY_CHOICES = [
        (FASHION, 'FS'),
        (TOYS, 'TO'),
        (ELECTRONICS, 'ET'),
        (HOME, 'HM'),
        (ART, 'AR'),
        (JEWELRY, 'JW'),
        (PROPERTIES, 'PT'),
        (CONTRACTS, 'CT'),
        (MISCELLANEOUS, 'MS')
    ]

    STATUS_CHOICES = [
        (ACTIVE, 'AC'),
        (CLOSED, 'CL')
    ]
    category = models.CharField(max_length = 64, choices = CATEGORY_CHOICES, blank = True)
    author = models.ForeignKey('User', on_delete = models.CASCADE, related_name = 'listing_author', default = "")
    watchlist_users = models.ManyToManyField('User', blank = True, related_name = 'watched_listing')
    watchlist_status = models.CharField(max_length = 21)
    winner = models.ForeignKey('User', on_delete = models.CASCADE, related_name = 'listing_winner', blank = True, null = True)
    status = models.CharField(max_length=64, choices = STATUS_CHOICES, blank = True, default = 'Active')

    def __str__(self):
        return f"Bidding for item: {self.title}, price: {self.starting_bid}"


class Bid(models.Model):
    amount = models.FloatField()
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "bids")
    user = models.ForeignKey('User', on_delete = models.CASCADE, related_name = 'user_bids', default = "request.user")

    def __str__(self):
        return f"Bid for item: {self.listing} for {self.amount}$"

class User(AbstractUser):
    pass