from .models import Hexagram
from django import forms
from django.contrib.auth.models import User

class HexagramForm(forms.ModelForm):
    class Meta:
        model = Hexagram
        fields = ["number", "description", "meaning"]