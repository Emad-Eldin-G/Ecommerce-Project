from distutils.command.upload import upload
from operator import truediv
from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass

class Listing(models.Model):

    Categories = [
        ('Tech', 'Tech'),
        ('House', 'House'),
        ('Kitchen', 'Kitchen'),
        ('Sport', 'Sport'),
    ]

    User     = models.ForeignKey(User, on_delete=models.PROTECT)
    Title    = models.CharField(max_length=50)
    Details  = models.TextField(blank=True)
    Price    = models.FloatField()
    Category = models.CharField(max_length=20, choices=Categories, null=True, blank=True)

    def __str__(self):
        return self.Title


class Bid(models.Model):
    Listing      = models.ForeignKey(Listing, on_delete=models.CASCADE)
    Previous_Bid = models.FloatField(null=True)
    Current_Bid  = models.FloatField(null=True)
    Active       = models.BooleanField(null=True)

    def __str__(self):
        return (f"{self.Listing} {self.Current_Bid}")




class Comment(models.Model):
    User    = models.ForeignKey(User, on_delete=models.PROTECT)
    Listing = models.ForeignKey(Listing, on_delete=models.PROTECT)
    Comment = models.TextField()

    def __str__(self):
        return (f"{self.User} {self.Listing}")



class Wishlist(models.Model):
    User    = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    Listing = models.ForeignKey(Listing, on_delete=models.PROTECT, unique=True)

    def __str__(self):
        return (f"{self.User} {self.Listing}")

