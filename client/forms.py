from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Row, Column, Reset
from django import forms

from .models import *

class InscriptionForm(forms.ModelForm):

    numTel = forms.IntegerField()
    numPermis = forms.IntegerField()

    class Meta:
        model = User
        fields = [
            'username',
            'last_name',
            'first_name',
            'password'
        ]   

    def __init__(self, *args, **kwargs):
        super(InscriptionForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class = 'form-group col-md-6 mb-0' ),
                Column('last_name', css_class = 'form-group col-md-6 mb-0'),
                css_class = 'form-row'
            ),
            Row(
                Column('numTel', css_class = 'form-group col-md-6 mb-0'),
                Column('numPermis', css_class = 'form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('username', css_class = 'form-group col-md-6 mb-0'),
                Column('password', css_class = 'form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
           
        )
        self.helper.add_input(Submit('submit', 'Save person'))
        self.helper.add_input(Reset('reset', 'annuler',css_class='btn-danger'))

class ConnexionForm(forms.Form):

    username = forms.CharField(label='Nom utilisateur',widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    password = forms.CharField(label='Mot de passe',widget=forms.TextInput(attrs={'type':'password','class':'form-control'}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Save person'))
        self.helper.add_input(Reset('reset', 'annuler',css_class='btn-danger'))
    