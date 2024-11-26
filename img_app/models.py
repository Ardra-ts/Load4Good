from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os
def validate_file_type(value):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.mp4', '.mov', '.avi']
    import os
    ext = os.path.splitext(value.name)[1]
    if ext.lower() not in valid_extensions:
        raise ValidationError('Unsupported file extension.')


class FileUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    discription = models.CharField(max_length=100)
    file = models.FileField(upload_to='uploads/',validators=[validate_file_type])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Automatically set file_type based on file extension
        ext = os.path.splitext(self.file.name)[1].lower()
        if ext in ['.jpg', '.jpeg', '.png']:
            self.file_type = 'image'
        elif ext in ['.mp4', '.avi', '.mov']:
            self.file_type = 'video'
        else:
            self.file_type = 'unknown'
        super().save(*args, **kwargs)

    def is_image(self):
        return self.file_type == 'image'

    def is_video(self):
        return self.file_type == 'video'

class PaymentDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pic = models.ForeignKey('FileUpload', on_delete=models.CASCADE)  # Link to FileUpload
    payer_id = models.CharField(max_length=255)  # Store PayerID from PayPal
    payment_status = models.CharField(max_length=50, default="Success")
    payment_date = models.DateTimeField(auto_now_add=True)  # Automatically store timestamp
