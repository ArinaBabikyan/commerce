from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .models import User, Listing, Comment


def index(request):
    if request.user.is_authenticated:
        return render(request, "auctions/index.html", {'listings': Listing.objects.all().order_by('closed', 'title').values(), 'logged_in': 'yes'})
    else:
        return render(request, "auctions/index.html", {'listings': [], 'logged_in': "no"})

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

def add(request):
    if request.method == "POST": 
        title = request.POST["title"]
        description = request.POST["description"]
        bid = request.POST["bid"]
        image_url = request.POST.get('image_url')
        category = request.POST.get('category')

        listing = Listing(title=title, description=description, starting_bid=bid, new_bid=bid)
        if image_url:
            listing.image_url = image_url
        if category:
            listing.category = category
        listing.closed = False
        listing.you_won = False
        listing.last_bid = request.user
        listing.save()
        request.user.listings.add(listing)
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/add.html")


def listing(request, name):
    listing = Listing.objects.get(pk=name)
    listing.you_won = False
    if listing in request.user.listings.all():
        ability_to_close = True
    else:
        if request.user == listing.last_bid and listing.closed:
            listing.you_won = True
        ability_to_close = False
        
    comms = listing.comments.all().values_list()
    comments = []
    for i in comms:
        username = get_object_or_404(User, id=i[1]).username
        comments.append(username + ": " + i[2])
    return render(request, 'auctions/listing.html', {'item': listing, 'close': ability_to_close,'comms': comments})
    


def new_bid(request, name):
    if request.method == "POST": 
        bid = request.POST['new_bid']
        if int(bid) < Listing.objects.get(pk=name).new_bid:
            return HttpResponse("<h1>New bid should be higher than current.</h1>")
        Listing.objects.filter(pk=name).update(new_bid=int(bid))
        Listing.objects.filter(pk=name).update(last_bid=request.user)
        #Listing.objects.update(new_bid=)
        # listing.update(new_bid=request.POST['new_bid'])
        return HttpResponseRedirect(reverse("listing", args=(name, )))
    

def categories(request):
    di = {}
    for i in (Listing.objects.all()):
        cat = Listing.objects.get(pk=i).category
        if not cat in di.keys():
            di[cat] = [i.title]
        else:
            di[cat].append(i.title)
    return render(request, 'auctions/categories.html', {'categories': di.keys(), 'valueslist': di})

def show_category(request, name):
    res = []
    for i in (Listing.objects.all()):
        cat = Listing.objects.get(pk=i).category
        if str(cat) == str(name):
            res.append(i)
    if request.user.is_authenticated:
        return render(request, "auctions/index.html", {'listings': res, 'logged_in': 'yes'})
    else:
        return render(request, "auctions/index.html", {'listings': res, 'logged_in': 'no'})


def watchlist(request):
    watchlist = request.user.watchlist.all()
    return render(request, 'auctions/index.html', {'listings': watchlist.order_by('title').values(), 'logged_in': 'yes'})


def to_wtchl(request, name):
    listing = get_object_or_404(Listing, pk=name)
    request.user.watchlist.add(listing)
    return HttpResponseRedirect(reverse('watchlist'))

def close(request, name):
    Listing.objects.filter(pk=name).update(closed=True)
    return render(request, 'auctions/listing.html', {'item': Listing.objects.get(pk=name),'close': True})

def new_com(request, name):
    listing = get_object_or_404(Listing, pk=name)
    if request.method == 'POST':
        comment_text = request.POST.get('new_com')
        if comment_text:
            # Create and save the comment
            comment = Comment(author=request.user, comm=comment_text)
            comment.save()
            # Add the comment to the listing
            
            listing.comments.add(comment)
            
    return HttpResponseRedirect(reverse("listing", args=(name, )))
    