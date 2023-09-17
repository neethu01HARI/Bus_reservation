from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import View,FormView,CreateView,TemplateView
from .forms import *
from account.models import Book,Bus
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout





class HomeView(FormView):
    template_name="home.html"
    form_class=LoginForm

    def post(self,request,*args,**kwargs):
        form_data=LoginForm(data=request.POST)
        if form_data.is_valid():
            us=form_data.cleaned_data.get("username")
            pswd=form_data.cleaned_data.get("password")
            user=authenticate(request,username=us,password=pswd)
            if user:
                login(request,user)
                messages.success(request," login Successfully")
                return redirect('passhome')
            else:
                messages.error(request,"sign in failed.")
                return redirect('h')
        return render(request,"home.html",{"form":form_data})
    
class UserRegView(CreateView):
    template_name="reg.html"
    form_class=RegForm
    model=User
    success_url=reverse_lazy('h')

    def form_valid(self,form):
        messages.success(self.request,"User Registered Successfully")
        return super().form_valid(form)

    
class LgoutView(View):
    def get(self,request):
        logout(request)
        return redirect("h")
    



