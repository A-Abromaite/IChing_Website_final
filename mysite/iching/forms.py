from .models import HexagramInstance
from django import forms
from django.contrib.auth.models import User

class HexagramInstanceForm(forms.ModelForm):
    class Meta:
        model = HexagramInstance
        fields = ["hexagram_number", "modified_hexagram_number", "note"]