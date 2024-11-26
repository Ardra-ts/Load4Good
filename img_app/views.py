from django.shortcuts import render
from django.http import HttpResponse
from .models import FileUpload
from admin_app.models import Charity
# Create your views here.

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def portfolio(request):
    pics = FileUpload.objects.all()
    return render(request,'portfolio.html', {'pics': pics})

def ch_detail(request):
    ch = Charity.objects.all()
    return render(request,'ch_details.html', {'ch': ch})

