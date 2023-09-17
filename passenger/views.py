from typing import Any
from django.shortcuts import render,redirect
from .forms import ContactForm
from django.contrib import messages
from .models import Contact
from django.views.generic import TemplateView,View,ListView,DetailView,FormView
from django.shortcuts import render
from account.models import Bus,Book
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.shortcuts import render
from decimal import Decimal
from .forms import *
from django.urls import reverse_lazy
from django.contrib import messages
from account.forms import*


# decorator
def signin_required(fn):
    def inner(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
        else:
            messages.error(request,"Please login first")
            return redirect("h")
    return inner

decs=[never_cache,signin_required]


@method_decorator(decs,name='dispatch')
class PassHomeView(ListView):
    template_name="passhome.html"
    queryset=Bus.objects.all()
    context_object_name="bus"


decs
def findbus(request):
    if request.method == 'POST':
        source_r = request.POST.get('source')
        dest_r = request.POST.get('destination')
        date_r = request.POST.get('date')
        bus_list = Bus.objects.filter(source=source_r, dest=dest_r, date=date_r)
        
        if bus_list:
            return render(request, 'list.html', context={'bus_list': bus_list})
        else:
            return render(request, 'findbus.html', context={'error': "No available Bus Schedule for entered Route and Date"})
    else:
        return render(request, 'findbus.html')


decs
def bookings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('bus_id')
        seats_r = int(request.POST.get('no_seats'))
        bus = Bus.objects.get(id=id_r)
        if bus:
            if bus.rem > int(seats_r):
                name_r = bus.bus_name
                cost = int(seats_r) * bus.price
                source_r = bus.source
                dest_r = bus.dest
                nos_r = Decimal(bus.nos)
                price_r = bus.price
                date_r = bus.date
                time_r = bus.time
                username_r = request.user.username
                email_r = request.user.email
                userid_r = request.user.id
                rem_r = bus.rem - seats_r
                Bus.objects.filter(id=id_r).update(rem=rem_r)
                book = Book.objects.create(name=username_r, email=email_r, userid=userid_r, bus_name=name_r,
                                           source=source_r, busid=id_r,
                                           dest=dest_r, price=price_r, nos=seats_r, date=date_r, time=time_r,
                                           status='Booked')
                print('------------book id-----------', book.id)
                # book.save()
                return render(request,'bookings.html', locals())
            else:
                context["error"] = "Sorry select fewer number of seats"
                return render(request, 'findbus.html', context)

    else:
        return render(request,'findbus.html')



decs
def cancellings(request):
    if request.method == 'POST':
        id_r = request.POST.get('bus_id')

        try:
            book = Book.objects.get(id=id_r)
            bus = Bus.objects.get(id=book.busid)
            rem_r = bus.rem + book.nos
            Bus.objects.filter(id=book.busid).update(rem=rem_r)
            Book.objects.filter(id=id_r).update(status='Cancelled')
            Book.objects.filter(id=id_r).update(nos=0)
            messages.success(request, "Booked Bus has been cancelled successfully.")
            return redirect(seebookings)
        except Book.DoesNotExist:
            messages.error(request, "Sorry You have not booked that bus")
            return render(request, 'error.html')
    else:
        return render(request, 'findbus.html')



decs
def seebookings(request,*args,**kwargs):
    id_r = request.user.id
    book_list = Book.objects.filter(userid=id_r)
    if book_list:
        return render(request, 'booklist.html', {'book_list': book_list})
    else:
        error_message = "Sorry no buses booked"
        return render(request, 'findbus.html', {'error_message': error_message})


@method_decorator(decs,name='dispatch')
class AboutView(TemplateView):
    template_name="about.html"


@method_decorator(decs,name='dispatch')
class PaymentView(TemplateView):
    template_name="payment.html"
    def post(self,request,*args,**kwargs):
        id_r=kwargs.get("id")
        book=Book.objects.get(id=id_r)
        ad=request.POST.get("name")
        ph=request.POST.get("email")
        Book.objects.create(cart=book,name=ad,email=ph)
        book.status='Booked'
        book.save()
        messages.success(request,"order placed successfully")
        return redirect("seebookings")
    
decs
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and email and message:
            contact = Contact(name=name, email=email, message=message)
            contact.save()
            # messages.success(request,"Thank you! Your message has been sent successfully..")
            return redirect('passhome')
    return render(request, 'contact.html')


class PaymetView(TemplateView):
    template_name="payment.html"

    # def post(self,request,*args,**kwargs):
    #     cid=kwargs.get("id")
    #     book=Book.objects.get(id=cid)
    #     na=request.POST.get("name")
    #     # ph=request.POST.get("phone")
    #     Book.objects.create(book=book,name=na)
    #     Book.status='Paid'
    #     Book.save()
    #     messages.success(request," payment Completed ")
    #     return redirect("seebookings")