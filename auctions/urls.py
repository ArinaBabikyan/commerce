from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.add, name="add"),
    path("watchlist", views.watchlist, name="watchlist"), 
    path("<str:name>/", views.listing, name="listing"),
    path("<str:name>/new_bid", views.new_bid, name="new_bid"),
    path("<str:name>/close", views.close, name="close"),
    path("<str:name>/to_wtchl", views.to_wtchl, name="to_wtchl"),
    path("categories", views.categories, name="categories"), 
    path("categories/<str:name>", views.show_category, name="show_category"), 
    path("<str:name>/new_com", views.new_com, name='new_com')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
