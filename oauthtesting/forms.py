from django import forms
from .models import Account

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('bio', 'picture')
        widgets = {
            'picture': forms.TextInput(attrs={"placeholder": "Ex: https://i.imgur.com/GvsgVcol.jpg"})
        }
        labels = {
            'bio': 'Biography', 'picture': 'Picture URL'
        }
