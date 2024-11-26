from django.shortcuts import render,redirect,get_object_or_404
from .forms import CharityForm
from .models import  Charity
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def add_char(request):
    if request.method == 'POST':
        form = CharityForm(request.POST, request.FILES)  # Pass user to form
        if form.is_valid():
            file = form.save(commit=False)
            file.save()  # Save the file instance to the database
            return redirect('char')  # Redirect to 'my_pics' after saving the file
    else:
        form = CharityForm()

    return render(request, 'add_char.html', {'form': form})

def home(request):
    return render(request,'home.html')

def char(request):
    char = Charity.objects.all() # Fetch cars added by the logged-in user
    return render(request, 'charity.html', {'char': char})

def log(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username') 
            password = form.cleaned_data.get('password')
            if username == 'admin' and password == 'admin':  # Replace 'admin' and 'admin_password' with your desired credentials
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')  # Redirect to the home page
                else:
                    messages.error(request, "Authentication failed.")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'log_in.html', {'form': form})


def out(request):
    logout(request)
    return render(request,'index.html')

@login_required
def delete_ch(request, pic_id):
    pic = get_object_or_404(Charity, id=pic_id)
    pic.delete()
    return redirect('char')

@login_required
def edit_ch(request, pic_id):
    pic = get_object_or_404(Charity, id=pic_id)  # Ensure the user is the owner

    if request.method == 'POST':
        form = CharityForm(request.POST, request.FILES, instance=pic)  # Include request.FILES for image upload
        if form.is_valid():
            form.save() 
            return redirect('char')  # Adjust redirect as necessary
    else:
        form = CharityForm(instance=pic)

    return render(request, 'edit_ch.html', {'form': form, 'char': char})
