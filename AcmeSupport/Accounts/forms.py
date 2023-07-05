



from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, Ticket



from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Ticket

from .models import Department

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number', 'password1', 'password2','role','department')




# class TicketForm(forms.ModelForm):
#     class Meta:
#         model = Ticket
#         fields = ['subject', 'body', 'priority', 'ticket_email', 'ticket_phone_number']
#         widgets = {
#             'subject': forms.TextInput(attrs={'class': 'form-control'}),
#             'body': forms.Textarea(attrs={'class': 'form-control'}),
#             'priority': forms.Select(attrs={'class': 'form-control'}),
#             'ticket_email': forms.EmailInput(attrs={'class': 'form-control'}),
#             'ticket_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
#         }
        
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['ticket_email'].widget.attrs.update({'class': 'form-control'})
#         self.fields['ticket_phone_number'].widget.attrs.update({'class': 'form-control'}
class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['subject', 'body', 'priority', 'ticket_email', 'ticket_phone_number']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'ticket_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'ticket_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['ticket_email'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['ticket_phone_number'].widget.attrs.update({'class': 'form-control'}) 