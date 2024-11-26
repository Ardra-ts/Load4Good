from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .import views
urlpatterns=[
    path('signup/',views.signup,name="signup"),
    path('login/',views.log_in, name='login'),
    path('view/',views.view,name='view'),
    path('add/', views.add, name='add'),
    path('logout/',views.log_out, name='logout'),
    path('delete/<int:pic_id>/', views.delete, name='delete'),
    path('edit/<int:pic_id>/',views.edit,name='edit'),
    path('my_pics/', views.my_pics, name='my_pics'),
    path('pics/', views.pics, name='pics'),
    path('bill_form/<int:pic_id>/', views.bill_form, name='bill_form'),
    path('payment-success/', views.downloads, name='downloads'),
    path('payment-cancel/', views.payment_cancel, name='payment_cancel'),
    path('paypal',include("paypal.standard.ipn.urls")),
    path('download/', views.download, name='download'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)