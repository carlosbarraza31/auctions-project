from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name = "create"),
    path("<str:title>/info", views.info, name = "info"),
    path("<str:title>/watchlist", views.watchlist, name = "watchlist"),
    path("<str:title>/newBid", views.newBid, name = "newBid"),
    path("<str:title>/close", views.close, name = "close"),
    path("<str:title>/activate", views.activate, name = "activate"),
    path("my_watchlist", views.my_watchlist, name = "my_watchlist"),
    path("categories", views.categories, name = "categories"),
    path("<str:category>/listings", views.category_listings, name = "category_listings"),
    path("active_listings", views.active_listings, name = "active_listings")
]
