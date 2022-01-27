from contextlib import redirect_stderr
from multiprocessing import context
from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import User, Listing, Bid, Comment, Wishlist
from .forms import ListingForm



def index(request):

    Listings = Listing.objects.all().order_by('id').reverse()
    
    context = {
        "All_Listings": Listings
    }


    return render(request, "auctions/index.html", context)

#___________________________________________________________________________

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("commerce:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("commerce:index"))

#___________________________________________________________________________


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("commerce:index"))
    else:
        return render(request, "auctions/register.html")

#___________________________________________________________________________

@login_required(login_url='/login')
def Listing_Page(request, listing):
    listingq = Listing.objects.get(Title=listing)
    userq = User.objects.get(username=request.user)
    bidq = Bid.objects.filter(Listing=listingq)

    Title = listingq.Title
    Details = listingq.Details
    Price = listingq.Price
    Category = listingq.Category
    Owner = listingq.User

    if request.method == 'POST':
        if "Wishlist" in request.POST:
            wishlist = Wishlist(User=userq, Listing=listingq)
            wishlist.save()
            return render(request, "auctions/Success_wish.html")

    if request.method == 'POST':
        if "Bid" in request.POST:
            New_Bid = Bid(Listing=listingq, Previous_Bid=Price, Current_Bid=request.POST, Active=True)
            New_Bid.save()
            current = bidq.Current_Bid
            New_Price = listingq(Price=current)
            New_Price.save()

    if request.method == 'POST':
        if "Comment" in request.POST:
            wishlist = Wishlist(User=userq, Listing=listingq)
            wishlist.save()
            return render(request, "auctions/Success_wish.html")
            


    context = {
        "Title": Title,
        "Detials": Details,
        "Price": Price,
        "Category": Category,
        "Owner": Owner,
    }

    return render(request, "auctions/listing.html", context)

#___________________________________________________________________________

def new_listing(request):

    Current_User = request.user
    form = ListingForm()

    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            User = form.cleaned_data["User"]
            Title = form.cleaned_data["Title"]
            Details = form.cleaned_data["Details"]
            Price = form.cleaned_data["Price"]
            Category = form.cleaned_data["Category"]

            form.save()
            return render(request, 'auctions/success_save.html')

    
    return render(request, 'auctions/new.html')

#___________________________________________________________________________

def wishlist(request):
    Current_User = request.user
    wishlist = Wishlist.objects.filter(User=Current_User)

    context = {
        'User': Current_User,
        'Listings': wishlist,
    }
    
    return render(request,'auctions/wishlist.html', context)

    



            

