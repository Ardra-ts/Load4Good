from django import forms
from img_app.models import FileUpload
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ('file','discription')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['file'].queryset = FileUpload.objects.filter(user=user)



class SignUpForm(UserCreationForm): 
    email = forms.EmailField(required=True)
    class Meta:
        model = User 
        fields = ('username', 'email', 'password1', 'password2')


