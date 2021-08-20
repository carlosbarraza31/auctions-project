from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms.models import ModelForm
from django.forms.widgets import Textarea
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Bid, Comment, Listing, User


class ListingForm(ModelForm):
    description = forms.CharField(widget = forms.Textarea, max_length = 500)

    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'url', 'category']

class CommentForm(ModelForm):
    content = forms.CharField(widget = forms.Textarea(attrs={'rows':3, 'cols':60}), max_length=500)
    class Meta:
        model = Comment
        fields = ['content']

class BidForm(ModelForm):
    amount = forms.FloatField(widget = forms.TextInput(attrs={'size':3}))
    class Meta:
        model = Bid
        fields = ['amount']

@login_required(login_url = '/login')
def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        'listings': listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url = '/login')
def create(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            starting_bid = form.cleaned_data["starting_bid"]
            current_bid = starting_bid
            category = form.cleaned_data["category"]
            url = form.cleaned_data["url"]
            author = request.user
            watchlist_status = "Add to watchlist"
            if url == None:
                url = "NoFileUploaded.png"

            listing = Listing(title = title, description = description, starting_bid = starting_bid, current_bid = current_bid, url = url, category = category, author = author, watchlist_status = watchlist_status)
            listing.save()
            return redirect('index')
        else:
            return redirect('info', title = 'bye')

    else:
        return render(request, 'auctions/createListing.html', {
            'form': ListingForm()
        })

@login_required(login_url = '/login')
def info(request, title):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            author = request.user
            listing = Listing.objects.get(title = title)
            comment = Comment(content = content, user = author, listing = listing)
            comment.save()
            return HttpResponseRedirect(reverse('info', kwargs={'title': title}))
    else:
        listing = Listing.objects.get(title = title)
        comments = Comment.objects.filter(listing = listing).order_by('-date')
        user = request.user
        if request.user in listing.watchlist_users.all():
            listing.watchlist_status = "Remove from watchlist"
        else:
            listing.watchlist_status = "Add to watchlist"
        listing.save()
        return render(request, 'auctions/listingInfo.html', {
            'listing': listing,
            'form': CommentForm(),
            'comments': comments,
            'bidform':BidForm(),
            'message': "Comment succesfully posted.",
            'user': user
        })

@login_required(login_url = '/login')
def watchlist(request, title):
    listing = Listing.objects.get(title = title)
    user = request.user
    if request.method == "POST":
        if user not in listing.watchlist_users.all():
            listing.watchlist_users.add(user)
            listing.watchlist_status = "Remove from watchlist"
            listing.save()
        else:
            listing.watchlist_users.remove(user)
            listing.watchlist_status = "Add to watchlist"
            listing.save()

        return HttpResponseRedirect(reverse('info', kwargs={'title':title}))

    else:
        pass

@login_required(login_url = '/login')
def newBid(request, title):
    if request.method == "POST":
        listing = Listing.objects.get(title = title)
        user = request.user
        form = BidForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            if amount >= listing.starting_bid and amount > listing.current_bid:
                listing.winner = user
                listing.current_bid = amount
                listing.save()
                message = "Congratulations! Your bid is now the current bid of this listing." 
                messages.success(request, message)
                return redirect('info', title = title)
            else:
                message = f"Bid must be at least as large as the starting bid and greater than the current bid ({ listing.current_bid } US$) ."
                messages.error(request, message)
                return redirect('info', title = title)
        
        else:
            message = "Invalid form input. "
            messages.error(request, message)
            return redirect('info', title = title)
    else:
        pass

@login_required(login_url = '/login')
def close(request, title):
    if request.method == "POST":
        listing = Listing.objects.get(title = title)
        listing.status = 'Closed'
        listing.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        pass

@login_required(login_url = '/login')
def activate(request, title):
    if request.method == "POST":
        listing = Listing.objects.get(title = title)
        listing.status = 'Active'
        listing.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        pass

@login_required(login_url = '/login')
def my_watchlist(request):
    user = request.user
    listings = Listing.objects.filter(watchlist_users__in=[user])
    return render(request, 'auctions/my_watchlist.html', {
        'listings':listings,
        'user': user
    })

@login_required(login_url = '/login')
def categories(request):
    categories = Listing._meta.get_field('category').choices
    first_elements = []
    for tuple in categories:
        first_elements.append(tuple[0])
    return render(request, 'auctions/categories.html', {
        'categories': first_elements
    })

@login_required(login_url = '/login')
def category_listings(request, category):
    listings = Listing.objects.filter(category = category)
    return render(request, 'auctions/category_listings.html', {
        'listings':listings,
        'category': category
    })

@login_required(login_url = '/login')
def active_listings(request):
    listings = Listing.objects.filter(status ='Active')
    return render (request, 'auctions/active_listings.html', {
        'listings': listings
    })
    
