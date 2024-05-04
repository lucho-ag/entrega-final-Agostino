from django import forms

from .models import Reserva, Mesa, Mesero, Avatar
from django.contrib.auth.models import User

class AvatarCreateForm(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ['image']
                  
class ReservaSearchForm(forms.ModelForm):
    class Meta: 
        model = Reserva
        fields = ['nombre_de_usuario']
    
class MesaSearchForm(forms.Form):
    numero = forms.IntegerField(required=True, label="Ingresar numero de mesa")
    
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']