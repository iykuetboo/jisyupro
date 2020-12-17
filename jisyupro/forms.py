from django import forms
from .models import FaceImage

class FaceImageForm(forms.ModelForm):
    your_name = forms.CharField(max_length=50,required=True)
    class Meta:
        model = FaceImage
        fields = ('image','your_name')
