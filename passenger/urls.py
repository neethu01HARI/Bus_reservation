from django.urls import path,include
from .views import*
urlpatterns = [
    path('passhome',PassHomeView.as_view(),name='passhome'),
    path('findbus',findbus,name='findbus'),
    path('bookings',bookings, name="bookings"),
    path('cancellings',cancellings, name="cancellings"),
    path('seebookings',seebookings, name="seebookings"),
    path('contact',contact,name="contact"),
    path('payment',PaymentView.as_view(),name="payment"),
    path('about',AboutView.as_view(),name='about'),


]