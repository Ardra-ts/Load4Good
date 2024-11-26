from django.urls import path
from .import views
urlpatterns=[
    path('home/',views.home,name='home'),
    path('add_char/', views.add_char, name='add_char'),
    path('char/', views.char, name='char'),
    path('log_in/',views.log, name='log_in'),
    path('out/',views.out, name='out'),
    path('delete_ch/<int:pic_id>/', views.delete_ch, name='delete_ch'),
    path('edit_ch/<int:pic_id>/',views.edit_ch,name='edit_ch'),
]