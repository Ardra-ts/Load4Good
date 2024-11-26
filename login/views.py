from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from img_app.models import FileUpload, PaymentDetail
from .forms import FileUploadForm,SignUpForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
# from django.urls import reverse
# from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.http import HttpResponse

# Create your views here.





def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = SignUpForm()  # Only create a new form instance for GET requests
    return render(request, 'sign_up.html', {'form': form})



def log_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('view')  # Redirect to the home page
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})



def log_out(request):
    logout(request)
    return render(request,'index.html')

@login_required
def my_pics(request):
    pics = FileUpload.objects.filter(user=request.user) 
    return render(request, 'my_pics.html', {'pics': pics})

@login_required
def pics(request):
    current_user = request.user  # Get the currently logged-in user
    pics = FileUpload.objects.exclude(user=current_user)
    return render(request, 'all.html', {'pics': pics})

def view(request):
    return render(request,'view.html')

@login_required
def add(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES, user=request.user)  # Pass user to form
        if form.is_valid():
            file = form.save(commit=False)
            file.user = request.user  # Make sure the uploaded file belongs to the current user
            file.save()  # Save the file instance to the database
            return redirect('my_pics')  # Redirect to 'my_pics' after saving the file
    else:
        form = FileUploadForm()

    return render(request, 'add.html', {'form': form})  # Render form for GET request

@login_required
def delete(request, pic_id):
    pic = get_object_or_404(FileUpload, id=pic_id,user=request.user)
    pic.delete()
    return redirect('my_pics')

@login_required
def edit(request, pic_id):
    pic = get_object_or_404(FileUpload, id=pic_id, user=request.user)  # Ensure the user is the owner

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES, instance=pic)  # Include request.FILES for image upload
        if form.is_valid():
            form.save() 
            return redirect('my_pics')  # Adjust redirect as necessary
    else:
        form = FileUploadForm(instance=pic)

    return render(request, 'edit.html', {'form': form, 'pic': pic})
    
import urllib.parse
PAYPAL_BASE_URL = 'https://www.sandbox.paypal.com'  # Use sandbox for testing; switch to live for production.


def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('file_list')
    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {'form': form})

def bill_form(request, pic_id):
    pic = get_object_or_404(FileUpload, id=pic_id)

    if request.method == "POST":
        

            # Example: Set payment amount (adjust as needed)
            payment_amount = 10.00  # Set the price for this bill
            currency = 'USD'

            # Redirect to PayPal payment page
            params = {
                'cmd': '_xclick',
                'business': settings.PAYPAL_RECIEVER_EMAIL,
                'item_name': f"Payment for {pic.discription}",
                'amount': f"{payment_amount:.2f}",
                'currency_code': currency,
                'return': request.build_absolute_uri(f'/login_app/payment-success/?pic_id={pic.id}'),  # Redirect URL after payment success
                'cancel_return': request.build_absolute_uri('/payment-cancel/'),  # Redirect URL after payment cancel
                'custom': f"{pic.id}"  # Pass custom data for tracking
            }
            paypal_url = f"{PAYPAL_BASE_URL}/cgi-bin/webscr?{urllib.parse.urlencode(params)}"
            return redirect(paypal_url)

    return render(request, "bill_form.html", {"pic": pic})

def downloads(request):
    pic_id = request.GET.get('pic_id')
    payer_id = request.GET.get('PayerID')  # PayerID from PayPal

    if not pic_id:
        return render(request, "error.html", {"message": "Image not found!"})

    # Get the FileUpload object
    pic = get_object_or_404(FileUpload, id=pic_id)
    user = request.user
    # Save payment details for the current transaction
    payment_detail = PaymentDetail.objects.create(
        pic=pic, 
        user= user,
        payer_id=payer_id,
        payment_status="Success"
    )

    # Retrieve all paid pictures
    paid_pictures = PaymentDetail.objects.filter(user=request.user).select_related('pic')

    # Pass payment details and all paid pictures to the template
    return render(request, "downloads.html", {
        "pic": pic,
        "payment_detail": payment_detail,
        "paid_pictures": paid_pictures
    })

def download(request):
    paid_pictures = PaymentDetail.objects.filter(user=request.user) # Fetch cars added by the logged-in user
    return render(request, 'downloads.html', {"paid_pictures": paid_pictures})   



def payment_cancel(request):
    # Handle payment cancellation
    return HttpResponse("Payment was canceled. Please try again.")

