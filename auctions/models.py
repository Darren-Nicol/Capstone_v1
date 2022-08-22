"""Contains all models used in the app."""
from django.contrib.auth.models import AbstractUser
from django.db import models

import sys

class User(AbstractUser):
    """User model - inherited from Django implementation"""
    pass

class Auction(models.Model):
    """Auction model contains all info about one auction:
    * auction's title
    * auction's description
    * who is selling
    * auction's current price
    * when auction was published
    * when will it close
    * what is auction's category
    * auction's image URL
    * is auction closed?
    * partners
    """

    # Categories - choices
    COLLECTION1 = "Genesis"
    COLLECTION2 = "Ghetto Kings"
    COLLECTION3 = "Township Princess"


    CATEGORY = [
        (COLLECTION1, "Genesis"),
        (COLLECTION2, "Ghetto Kings"),
        (COLLECTION3, "Township Princess")
    ]

    # Model fields
    # auto: auction_id
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64, blank=False)
    description = models.TextField(blank=True)
    current_price = models.DecimalField(max_digits=11, decimal_places=2, default=0.0)
    category = models.CharField(max_length=30, choices=CATEGORY, default=COLLECTION1)
    image_url = models.URLField(blank=True)
    publication_date = models.DateTimeField(auto_now_add=True)
    close_date = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True) # added close_date field also need to change to allow for close date to be added not 'auto_now'
    closed = models.BooleanField(default=False)
    

    class Meta:
        verbose_name = "auction"
        verbose_name_plural = "auctions"

    def __str__(self):
        return f"Auction id: {self.id}, title: {self.title}, seller: {self.seller}"

class Bid(models.Model):
    """Bid model contains all info about single bid:
    * price
    * who bid
    * when
    * on what auction
    """

    # Model fields
    # auto: bid_id
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_date = models.DateTimeField(auto_now_add=True)
    bid_price = models.DecimalField(max_digits=11, decimal_places=2)

    class Meta:
        verbose_name = "bid"
        verbose_name_plural = "bids"

    def __str__(self):
        return f"{self.user} bid {self.bid_price} $ on {self.auction}"

class Comment(models.Model):
    """Comment model contains all info about single comment
    * content
    * who posted
    * when
    * on what auction
    """

    # Model fields
    # auto: comment_id
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(blank=False)
    comment_date = models.DateTimeField(auto_now_add=True, null=True)
    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"

    def __str__(self):
        return f"Comment {self.id} on auction {self.auction} made by {self.user}"

class Watchlist(models.Model):
    """Watchlist model contains all info about object on watchlist
    * which auction is on watchlist
    * on whose watchlist this auction is
    """

    # Model field
    # auto: watchlist_id
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")

    class Meta:
        verbose_name = "watchlist"
        verbose_name_plural = "watchlists"
        # Forces to not have auction duplicates for one user
        unique_together = ["auction", "user"]

    def __str__(self):
        return f"{self.auction} on user {self.user} watchlist"
